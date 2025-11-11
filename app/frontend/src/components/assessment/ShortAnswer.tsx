/** Short answer question component */
import React from 'react';
import { Box, TextField, Typography, Alert } from '@mui/material';
import { CheckCircle, HourglassEmpty } from '@mui/icons-material';
import { motion } from 'framer-motion';
import type { Assessment, AssessmentSubmitResponse } from '../../types/assessment';
import { ReviewStatus } from '../../types/assessment';

interface ShortAnswerProps {
  assessment: Assessment;
  answer: string;
  onAnswerChange: (answer: string) => void;
  result?: AssessmentSubmitResponse | null;
  disabled?: boolean;
}

export const ShortAnswer: React.FC<ShortAnswerProps> = ({
  assessment,
  answer,
  onAnswerChange,
  result,
  disabled = false,
}) => {
  const showResult = result !== null && result !== undefined;
  const isPending = result?.review_status === ReviewStatus.NEEDS_REVIEW || 
                    result?.review_status === ReviewStatus.PENDING;

  return (
    <Box>
      <TextField
        fullWidth
        multiline
        rows={4}
        value={answer}
        onChange={(e) => !disabled && onAnswerChange(e.target.value)}
        placeholder="Type your answer here..."
        disabled={disabled}
        className="mb-4"
      />

      {showResult && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
        >
          {isPending ? (
            <Alert
              icon={<HourglassEmpty />}
              severity="info"
              className="mb-4"
            >
              <Typography variant="body2">
                Your answer has been submitted and is awaiting instructor review.
              </Typography>
            </Alert>
          ) : result.is_correct !== null ? (
            <Alert
              icon={<CheckCircle />}
              severity={result.is_correct ? 'success' : 'warning'}
              className="mb-4"
            >
              <Typography variant="body2" className="mb-2">
                <strong>Status:</strong> {result.is_correct ? 'Correct' : 'Needs improvement'}
              </Typography>
              {result.points_earned !== null && (
                <Typography variant="body2">
                  <strong>Points earned:</strong> {result.points_earned} / {assessment.points}
                </Typography>
              )}
              {result.explanation && (
                <Typography variant="body2" className="mt-2">
                  <strong>Explanation:</strong> {result.explanation}
                </Typography>
              )}
            </Alert>
          ) : null}
        </motion.div>
      )}
    </Box>
  );
};

