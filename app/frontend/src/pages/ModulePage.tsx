/** Module page - displays lessons and assessment link */
import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Box, Button, Typography, Paper, CircularProgress, Alert, Divider, Container } from '@mui/material';
import { ArrowBack, ArrowForward, Assessment, CheckCircle } from '@mui/icons-material';
import { motion } from 'framer-motion';
import { useQuery } from '@tanstack/react-query';
import ReactMarkdown from 'react-markdown';
import { useThemeMode } from '../contexts/ThemeContext';
import { moduleService } from '../services/moduleService';
import { assessmentService } from '../services/assessmentService';
import type { Lesson } from '../types/module';

export const ModulePage: React.FC = () => {
  const { moduleId } = useParams<{ moduleId: string }>();
  const navigate = useNavigate();
  const { mode } = useThemeMode();
  const backgroundColor = mode === 'light' ? '#f8f9fa' : '#0a0e27';
  const [currentLessonIndex, setCurrentLessonIndex] = useState(0);

  // Fetch module details
  const {
    data: moduleData,
    isLoading,
    error,
  } = useQuery({
    queryKey: ['module', moduleId],
    queryFn: () => moduleService.getModuleDetail(Number(moduleId)),
    enabled: !!moduleId,
  });

  // Check if user has completed assessment
  const {
    data: assessmentResults,
    refetch: refetchResults,
  } = useQuery({
    queryKey: ['assessment-results', moduleId],
    queryFn: () => assessmentService.getModuleResults(Number(moduleId)),
    enabled: !!moduleId && !!moduleData?.has_assessment,
  });

  // Refetch results when returning from assessment
  React.useEffect(() => {
    if (moduleData?.has_assessment) {
      refetchResults();
    }
  }, [moduleData?.has_assessment, refetchResults]);

  const lessons = moduleData?.lessons || [];
  const currentLesson: Lesson | undefined = lessons[currentLessonIndex];
  const hasPassedAssessment = assessmentResults?.can_progress === true;

  const handleNextLesson = () => {
    if (currentLessonIndex < lessons.length - 1) {
      setCurrentLessonIndex((prev) => prev + 1);
    }
  };

  const handlePreviousLesson = () => {
    if (currentLessonIndex > 0) {
      setCurrentLessonIndex((prev) => prev - 1);
    }
  };

  const handleTakeAssessment = () => {
    navigate(`/modules/${moduleId}/assessments`);
  };

  if (isLoading) {
    return (
      <Box sx={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', backgroundColor }}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box sx={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', p: 4, backgroundColor }}>
        <Alert severity="error">
          Failed to load module. Please try again.
        </Alert>
      </Box>
    );
  }

  if (!moduleData) {
    return (
      <Box sx={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', p: 4, backgroundColor }}>
        <Alert severity="info">Module not found.</Alert>
      </Box>
    );
  }

  return (
    <Box sx={{ minHeight: '100vh', backgroundColor, py: 4 }}>
      <Container maxWidth="lg">
        {/* Header */}
        <Box sx={{ mb: 4 }}>
          <Typography variant="h4" sx={{ fontWeight: 'bold', color: 'text.primary', mb: 2 }}>
            {moduleData.title}
          </Typography>
          {moduleData.description && (
            <Typography variant="body1" sx={{ color: mode === 'light' ? 'text.secondary' : 'rgba(255, 255, 255, 0.8)', mb: 1 }}>
              {moduleData.description}
            </Typography>
          )}
          <Typography variant="body2" sx={{ color: mode === 'light' ? 'text.secondary' : 'rgba(255, 255, 255, 0.6)' }}>
            Track: {moduleData.track} • Duration: {moduleData.duration_hours} hours
          </Typography>
        </Box>

        {/* Lesson Content */}
        {currentLesson ? (
          <motion.div
            key={currentLesson.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
          >
            <Paper
              className="glass-surface"
              sx={{
                borderRadius: 3,
                p: 4,
                mb: 4,
              }}
            >
              <Box sx={{ mb: 3 }}>
                <Typography variant="caption" sx={{ color: mode === 'light' ? 'text.secondary' : 'rgba(255, 255, 255, 0.7)', display: 'block', mb: 2 }}>
                  Lesson {currentLessonIndex + 1} of {lessons.length}
                  {currentLesson.estimated_minutes && ` • ${currentLesson.estimated_minutes} minutes`}
                </Typography>
                <Typography variant="h5" sx={{ fontWeight: 'semibold', color: 'text.primary', mb: 3 }}>
                  {currentLesson.title}
                </Typography>
              </Box>

              <Divider sx={{ my: 3, borderColor: mode === 'light' ? 'rgba(0,0,0,0.1)' : 'rgba(255, 255, 255, 0.2)' }} />

              <Box sx={{ color: 'text.primary' }}>
                <ReactMarkdown>{currentLesson.content}</ReactMarkdown>
              </Box>
            </Paper>

            {/* Lesson Navigation */}
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
              <Button
                startIcon={<ArrowBack />}
                onClick={handlePreviousLesson}
                disabled={currentLessonIndex === 0}
                variant="outlined"
                sx={{
                  borderColor: mode === 'light' ? 'divider' : 'rgba(255, 255, 255, 0.5)',
                  color: 'text.primary',
                  '&:hover': {
                    borderColor: mode === 'light' ? 'text.primary' : '#ffffff',
                    backgroundColor: mode === 'light' ? 'rgba(0,0,0,0.04)' : 'rgba(255, 255, 255, 0.1)',
                  },
                }}
              >
                Previous Lesson
              </Button>

              {currentLessonIndex < lessons.length - 1 ? (
                <Button
                  endIcon={<ArrowForward />}
                  onClick={handleNextLesson}
                  variant="contained"
                  sx={{
                    backgroundColor: '#1976d2',
                    '&:hover': {
                      backgroundColor: '#1565c0',
                    },
                  }}
                >
                  Next Lesson
                </Button>
              ) : (
                <Button
                  endIcon={<ArrowForward />}
                  onClick={handleNextLesson}
                  disabled
                  variant="outlined"
                  sx={{
                  borderColor: mode === 'light' ? 'divider' : 'rgba(255, 255, 255, 0.3)',
                  color: mode === 'light' ? 'text.disabled' : 'rgba(255, 255, 255, 0.5)',
                  }}
                >
                  Last Lesson
                </Button>
              )}
            </Box>
          </motion.div>
        ) : (
          <Paper
            className="glass-surface"
            sx={{
              borderRadius: 3,
              p: 3,
              mb: 4,
            }}
          >
            <Alert severity="info">No lessons available for this module.</Alert>
          </Paper>
        )}

        {/* Assessment Section - Always visible if module has assessments */}
        {moduleData.has_assessment && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: 0.2 }}
          >
            <Paper
              className="glass-surface"
              sx={{
                borderRadius: 3,
                p: 4,
                textAlign: 'center',
              }}
            >
              {hasPassedAssessment ? (
                <>
                  <CheckCircle sx={{ fontSize: 64, color: 'success.main', mb: 2 }} />
                  <Typography variant="h5" sx={{ fontWeight: 'bold', color: 'text.primary', mb: 2 }}>
                    Assessment Complete!
                  </Typography>
                  <Typography variant="body1" sx={{ color: mode === 'light' ? 'text.secondary' : 'rgba(255, 255, 255, 0.8)', mb: 4 }}>
                    You've successfully completed this module with a score of {assessmentResults?.score_percent.toFixed(1)}%.
                  </Typography>
                  <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center' }}>
                    <Button
                      variant="outlined"
                      onClick={() => navigate('/modules')}
                      sx={{
                        borderColor: mode === 'light' ? 'divider' : 'rgba(255, 255, 255, 0.5)',
                        color: 'text.primary',
                        '&:hover': {
                          borderColor: mode === 'light' ? 'text.primary' : '#ffffff',
                          backgroundColor: mode === 'light' ? 'rgba(0,0,0,0.04)' : 'rgba(255, 255, 255, 0.1)',
                        },
                      }}
                    >
                      Browse Modules
                    </Button>
                    <Button
                      variant="contained"
                      startIcon={<Assessment />}
                      onClick={handleTakeAssessment}
                      sx={{
                        backgroundColor: '#1976d2',
                        '&:hover': {
                          backgroundColor: '#1565c0',
                        },
                      }}
                    >
                      Retake Assessment
                    </Button>
                  </Box>
                </>
              ) : (
                <>
                  <Assessment sx={{ fontSize: 64, color: '#1976d2', mb: 2 }} />
                  <Typography variant="h5" sx={{ fontWeight: 'bold', color: 'text.primary', mb: 2 }}>
                    Module Assessment
                  </Typography>
                  <Typography variant="body1" sx={{ color: mode === 'light' ? 'text.secondary' : 'rgba(255, 255, 255, 0.8)', mb: 4 }}>
                    Test your knowledge with 10 comprehensive questions. You can take the assessment at any time.
                  </Typography>
                  <Button
                    variant="contained"
                    size="large"
                    startIcon={<Assessment />}
                    onClick={handleTakeAssessment}
                    sx={{
                      backgroundColor: '#1976d2',
                      '&:hover': {
                        backgroundColor: '#1565c0',
                      },
                    }}
                  >
                    Take Assessment
                  </Button>
                </>
              )}
            </Paper>
          </motion.div>
        )}
      </Container>
    </Box>
  );
};
