/** Assessments list page - displays all modules with their assessments */
import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Box, Button, Typography, Paper, CircularProgress, Alert, Card, CardContent, Grid, Container } from '@mui/material';
import { Assessment, School } from '@mui/icons-material';
import { motion } from 'framer-motion';
import { useQuery } from '@tanstack/react-query';
import { moduleService } from '../services/moduleService';
import type { Module } from '../types/module';

export const AssessmentsListPage: React.FC = () => {
  const navigate = useNavigate();

  // Fetch all modules
  const {
    data: modulesData,
    isLoading,
    error,
  } = useQuery({
    queryKey: ['modules'],
    queryFn: () => moduleService.getModules(),
  });

  const handleAssessmentClick = (moduleId: number) => {
    navigate(`/modules/${moduleId}/assessments`);
  };

  const handleModuleClick = (moduleId: number) => {
    navigate(`/modules/${moduleId}`);
  };

  if (isLoading) {
    return (
      <Box sx={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', backgroundColor: '#0a0e27' }}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box sx={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', p: 4, backgroundColor: '#0a0e27' }}>
        <Alert severity="error">
          Failed to load modules. Please try again.
        </Alert>
      </Box>
    );
  }

  const modules = modulesData?.modules || [];

  return (
    <Box sx={{ minHeight: '100vh', backgroundColor: '#0a0e27', py: 4 }}>
      <Container maxWidth="lg">
        {/* Header */}
        <Box sx={{ mb: 4, textAlign: 'center' }}>
          <Typography variant="h3" sx={{ fontWeight: 'bold', color: '#ffffff', mb: 2 }}>
            All Assessments
          </Typography>
          <Typography variant="body1" sx={{ color: 'rgba(255, 255, 255, 0.8)' }}>
            Access assessments for all {modules.length} modules. Each module contains 10 comprehensive questions.
          </Typography>
        </Box>

        {/* Modules Grid */}
        <Grid container spacing={3}>
          {modules.map((module: Module, index: number) => (
            <Grid size={{ xs: 12, sm: 6, md: 4 }} key={module.id}>
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3, delay: index * 0.1 }}
                whileHover={{ scale: 1.02 }}
              >
                <Card
                  sx={{
                    backgroundColor: '#ffffff',
                    borderRadius: 3,
                    height: '100%',
                    boxShadow: '0 2px 10px rgba(0, 0, 0, 0.2)',
                  }}
                >
                  <CardContent sx={{ p: 3 }}>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', mb: 2 }}>
                      <Box>
                        <Typography variant="caption" sx={{ color: '#666666', display: 'block', mb: 0.5 }}>
                          Module {module.order_index}
                        </Typography>
                        <Typography variant="h6" sx={{ fontWeight: 'bold', color: '#1a1a1a', mb: 1 }}>
                          {module.title}
                        </Typography>
                        {module.description && (
                          <Typography variant="body2" sx={{ color: '#666666', mb: 2 }}>
                            {module.description}
                          </Typography>
                        )}
                        <Typography variant="caption" sx={{ color: '#999999', display: 'block' }}>
                          {module.track} • {module.duration_hours} hours
                        </Typography>
                      </Box>
                    </Box>
                    <Box sx={{ display: 'flex', gap: 1, mt: 2 }}>
                      <Button
                        size="small"
                        variant="contained"
                        startIcon={<Assessment />}
                        onClick={() => handleAssessmentClick(module.id)}
                        fullWidth
                        sx={{
                          backgroundColor: '#1976d2',
                          '&:hover': {
                            backgroundColor: '#1565c0',
                          },
                        }}
                      >
                        Take Assessment
                      </Button>
                      <Button
                        size="small"
                        variant="outlined"
                        startIcon={<School />}
                        onClick={() => handleModuleClick(module.id)}
                        sx={{
                          borderColor: '#999999',
                          color: '#1a1a1a',
                          '&:hover': {
                            borderColor: '#666666',
                            backgroundColor: '#f5f5f5',
                          },
                        }}
                      >
                        View Module
                      </Button>
                    </Box>
                  </CardContent>
                </Card>
              </motion.div>
            </Grid>
          ))}
        </Grid>

        {modules.length === 0 && (
          <Paper
            sx={{
              backgroundColor: '#ffffff',
              borderRadius: 3,
              p: 3,
              mt: 4,
            }}
          >
            <Alert severity="info">No modules available.</Alert>
          </Paper>
        )}
      </Container>
    </Box>
  );
};
