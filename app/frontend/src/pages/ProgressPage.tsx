/** Progress page - shows overall and per-module assessment progress */
import React from 'react';
import { Box, Container, Typography, Alert, Card, CardContent, Grid, LinearProgress } from '@mui/material';
import { useThemeMode } from '../contexts/ThemeContext';
import { useQuery } from '@tanstack/react-query';
import { moduleService } from '../services/moduleService';
import { assessmentService } from '../services/assessmentService';
import type { Module } from '../types/module';

export const ProgressPage: React.FC = () => {
  const { mode } = useThemeMode();
  const backgroundColor = mode === 'light' ? '#f8f9fa' : '#0a0e27';

  const modulesQuery = useQuery({
    queryKey: ['modules'],
    queryFn: () => moduleService.getModules(),
  });

  const modules: Module[] = modulesQuery.data?.modules || [];

  // Fetch results per module
  const resultsQueries = useQuery({
    queryKey: ['progress-results', modules.map(m => m.id)],
    queryFn: async () => {
      const pairs = await Promise.all(
        modules.map(async (m) => {
          try {
            const r = await assessmentService.getModuleResults(m.id);
            return [m.id, r] as const;
          } catch {
            return [m.id, null] as const;
          }
        })
      );
      return Object.fromEntries(pairs) as Record<number, any>;
    },
    enabled: modules.length > 0,
  });

  const resultsByModule = resultsQueries.data || {};
  const completedCount = modules.filter(
    (m) => resultsByModule[m.id]?.can_progress === true
  ).length;
  const completionPercent =
    modules.length > 0 ? Math.round((completedCount / modules.length) * 100) : 0;

  return (
    <Box sx={{ minHeight: '100vh', backgroundColor, py: 4 }}>
      <Container maxWidth="lg">
        <Typography variant="h4" sx={{ fontWeight: 'bold', color: 'text.primary', mb: 2 }}>
          Your Progress
        </Typography>

        <Card className="glass-surface" sx={{ mb: 3, borderRadius: 3 }}>
          <CardContent>
            <Typography variant="body2" sx={{ color: mode === 'light' ? 'text.secondary' : 'rgba(255,255,255,0.8)', mb: 1 }}>
              Overall completion
            </Typography>
            <LinearProgress
              variant="determinate"
              value={completionPercent}
              sx={{ height: 10, borderRadius: 1 }}
            />
            <Typography variant="caption" sx={{ color: 'text.secondary' }}>
              {completedCount} of {modules.length} modules complete ({completionPercent}%)
            </Typography>
          </CardContent>
        </Card>

        {modulesQuery.isLoading && (
          <Alert severity="info">Loading modules…</Alert>
        )}
        {modulesQuery.error && (
          <Alert severity="error">Failed to load modules.</Alert>
        )}

        <Grid container spacing={2}>
          {modules.map((m) => {
            const r = resultsByModule[m.id];
            const total = r?.total_questions || 0;
            const attempted = r?.attempted || 0;
            const correct = r?.correct || 0;
            const canProgress = r?.can_progress === true;
            const pct = total > 0 ? Math.round((correct / total) * 100) : 0;
            return (
              <Grid size={{ xs: 12, sm: 6, md: 4 }} key={m.id}>
                <Card className="glass-surface" sx={{ borderRadius: 3, height: '100%' }}>
                  <CardContent>
                    <Typography variant="h6" sx={{ color: 'text.primary', fontWeight: 'bold', mb: 1 }}>
                      {m.title}
                    </Typography>
                    <Typography variant="caption" sx={{ color: mode === 'light' ? 'text.secondary' : 'rgba(255,255,255,0.7)' }}>
                      {canProgress ? 'Completed' : 'In progress'}
                    </Typography>
                    <Box sx={{ mt: 2 }}>
                      <LinearProgress variant="determinate" value={pct} sx={{ height: 8, borderRadius: 1 }} />
                      <Typography variant="caption" sx={{ color: 'text.secondary' }}>
                        {correct}/{total} correct ({pct}%)
                      </Typography>
                    </Box>
                    {attempted > 0 && (
                      <Typography variant="caption" sx={{ color: 'text.secondary', display: 'block', mt: 1 }}>
                        Attempts: {r?.attempt_count ?? attempted}
                      </Typography>
                    )}
                  </CardContent>
                </Card>
              </Grid>
            );
          })}
        </Grid>
      </Container>
    </Box>
  );
};


