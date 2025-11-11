/** Assessment page component */
import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Box, Button, Typography, CircularProgress, Alert, Paper, Container } from '@mui/material';
import { ArrowBack, ArrowForward, Send } from '@mui/icons-material';
import { motion } from 'framer-motion';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { assessmentService } from '../services/assessmentService';
import { QuestionCard } from '../components/assessment/QuestionCard';
import { MultipleChoice } from '../components/assessment/MultipleChoice';
import { TrueFalse } from '../components/assessment/TrueFalse';
import { ShortAnswer } from '../components/assessment/ShortAnswer';
import { QuizResults } from '../components/assessment/QuizResults';
import type { AssessmentSubmitResponse } from '../types/assessment';
import { QuestionType } from '../types/assessment';

export const AssessmentPage: React.FC = () => {
  const { moduleId } = useParams<{ moduleId: string }>();
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState<Record<number, string>>({});
  const [submittedAnswers, setSubmittedAnswers] = useState<Record<number, AssessmentSubmitResponse>>({});
  const [showResults, setShowResults] = useState(false);
  const [startTime] = useState(Date.now());

  // Fetch assessments
  const {
    data: assessmentData,
    isLoading: isLoadingAssessments,
    error: assessmentError,
  } = useQuery({
    queryKey: ['assessments', moduleId],
    queryFn: () => assessmentService.getModuleAssessments(Number(moduleId)),
    enabled: !!moduleId,
  });

  // Fetch results
  const {
    data: resultsData,
  } = useQuery({
    queryKey: ['assessment-results', moduleId],
    queryFn: () => assessmentService.getModuleResults(Number(moduleId)),
    enabled: !!moduleId && showResults,
  });

  // Submit answer mutation
  const submitAnswerMutation = useMutation({
    mutationFn: ({ assessmentId, answer }: { assessmentId: number; answer: string }) => {
      const timeSpent = Math.floor((Date.now() - startTime) / 1000);
      return assessmentService.submitAnswer(assessmentId, {
        user_answer: answer,
        time_spent_seconds: timeSpent,
      });
    },
    onSuccess: (data, variables) => {
      setSubmittedAnswers((prev) => ({
        ...prev,
        [variables.assessmentId]: data,
      }));
    },
  });

  const assessments = assessmentData?.assessments || [];
  const currentAssessment = assessments[currentQuestionIndex];
  const currentAnswer = answers[currentAssessment?.id || 0] || '';
  const currentResult = submittedAnswers[currentAssessment?.id || 0];

  const handleAnswerChange = (answer: string) => {
    if (currentAssessment) {
      setAnswers((prev) => ({
        ...prev,
        [currentAssessment.id]: answer,
      }));
    }
  };

  const handleSubmitAnswer = async () => {
    if (!currentAssessment || !currentAnswer) return;

    await submitAnswerMutation.mutateAsync({
      assessmentId: currentAssessment.id,
      answer: currentAnswer,
    });
  };

  const handleNext = () => {
    if (currentQuestionIndex < assessments.length - 1) {
      setCurrentQuestionIndex((prev) => prev + 1);
    } else {
      // Last question - show results
      setShowResults(true);
      queryClient.invalidateQueries({ queryKey: ['assessment-results', moduleId] });
    }
  };

  const handleRetake = () => {
    setShowResults(false);
    setCurrentQuestionIndex(0);
    setAnswers({});
    setSubmittedAnswers({});
  };

  if (isLoadingAssessments) {
    return (
      <Box sx={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', backgroundColor: '#0a0e27' }}>
        <CircularProgress />
      </Box>
    );
  }

  if (assessmentError) {
    return (
      <Box sx={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', p: 4, backgroundColor: '#0a0e27' }}>
        <Alert severity="error">
          Failed to load assessments. Please try again.
        </Alert>
      </Box>
    );
  }

  if (assessments.length === 0) {
    return (
      <Box sx={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', p: 4, backgroundColor: '#0a0e27' }}>
        <Alert severity="info">No assessments available for this module.</Alert>
      </Box>
    );
  }

  if (showResults && resultsData) {
    return <QuizResults results={resultsData} onRetake={handleRetake} />;
  }

  if (!currentAssessment) {
    return (
      <Box sx={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', p: 4, backgroundColor: '#0a0e27' }}>
        <Alert severity="info">No assessments available for this module.</Alert>
      </Box>
    );
  }

  const isAnswerSubmitted = currentResult !== undefined;

  return (
    <Box sx={{ minHeight: '100vh', backgroundColor: '#0a0e27', py: 4 }}>
      <Container maxWidth="md">
        {/* Header */}
        <Box sx={{ mb: 4 }}>
          <Typography variant="h4" sx={{ fontWeight: 'bold', color: '#ffffff', mb: 2 }}>
            {assessmentData?.module_title}
          </Typography>
          <Typography variant="body2" sx={{ color: 'rgba(255, 255, 255, 0.8)' }}>
            {assessmentData?.total_points} points • Estimated time: {assessmentData?.estimated_time_minutes} minutes
          </Typography>
        </Box>

        {/* Progress Bar */}
        <Paper
          sx={{
            backgroundColor: '#ffffff',
            borderRadius: 2,
            p: 3,
            mb: 4,
            boxShadow: '0 2px 10px rgba(0, 0, 0, 0.2)',
          }}
        >
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
            <Typography variant="body2" sx={{ color: '#666666' }}>
              Progress: {currentQuestionIndex + 1} / {assessments.length}
            </Typography>
            <Typography variant="body2" sx={{ color: '#666666' }}>
              {Math.round(((currentQuestionIndex + 1) / assessments.length) * 100)}%
            </Typography>
          </Box>
          <Box sx={{ width: '100%', height: 8, backgroundColor: '#e0e0e0', borderRadius: 1, overflow: 'hidden' }}>
            <motion.div
              style={{
                height: '100%',
                backgroundColor: '#1976d2',
              }}
              initial={{ width: 0 }}
              animate={{ width: `${((currentQuestionIndex + 1) / assessments.length) * 100}%` }}
              transition={{ duration: 0.3 }}
            />
          </Box>
        </Paper>

        {/* Question Card */}
        <QuestionCard
          assessment={currentAssessment}
          questionNumber={currentQuestionIndex + 1}
          totalQuestions={assessments.length}
        >
          {currentAssessment.question_type === QuestionType.MULTIPLE_CHOICE && (
            <MultipleChoice
              assessment={currentAssessment}
              selectedAnswer={currentAnswer}
              onAnswerSelect={handleAnswerChange}
              result={currentResult}
              disabled={isAnswerSubmitted}
            />
          )}

          {currentAssessment.question_type === QuestionType.TRUE_FALSE && (
            <TrueFalse
              assessment={currentAssessment}
              selectedAnswer={currentAnswer}
              onAnswerSelect={handleAnswerChange}
              result={currentResult}
              disabled={isAnswerSubmitted}
            />
          )}

          {(currentAssessment.question_type === QuestionType.SHORT_ANSWER ||
            currentAssessment.question_type === QuestionType.CODING_TASK) && (
            <ShortAnswer
              assessment={currentAssessment}
              answer={currentAnswer}
              onAnswerChange={handleAnswerChange}
              result={currentResult}
              disabled={isAnswerSubmitted}
            />
          )}
        </QuestionCard>

        {/* Action Buttons */}
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mt: 4 }}>
          <Button
            startIcon={<ArrowBack />}
            onClick={() => navigate(`/modules/${moduleId}`)}
            variant="outlined"
            sx={{
              borderColor: '#999999',
              color: '#ffffff',
              '&:hover': {
                borderColor: '#ffffff',
                backgroundColor: 'rgba(255, 255, 255, 0.1)',
              },
            }}
          >
            Back to Module
          </Button>

          <Box sx={{ display: 'flex', gap: 2 }}>
            {!isAnswerSubmitted && currentAnswer && (
              <Button
                variant="contained"
                startIcon={<Send />}
                onClick={handleSubmitAnswer}
                disabled={submitAnswerMutation.isPending}
                sx={{
                  backgroundColor: '#1976d2',
                  '&:hover': {
                    backgroundColor: '#1565c0',
                  },
                }}
              >
                Submit Answer
              </Button>
            )}

            <Button
              variant="contained"
              endIcon={<ArrowForward />}
              onClick={handleNext}
              disabled={!isAnswerSubmitted && !currentAnswer}
              sx={{
                backgroundColor: '#1976d2',
                '&:hover': {
                  backgroundColor: '#1565c0',
                },
                '&:disabled': {
                  backgroundColor: '#999999',
                },
              }}
            >
              {currentQuestionIndex === assessments.length - 1 ? 'View Results' : 'Next'}
            </Button>
          </Box>
        </Box>
      </Container>
    </Box>
  );
};
