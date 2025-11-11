/** Grading Queue Component */
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Card,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Button,
  Chip,
  Alert,
  IconButton,
} from '@mui/material';
import {
  Grade,
  Visibility,
} from '@mui/icons-material';
import { gradingService, type GradingQueueItem } from '../../services/gradingService';
import { useThemeMode } from '../../contexts/ThemeContext';
import { ManualGradingInterface } from './ManualGradingInterface';

interface GradingQueueProps {
  queue: GradingQueueItem[];
  onRefresh: () => void;
}

export const GradingQueue: React.FC<GradingQueueProps> = ({ queue, onRefresh }) => {
  const { mode } = useThemeMode();
  const navigate = useNavigate();
  const [selectedItem, setSelectedItem] = useState<GradingQueueItem | null>(null);
  const [openGradingDialog, setOpenGradingDialog] = useState(false);

  const handleGrade = (item: GradingQueueItem) => {
    setSelectedItem(item);
    setOpenGradingDialog(true);
  };

  const handleCloseGradingDialog = () => {
    setOpenGradingDialog(false);
    setSelectedItem(null);
    onRefresh();
  };

  if (queue.length === 0) {
    return (
      <Card className="glass-surface" sx={{ borderRadius: 2, p: 4, textAlign: 'center' }}>
        <Typography variant="body1" sx={{ color: 'text.secondary', mb: 2 }}>
          No items in grading queue. All assessments are auto-graded!
        </Typography>
        <Typography variant="body2" sx={{ color: 'text.secondary' }}>
          Note: Currently all questions are multiple-choice and auto-gradable.
          This interface is ready for when short-answer questions are added.
        </Typography>
      </Card>
    );
  }

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h6" sx={{ fontWeight: 'bold', color: 'text.primary' }}>
          Pending Grading ({queue.length})
        </Typography>
      </Box>

      <TableContainer component={Card} className="glass-surface" sx={{ borderRadius: 2 }}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell sx={{ fontWeight: 'bold', color: 'text.primary' }}>Student</TableCell>
              <TableCell sx={{ fontWeight: 'bold', color: 'text.primary' }}>Module</TableCell>
              <TableCell sx={{ fontWeight: 'bold', color: 'text.primary' }}>Question</TableCell>
              <TableCell sx={{ fontWeight: 'bold', color: 'text.primary' }}>Type</TableCell>
              <TableCell sx={{ fontWeight: 'bold', color: 'text.primary' }}>Submitted</TableCell>
              <TableCell sx={{ fontWeight: 'bold', color: 'text.primary' }}>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {queue.map((item) => (
              <TableRow key={item.attempt_id}>
                <TableCell sx={{ color: 'text.primary' }}>
                  <Box>
                    <Typography variant="body2" sx={{ fontWeight: 'bold' }}>
                      {item.user_name}
                    </Typography>
                    <Typography variant="caption" sx={{ color: 'text.secondary' }}>
                      {item.user_email}
                    </Typography>
                  </Box>
                </TableCell>
                <TableCell sx={{ color: 'text.secondary' }}>{item.module_title}</TableCell>
                <TableCell sx={{ color: 'text.secondary', maxWidth: 300 }}>
                  <Typography
                    variant="body2"
                    sx={{
                      overflow: 'hidden',
                      textOverflow: 'ellipsis',
                      whiteSpace: 'nowrap',
                    }}
                  >
                    {item.question_text}
                  </Typography>
                </TableCell>
                <TableCell>
                  <Chip
                    label={item.question_type}
                    size="small"
                    color="primary"
                    variant="outlined"
                  />
                </TableCell>
                <TableCell sx={{ color: 'text.secondary' }}>
                  {new Date(item.attempted_at).toLocaleDateString()}
                </TableCell>
                <TableCell>
                  <Box sx={{ display: 'flex', gap: 1 }}>
                    <Button
                      size="small"
                      variant="contained"
                      startIcon={<Grade />}
                      onClick={() => handleGrade(item)}
                      sx={{
                        backgroundColor: '#1976d2',
                        color: 'text.primary',
                      }}
                    >
                      Grade
                    </Button>
                    <IconButton
                      size="small"
                      onClick={() => navigate(`/modules/${item.module_id}`)}
                      sx={{ color: 'text.secondary' }}
                    >
                      <Visibility fontSize="small" />
                    </IconButton>
                  </Box>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      {selectedItem && (
        <ManualGradingInterface
          open={openGradingDialog}
          onClose={handleCloseGradingDialog}
          item={selectedItem}
        />
      )}
    </Box>
  );
};

