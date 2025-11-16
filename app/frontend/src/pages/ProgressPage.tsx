/** Progress page - shows overall and per-module assessment progress */
import React from 'react';
import { Box, Container, Typography, Alert, Card, CardContent, Grid, LinearProgress } from '@mui/material';
import { useThemeMode } from '../contexts/ThemeContext';
import { useQuery } from '@tanstack/react-query';
import { moduleService } from '../services/moduleService';
import { assessmentService } from '../services/assessmentService';
import { achievementService } from '../services/achievementService';
import { AchievementBadge } from '../components/achievement/AchievementBadge';
import type { Module } from '../types/module';
import { ProgressStatus, type ModuleResultsResponse } from '../types/assessment';

export const ProgressPage: React.FC = () => {
  const { mode } = useThemeMode();
  const backgroundColor = mode === 'light' ? '#f8f9fa' : '#0a0e27';

  const modulesQuery = useQuery({
    queryKey: ['modules'],
    queryFn: () => moduleService.getModules(),
  });

  const modules: Module[] = modulesQuery.data?.modules || [];

  // Fetch achievements to show on completed modules
  const achievementsQuery = useQuery({
    queryKey: ['achievements'],
    queryFn: () => achievementService.getAchievements(),
  });

  const achievements = achievementsQuery.data || [];

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

  const moduleResults: ModuleResultsResponse[] = modules
    .map((m) => resultsByModule[m.id])
    .filter((result): result is ModuleResultsResponse => Boolean(result));

  const completedCount = moduleResults.filter(
    (result) => result.progress_status === ProgressStatus.COMPLETED
  ).length;

  const overallCompletionPercent = modules.length
    ? Math.round(
        modules.reduce((acc, module) => {
          const result = resultsByModule[module.id] as ModuleResultsResponse | undefined;
          if (!result) return acc;
          if (result.progress_status === ProgressStatus.COMPLETED) {
            return acc + 100;
          }
          if (result.total_questions > 0) {
            return acc + Math.round((result.attempted / result.total_questions) * 100);
          }
          return acc;
        }, 0) / modules.length
      )
    : 0;

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
              value={overallCompletionPercent}
              sx={{ height: 10, borderRadius: 1 }}
            />
            <Typography variant="caption" sx={{ color: 'text.secondary' }}>
              {completedCount} of {modules.length} modules complete ({overallCompletionPercent}% overall progress)
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
            const r = resultsByModule[m.id] as ModuleResultsResponse | undefined;
            const total = r?.total_questions ?? 0;
            const attempted = r?.attempted ?? 0;
            const correct = r?.correct ?? 0;

            const statusLabel = (() => {
              switch (r?.progress_status) {
                case ProgressStatus.COMPLETED:
                  return 'Completed';
                case ProgressStatus.IN_PROGRESS:
                  return 'In progress';
                default:
                  return 'Not started';
              }
            })();

            const completionPercent =
              r?.progress_status === ProgressStatus.COMPLETED
                ? 100
                : total > 0
                  ? Math.round((attempted / total) * 100)
                  : 0;

            // Show subtle achievement badges on completed modules
            // Filter to show completion/score achievements that are earned
            const moduleAchievements = achievements
              .filter((a) => {
                if (!a.earned) return false;
                // Show completion and score achievements (most relevant to module completion)
                return a.category === 'completion' || a.category === 'score';
              })
              .slice(0, 2); // Limit to 2 badges to keep it subtle
            const showAchievements = r?.progress_status === ProgressStatus.COMPLETED && moduleAchievements.length > 0;

            return (
              <Grid size={{ xs: 12, sm: 6, md: 4 }} key={m.id}>
                <Card className="glass-surface" sx={{ borderRadius: 3, height: '100%' }}>
                  <CardContent>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', mb: 1 }}>
                      <Box sx={{ flex: 1 }}>
                        <Typography variant="h6" sx={{ color: 'text.primary', fontWeight: 'bold', mb: 1 }}>
                          {m.title}
                        </Typography>
                        <Typography variant="caption" sx={{ color: mode === 'light' ? 'text.secondary' : 'rgba(255,255,255,0.7)' }}>
                          {statusLabel}
                        </Typography>
                      </Box>
                      {showAchievements && (
                        <Box sx={{ display: 'flex', gap: 0.5, flexWrap: 'wrap', justifyContent: 'flex-end' }}>
                          {moduleAchievements.map((achievement) => (
                            <AchievementBadge
                              key={achievement.id}
                              name={achievement.name}
                              description={achievement.description}
                              icon={achievement.icon}
                              earned={achievement.earned}
                              size="small"
                            />
                          ))}
                        </Box>
                      )}
                    </Box>
                    <Box sx={{ mt: 2 }}>
                      <LinearProgress variant="determinate" value={completionPercent} sx={{ height: 8, borderRadius: 1 }} />
                      <Typography variant="caption" sx={{ color: 'text.secondary' }}>
                        {correct}/{total} correct ({completionPercent}% complete)
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


