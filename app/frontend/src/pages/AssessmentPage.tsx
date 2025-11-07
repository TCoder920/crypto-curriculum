/** Assessment page component */
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Box, Button, Typography, CircularProgress, Alert, Paper } from '@mui/material';
import { ArrowBack, ArrowForward, CheckCircle, Send } from '@mui/icons-material';
import { motion } from 'framer-motion';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { assessmentService } from '../services/assessmentService';
import { QuestionCard } from '../components/assessment/QuestionCard';
import { MultipleChoice } from '../components/assessment/MultipleChoice';
import { TrueFalse } from '../components/assessment/TrueFalse';
import { ShortAnswer } from '../components/assessment/ShortAnswer';
import { QuizResults } from '../components/assessment/QuizResults';
import type { Assessment, AssessmentSubmitResponse } from '../types/assessment';
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
    isLoading: isLoadingResults,
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
      // Show results
      setShowResults(true);
      queryClient.invalidateQueries({ queryKey: ['assessment-results', moduleId] });
    }
  };

  const handlePrevious = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex((prev) => prev - 1);
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
      <Box className="min-h-screen flex items-center justify-center">
        <CircularProgress />
      </Box>
    );
  }

  if (assessmentError) {
    return (
      <Box className="min-h-screen flex items-center justify-center p-4">
        <Alert severity="error">
          Failed to load assessments. Please try again.
        </Alert>
      </Box>
    );
  }

  if (showResults && resultsData) {
    return <QuizResults results={resultsData} onRetake={handleRetake} />;
  }

  if (!currentAssessment) {
    return (
      <Box className="min-h-screen flex items-center justify-center p-4">
        <Alert severity="info">No assessments available for this module.</Alert>
      </Box>
    );
  }

  const isAnswerSubmitted = currentResult !== undefined;
  const canProceed = isAnswerSubmitted || currentAnswer.length > 0;

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 dark:from-gray-900 dark:to-blue-900 p-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <Box className="mb-6">
          <Button
            startIcon={<ArrowBack />}
            onClick={() => navigate('/')}
            className="mb-4"
          >
            Back to Modules
          </Button>
          <Typography variant="h4" component="h1" className="font-bold mb-2">
            {assessmentData?.module_title}
          </Typography>
          <Typography variant="body2" color="text.secondary">
            {assessmentData?.total_points} points • Estimated time: {assessmentData?.estimated_time_minutes} minutes
          </Typography>
        </Box>

        {/* Progress Bar */}
        <Paper className="glass-surface rounded-2xl p-4 mb-6" elevation={0}>
          <Box className="flex items-center justify-between mb-2">
            <Typography variant="body2" color="text.secondary">
              Progress: {currentQuestionIndex + 1} / {assessments.length}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              {Math.round(((currentQuestionIndex + 1) / assessments.length) * 100)}%
            </Typography>
          </Box>
          <Box className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
            <motion.div
              className="bg-primary h-2 rounded-full"
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
        <Box className="flex justify-between items-center">
          <Button
            startIcon={<ArrowBack />}
            onClick={handlePrevious}
            disabled={currentQuestionIndex === 0}
            variant="outlined"
          >
            Previous
          </Button>

          {!isAnswerSubmitted ? (
            <Button
              endIcon={<Send />}
              onClick={handleSubmitAnswer}
              disabled={!currentAnswer || submitAnswerMutation.isPending}
              variant="contained"
            >
              {submitAnswerMutation.isPending ? 'Submitting...' : 'Submit Answer'}
            </Button>
          ) : (
            <Button
              endIcon={<ArrowForward />}
              onClick={handleNext}
              variant="contained"
            >
              {currentQuestionIndex === assessments.length - 1 ? 'View Results' : 'Next'}
            </Button>
          )}
        </Box>
      </div>
    </div>
  );
};

