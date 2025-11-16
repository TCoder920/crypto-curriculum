/** Analytics dashboard component */
import React from 'react';
import {
  Box,
  Container,
  Typography,
  Card,
  CardContent,
  Grid,
  Alert,
  LinearProgress,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
} from '@mui/material';
import { useQuery } from '@tanstack/react-query';
import { useAuth } from '../../contexts/AuthContext';
import { analyticsService, type StudentAnalytics } from '../../services/analyticsService';
import { useThemeMode } from '../../contexts/ThemeContext';

export const AnalyticsDashboard: React.FC = () => {
  const { user } = useAuth();
  const { mode } = useThemeMode();

  const analyticsQuery = useQuery({
    queryKey: ['student-analytics', user?.id],
    queryFn: () => analyticsService.getStudentAnalytics(user!.id),
    enabled: !!user?.id,
  });

  const analytics: StudentAnalytics | undefined = analyticsQuery.data;

  if (analyticsQuery.isLoading) {
    return (
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <Typography>Loading analytics...</Typography>
      </Container>
    );
  }

  if (analyticsQuery.isError || !analytics) {
    return (
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <Alert severity="error">Failed to load analytics</Alert>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h4" gutterBottom>
        Your Analytics
      </Typography>

      {/* Overview Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ bgcolor: mode === 'light' ? 'background.paper' : 'grey.900' }}>
            <CardContent>
              <Typography variant="body2" color="text.secondary">
                Modules Completed
              </Typography>
              <Typography variant="h4">{analytics.total_modules_completed}</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ bgcolor: mode === 'light' ? 'background.paper' : 'grey.900' }}>
            <CardContent>
              <Typography variant="body2" color="text.secondary">
                Average Score
              </Typography>
              <Typography variant="h4">{analytics.average_score.toFixed(1)}%</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ bgcolor: mode === 'light' ? 'background.paper' : 'grey.900' }}>
            <CardContent>
              <Typography variant="body2" color="text.secondary">
                Current Streak
              </Typography>
              <Typography variant="h4">{analytics.current_streak_days} days</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ bgcolor: mode === 'light' ? 'background.paper' : 'grey.900' }}>
            <CardContent>
              <Typography variant="body2" color="text.secondary">
                Total Achievements
              </Typography>
              <Typography variant="h4">{analytics.total_achievements}</Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Progress by Status */}
      <Card sx={{ mb: 4, bgcolor: mode === 'light' ? 'background.paper' : 'grey.900' }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Progress by Status
          </Typography>
          <Grid container spacing={2} sx={{ mt: 2 }}>
            <Grid item xs={12} md={4}>
              <Typography variant="body2" color="text.secondary">
                Completed
              </Typography>
              <Typography variant="h5">{analytics.modules_by_status.completed}</Typography>
            </Grid>
            <Grid item xs={12} md={4}>
              <Typography variant="body2" color="text.secondary">
                In Progress
              </Typography>
              <Typography variant="h5">{analytics.modules_by_status.in_progress}</Typography>
            </Grid>
            <Grid item xs={12} md={4}>
              <Typography variant="body2" color="text.secondary">
                Not Started
              </Typography>
              <Typography variant="h5">{analytics.modules_by_status.not_started}</Typography>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* Scores by Module */}
      {analytics.scores_by_module.length > 0 && (
        <Card sx={{ mb: 4, bgcolor: mode === 'light' ? 'background.paper' : 'grey.900' }}>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Scores by Module
            </Typography>
            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Module</TableCell>
                    <TableCell align="right">Best Score</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {analytics.scores_by_module.map((score) => (
                    <TableRow key={score.module_id}>
                      <TableCell>{score.module_title}</TableCell>
                      <TableCell align="right">
                        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'flex-end' }}>
                          <Typography variant="body2" sx={{ mr: 1 }}>
                            {score.best_score.toFixed(1)}%
                          </Typography>
                          <LinearProgress
                            variant="determinate"
                            value={score.best_score}
                            sx={{ width: 100, height: 8, borderRadius: 1 }}
                            color={score.best_score >= 70 ? 'success' : 'error'}
                          />
                        </Box>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </CardContent>
        </Card>
      )}

      {/* Recent Activity */}
      {analytics.recent_activity.length > 0 && (
        <Card sx={{ bgcolor: mode === 'light' ? 'background.paper' : 'grey.900' }}>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Recent Activity
            </Typography>
            <Box sx={{ mt: 2 }}>
              {analytics.recent_activity.map((activity, index) => (
                <Box
                  key={index}
                  sx={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    py: 1,
                    borderBottom: index < analytics.recent_activity.length - 1 ? 1 : 0,
                    borderColor: 'divider',
                  }}
                >
                  <Box>
                    <Typography variant="body1">{activity.module_title}</Typography>
                    <Typography variant="caption" color="text.secondary">
                      {activity.status}
                    </Typography>
                  </Box>
                  <Typography variant="caption" color="text.secondary">
                    {activity.updated_at
                      ? new Date(activity.updated_at).toLocaleDateString()
                      : 'N/A'}
                  </Typography>
                </Box>
              ))}
            </Box>
          </CardContent>
        </Card>
      )}
    </Container>
  );
};

