/** True/False question component */
import React from 'react';
import { Box, Button, Typography } from '@mui/material';
import { CheckCircle, Cancel } from '@mui/icons-material';
import { motion } from 'framer-motion';
import type { Assessment, AssessmentSubmitResponse } from '../../types/assessment';

interface TrueFalseProps {
  assessment: Assessment;
  selectedAnswer: string | null;
  onAnswerSelect: (answer: string) => void;
  result?: AssessmentSubmitResponse | null;
  disabled?: boolean;
}

export const TrueFalse: React.FC<TrueFalseProps> = ({
  assessment,
  selectedAnswer,
  onAnswerSelect,
  result,
  disabled = false,
}) => {
  const showResult = result !== null && result !== undefined;
  const correctAnswer = result?.correct_answer?.toUpperCase();

  const getButtonProps = (value: string) => {
    const isSelected = selectedAnswer?.toUpperCase() === value;
    const isCorrect = correctAnswer === value;
    
    if (!showResult) {
      return {
        variant: isSelected ? 'contained' : 'outlined' as const,
        color: 'primary' as const,
      };
    }
    
    if (isCorrect) {
      return {
        variant: 'contained' as const,
        color: 'success' as const,
      };
    }
    
    if (isSelected && !isCorrect) {
      return {
        variant: 'contained' as const,
        color: 'error' as const,
      };
    }
    
    return {
      variant: 'outlined' as const,
      color: 'default' as const,
    };
  };

  return (
    <Box className="flex gap-4">
      {['True', 'False'].map((option) => {
        const isSelected = selectedAnswer?.toUpperCase() === option.toUpperCase();
        const isCorrect = correctAnswer === option.toUpperCase();
        const buttonProps = getButtonProps(option);

        return (
          <motion.div
            key={option}
            whileHover={!disabled ? { scale: 1.05 } : {}}
            whileTap={!disabled ? { scale: 0.95 } : {}}
            className="flex-1"
          >
            <Button
              {...buttonProps}
              fullWidth
              size="large"
              onClick={() => !disabled && onAnswerSelect(option)}
              disabled={disabled}
              className={`
                h-20 text-lg font-semibold rounded-xl
                ${showResult && isCorrect ? 'bg-green-500 hover:bg-green-600' : ''}
                ${showResult && isSelected && !isCorrect ? 'bg-red-500 hover:bg-red-600' : ''}
              `}
              startIcon={
                showResult && (
                  <>
                    {isCorrect && <CheckCircle />}
                    {isSelected && !isCorrect && <Cancel />}
                  </>
                )
              }
            >
              {option}
            </Button>
          </motion.div>
        );
      })}

      {result && result.explanation && (
        <motion.div
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: 'auto' }}
          className="mt-4 p-4 rounded-xl bg-blue-50 dark:bg-blue-900/20 w-full"
        >
          <Typography variant="body2" className="text-blue-900 dark:text-blue-100">
            <strong>Explanation:</strong> {result.explanation}
          </Typography>
        </motion.div>
      )}
    </Box>
  );
};

