/** Multiple choice question component */
import React from 'react';
import { Box, Typography, Radio, RadioGroup, FormControlLabel, FormControl } from '@mui/material';
import { CheckCircle, Cancel } from '@mui/icons-material';
import { motion } from 'framer-motion';
import type { Assessment, AssessmentSubmitResponse } from '../../types/assessment';

interface MultipleChoiceProps {
  assessment: Assessment;
  selectedAnswer: string | null;
  onAnswerSelect: (answer: string) => void;
  result?: AssessmentSubmitResponse | null;
  disabled?: boolean;
}

export const MultipleChoice: React.FC<MultipleChoiceProps> = ({
  assessment,
  selectedAnswer,
  onAnswerSelect,
  result,
  disabled = false,
}) => {
  const options = assessment.options || {};
  const optionKeys = Object.keys(options).sort();

  return (
    <FormControl component="fieldset" fullWidth disabled={disabled}>
      <RadioGroup
        value={selectedAnswer || ''}
        onChange={(e) => !disabled && onAnswerSelect(e.target.value)}
      >
        {optionKeys.map((key) => {
          const isSelected = selectedAnswer === key;
          const isCorrect = result?.correct_answer === key;
          const showResult = result !== null && result !== undefined;

          return (
            <motion.div
              key={key}
              whileHover={!disabled ? { scale: 1.02 } : {}}
              whileTap={!disabled ? { scale: 0.98 } : {}}
            >
              <FormControlLabel
                value={key}
                control={<Radio />}
                label={
                  <Box className="flex items-center justify-between w-full">
                    <Typography variant="body1">
                      <strong>{key}.</strong> {options[key]}
                    </Typography>
                    {showResult && (
                      <Box className="ml-4">
                        {isCorrect && (
                          <CheckCircle color="success" className="text-green-500" />
                        )}
                        {isSelected && !isCorrect && (
                          <Cancel color="error" className="text-red-500" />
                        )}
                      </Box>
                    )}
                  </Box>
                }
                className={`
                  mb-3 p-3 rounded-xl border-2 transition-all
                  ${showResult && isCorrect ? 'border-green-500 bg-green-50 dark:bg-green-900/20' : ''}
                  ${showResult && isSelected && !isCorrect ? 'border-red-500 bg-red-50 dark:bg-red-900/20' : ''}
                  ${!showResult ? 'border-gray-200 dark:border-gray-700 hover:border-primary' : ''}
                `}
                disabled={disabled}
              />
            </motion.div>
          );
        })}
      </RadioGroup>

      {result && result.explanation && (
        <motion.div
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: 'auto' }}
          className="mt-4 p-4 rounded-xl bg-blue-50 dark:bg-blue-900/20"
        >
          <Typography variant="body2" className="text-blue-900 dark:text-blue-100">
            <strong>Explanation:</strong> {result.explanation}
          </Typography>
        </motion.div>
      )}
    </FormControl>
  );
};

