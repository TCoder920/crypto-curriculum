/** Question card component wrapper */
import React from 'react';
import { Box, Typography, Paper } from '@mui/material';
import { motion } from 'framer-motion';
import type { Assessment } from '../../types/assessment';

interface QuestionCardProps {
  assessment: Assessment;
  questionNumber: number;
  totalQuestions: number;
  children: React.ReactNode;
}

export const QuestionCard: React.FC<QuestionCardProps> = ({
  assessment,
  questionNumber,
  totalQuestions,
  children,
}) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      <Paper
        className="glass-surface rounded-3xl p-6 mb-6"
        elevation={0}
      >
        <Box className="mb-4">
          <Typography variant="caption" color="text.secondary" className="mb-2">
            Question {questionNumber} of {totalQuestions} • {assessment.points} points
          </Typography>
          <Typography variant="h6" component="h2" className="font-semibold mb-4">
            {assessment.question_text}
          </Typography>
        </Box>
        {children}
      </Paper>
    </motion.div>
  );
};

