/** Modules list page - displays all available modules */
import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Box, Button, Typography, Paper, CircularProgress, Alert, Card, CardContent, Grid, Container } from '@mui/material';
import { School } from '@mui/icons-material';
import { motion } from 'framer-motion';
import { useQuery } from '@tanstack/react-query';
import { useThemeMode } from '../contexts/ThemeContext';
import { moduleService } from '../services/moduleService';
import type { Module } from '../types/module';

export const ModulesListPage: React.FC = () => {
  const navigate = useNavigate();
  const { mode } = useThemeMode();
  const backgroundColor = mode === 'light' ? '#f8f9fa' : '#0a0e27';

  // Fetch all modules
  const {
    data: modulesData,
    isLoading,
    error,
  } = useQuery({
    queryKey: ['modules'],
    queryFn: () => moduleService.getModules(),
  });

  const handleModuleClick = (moduleId: number) => {
    navigate(`/modules/${moduleId}`);
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
          Failed to load modules. Please try again.
        </Alert>
      </Box>
    );
  }

  const modules = modulesData?.modules || [];

  return (
    <Box sx={{ minHeight: '100vh', backgroundColor, py: 4 }}>
      <Container maxWidth="lg">
        {/* Header */}
        <Box sx={{ mb: 4, textAlign: 'center' }}>
          <Typography variant="h3" sx={{ fontWeight: 'bold', color: 'text.primary', mb: 2 }}>
            All Modules
          </Typography>
          <Typography variant="body1" sx={{ color: mode === 'light' ? 'text.secondary' : 'rgba(255, 255, 255, 0.8)' }}>
            Explore {modules.length} comprehensive modules on blockchain and cryptocurrency
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
                style={{ cursor: 'pointer' }}
                onClick={() => handleModuleClick(module.id)}
              >
                <Card
                  className="glass-surface"
                  sx={{
                    borderRadius: 3,
                    height: '100%',
                  }}
                >
                  <CardContent sx={{ p: 3 }}>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', mb: 2 }}>
                      <Box>
                        <Typography variant="caption" sx={{ color: mode === 'light' ? 'text.secondary' : 'rgba(255, 255, 255, 0.7)', display: 'block', mb: 0.5 }}>
                          Module {module.order_index}
                        </Typography>
                        <Typography variant="h6" sx={{ fontWeight: 'bold', color: 'text.primary', mb: 1 }}>
                          {module.title}
                        </Typography>
                        {module.description && (
                          <Typography variant="body2" sx={{ color: mode === 'light' ? 'text.secondary' : 'rgba(255, 255, 255, 0.8)', mb: 2 }}>
                            {module.description}
                          </Typography>
                        )}
                        <Typography variant="caption" sx={{ color: mode === 'light' ? 'text.secondary' : 'rgba(255, 255, 255, 0.6)', display: 'block' }}>
                          {module.track} • {module.duration_hours} hours
                        </Typography>
                      </Box>
                    </Box>
                    <Button
                      size="small"
                      variant="outlined"
                      startIcon={<School />}
                      onClick={(e) => {
                        e.stopPropagation();
                        handleModuleClick(module.id);
                      }}
                      sx={{
                        borderColor: mode === 'light' ? 'divider' : 'rgba(255, 255, 255, 0.5)',
                        color: 'text.primary',
                        '&:hover': {
                          borderColor: mode === 'light' ? 'text.primary' : '#ffffff',
                          backgroundColor: mode === 'light' ? 'rgba(0,0,0,0.04)' : 'rgba(255, 255, 255, 0.1)',
                        },
                      }}
                    >
                      View Module
                    </Button>
                  </CardContent>
                </Card>
              </motion.div>
            </Grid>
          ))}
        </Grid>

        {modules.length === 0 && (
          <Paper
            className="glass-surface"
            sx={{
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
