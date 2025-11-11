/** Quiz results component */
import React from 'react';
import { Box, Typography, Paper, LinearProgress, Button, Alert } from '@mui/material';
import { CheckCircle, Cancel, CheckCircleOutline, ErrorOutline, HourglassEmpty } from '@mui/icons-material';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import type { ModuleResultsResponse, QuizAttempt } from '../../types/assessment';
import { ReviewStatus } from '../../types/assessment';

interface QuizResultsProps {
  results: ModuleResultsResponse;
  onRetake?: () => void;
}

export const QuizResults: React.FC<QuizResultsProps> = ({ results, onRetake }) => {
  const navigate = useNavigate();
  const scoreColor = results.score_percent >= 70 ? 'success' : 'error';
  const canProgress = results.can_progress;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <Paper className="glass-surface rounded-3xl p-8 mb-6" elevation={0}>
        <Box className="text-center mb-6">
          <Typography variant="h4" component="h1" className="font-bold mb-4">
            Assessment Results
          </Typography>
          <Typography variant="h6" color="text.secondary" className="mb-2">
            {results.module_title}
          </Typography>

          {/* Score Display */}
          <Box className="my-6">
            <Typography variant="h2" className={`font-bold text-${scoreColor}-500 mb-2`}>
              {results.score_percent.toFixed(1)}%
            </Typography>
            <Typography variant="body1" color="text.secondary">
              {results.points_earned} / {results.points_possible} points
            </Typography>
            <LinearProgress
              variant="determinate"
              value={results.score_percent}
              color={scoreColor}
              className="mt-4 h-3 rounded-full"
            />
          </Box>

          {/* Statistics */}
          <Box className="grid grid-cols-2 md:grid-cols-4 gap-4 my-6">
            <Box className="text-center">
              <Typography variant="h6" className="font-bold">
                {results.attempted}
              </Typography>
              <Typography variant="caption" color="text.secondary">
                Attempted
              </Typography>
            </Box>
            <Box className="text-center">
              <Typography variant="h6" className="font-bold text-green-500">
                {results.correct}
              </Typography>
              <Typography variant="caption" color="text.secondary">
                Correct
              </Typography>
            </Box>
            <Box className="text-center">
              <Typography variant="h6" className="font-bold text-orange-500">
                {results.pending_review}
              </Typography>
              <Typography variant="caption" color="text.secondary">
                Pending Review
              </Typography>
            </Box>
            <Box className="text-center">
              <Typography variant="h6" className="font-bold">
                {results.attempt_count}
              </Typography>
              <Typography variant="caption" color="text.secondary">
                Attempts
              </Typography>
            </Box>
          </Box>

          {/* Best Score */}
          {results.best_score_percent && results.best_score_percent !== results.score_percent && (
            <Typography variant="body2" color="text.secondary" className="mb-4">
              Best score: {results.best_score_percent.toFixed(1)}%
            </Typography>
          )}

          {/* Progression Status */}
          {canProgress ? (
            <Alert severity="success" icon={<CheckCircleOutline />} className="mb-4">
              <Typography variant="body1">
                <strong>Congratulations!</strong> You've passed the assessment and can proceed to the next module.
              </Typography>
            </Alert>
          ) : (
            <Alert severity="warning" icon={<ErrorOutline />} className="mb-4">
              <Typography variant="body1">
                You need a score of at least 70% to proceed. {results.pending_review > 0 && 'Some answers are still pending review.'}
              </Typography>
            </Alert>
          )}

          {/* Action Buttons */}
          <Box className="flex gap-4 justify-center mt-6">
            <Button
              variant="outlined"
              onClick={() => navigate('/')}
            >
              Back to Home
            </Button>
            {canProgress ? (
              <Button
                variant="contained"
                onClick={() => {
                  const moduleId = window.location.pathname.split('/')[2];
                  navigate(`/modules/${moduleId}`);
                }}
              >
                Back to Module
              </Button>
            ) : (
              <Button
                variant="contained"
                onClick={onRetake}
              >
                Retake Assessment
              </Button>
            )}
          </Box>
        </Box>
      </Paper>

      {/* Detailed Results */}
      <Paper className="glass-surface rounded-3xl p-6" elevation={0}>
        <Typography variant="h6" className="font-semibold mb-4">
          Question Details
        </Typography>
        <Box className="space-y-4">
          {results.attempts.map((attempt, index) => (
            <QuestionResultItem key={attempt.attempt_id} attempt={attempt} questionNumber={index + 1} />
          ))}
        </Box>
      </Paper>
    </motion.div>
  );
};

interface QuestionResultItemProps {
  attempt: QuizAttempt;
  questionNumber: number;
}

const QuestionResultItem: React.FC<QuestionResultItemProps> = ({ attempt, questionNumber }) => {
  const isCorrect = attempt.is_correct === true;
  const isPending = attempt.review_status === ReviewStatus.NEEDS_REVIEW || 
                    attempt.review_status === ReviewStatus.PENDING;

  return (
    <motion.div
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay: questionNumber * 0.1 }}
    >
      <Box
        className={`
          p-4 rounded-xl border-2 mb-4
          ${isCorrect ? 'border-green-500 bg-green-50 dark:bg-green-900/20' : ''}
          ${!isCorrect && !isPending ? 'border-red-500 bg-red-50 dark:bg-red-900/20' : ''}
          ${isPending ? 'border-orange-500 bg-orange-50 dark:bg-orange-900/20' : ''}
          ${!isCorrect && !isPending && !isPending ? 'border-gray-200 dark:border-gray-700' : ''}
        `}
      >
        <Box className="flex items-start justify-between mb-2">
          <Typography variant="subtitle1" className="font-semibold">
            Question {questionNumber}: {attempt.question_text}
          </Typography>
          <Box className="ml-4">
            {isCorrect && <CheckCircle color="success" />}
            {!isCorrect && !isPending && <Cancel color="error" />}
            {isPending && <HourglassEmpty className="text-orange-500" />}
          </Box>
        </Box>

        <Typography variant="body2" className="mb-2">
          <strong>Your answer:</strong> {attempt.user_answer || 'No answer provided'}
        </Typography>

        {attempt.points_earned !== null && (
          <Typography variant="body2" className="mb-2">
            <strong>Points:</strong> {attempt.points_earned}
          </Typography>
        )}

        {attempt.feedback && (
          <Typography variant="body2" className="mt-2 text-blue-700 dark:text-blue-300">
            <strong>Feedback:</strong> {attempt.feedback}
          </Typography>
        )}

        {isPending && (
          <Typography variant="body2" className="mt-2 text-orange-700 dark:text-orange-300">
            <strong>Status:</strong> Awaiting instructor review
          </Typography>
        )}
      </Box>
    </motion.div>
  );
};

