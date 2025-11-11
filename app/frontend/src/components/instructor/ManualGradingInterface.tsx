/** Manual Grading Interface Component */
import React, { useState } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  Typography,
  Box,
  Card,
  CardContent,
  FormControlLabel,
  Checkbox,
  Alert,
  Divider,
} from '@mui/material';
import { gradingService, type GradingQueueItem, type GradeSubmission } from '../../services/gradingService';
import { useThemeMode } from '../../contexts/ThemeContext';

interface ManualGradingInterfaceProps {
  open: boolean;
  onClose: () => void;
  item: GradingQueueItem;
}

export const ManualGradingInterface: React.FC<ManualGradingInterfaceProps> = ({
  open,
  onClose,
  item,
}) => {
  const { mode } = useThemeMode();
  const [points, setPoints] = useState<number>(0);
  const [isCorrect, setIsCorrect] = useState<boolean>(false);
  const [feedback, setFeedback] = useState<string>('');
  const [partialCredit, setPartialCredit] = useState<boolean>(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async () => {
    try {
      setLoading(true);
      setError(null);

      const grade: GradeSubmission = {
        is_correct: isCorrect,
        points_earned: points,
        feedback: feedback || undefined,
        partial_credit: partialCredit,
      };

      await gradingService.gradeAttempt(item.attempt_id, grade);
      onClose();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to submit grade');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
      <DialogTitle>Grade Assessment</DialogTitle>
      <DialogContent>
        {error && (
          <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>
            <Typography variant="body2">{error}</Typography>
          </Alert>
        )}

        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
          {/* Student Info */}
          <Card className="glass-surface" sx={{ borderRadius: 2 }}>
            <CardContent>
              <Typography variant="subtitle2" sx={{ color: 'text.secondary', mb: 1 }}>
                Student
              </Typography>
              <Typography variant="body1" sx={{ fontWeight: 'bold', color: 'text.primary' }}>
                {item.user_name}
              </Typography>
              <Typography variant="body2" sx={{ color: 'text.secondary' }}>
                {item.user_email}
              </Typography>
            </CardContent>
          </Card>

          {/* Question Info */}
          <Card className="glass-surface" sx={{ borderRadius: 2 }}>
            <CardContent>
              <Typography variant="subtitle2" sx={{ color: 'text.secondary', mb: 1 }}>
                Module
              </Typography>
              <Typography variant="body1" sx={{ color: 'text.primary', mb: 2 }}>
                {item.module_title}
              </Typography>

              <Divider sx={{ my: 2 }} />

              <Typography variant="subtitle2" sx={{ color: 'text.secondary', mb: 1 }}>
                Question
              </Typography>
              <Typography variant="body1" sx={{ color: 'text.primary', mb: 2 }}>
                {item.question_text}
              </Typography>

              <Divider sx={{ my: 2 }} />

              <Typography variant="subtitle2" sx={{ color: 'text.secondary', mb: 1 }}>
                Correct Answer
              </Typography>
              <Typography variant="body1" sx={{ color: 'text.primary', mb: 2 }}>
                {item.correct_answer}
              </Typography>

              <Divider sx={{ my: 2 }} />

              <Typography variant="subtitle2" sx={{ color: 'text.secondary', mb: 1 }}>
                Student Answer
              </Typography>
              <Typography variant="body1" sx={{ color: 'text.primary' }}>
                {item.user_answer || 'No answer provided'}
              </Typography>
            </CardContent>
          </Card>

          {/* Grading Form */}
          <Box>
            <Typography variant="h6" sx={{ fontWeight: 'bold', color: 'text.primary', mb: 2 }}>
              Grading
            </Typography>

            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
              <FormControlLabel
                control={
                  <Checkbox
                    checked={isCorrect}
                    onChange={(e) => setIsCorrect(e.target.checked)}
                    sx={{ color: 'text.secondary' }}
                  />
                }
                label="Answer is correct"
                sx={{ color: 'text.primary' }}
              />

              <TextField
                label="Points Awarded"
                type="number"
                value={points}
                onChange={(e) => setPoints(parseInt(e.target.value) || 0)}
                inputProps={{ min: 0 }}
                fullWidth
                required
              />

              <FormControlLabel
                control={
                  <Checkbox
                    checked={partialCredit}
                    onChange={(e) => setPartialCredit(e.target.checked)}
                    sx={{ color: 'text.secondary' }}
                  />
                }
                label="Award partial credit"
                sx={{ color: 'text.primary' }}
              />

              <TextField
                label="Feedback (optional)"
                value={feedback}
                onChange={(e) => setFeedback(e.target.value)}
                multiline
                rows={4}
                fullWidth
                placeholder="Provide feedback to help the student improve..."
              />
            </Box>
          </Box>
        </Box>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose} sx={{ color: 'text.secondary' }}>
          Cancel
        </Button>
        <Button
          onClick={handleSubmit}
          variant="contained"
          disabled={loading}
          sx={{ backgroundColor: '#1976d2', color: 'text.primary' }}
        >
          Submit Grade
        </Button>
      </DialogActions>
    </Dialog>
  );
};

