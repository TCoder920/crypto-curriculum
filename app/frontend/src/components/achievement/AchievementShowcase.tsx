/** Achievement showcase component */
import React, { useEffect, useState } from 'react';
import {
  Box,
  Container,
  Typography,
  Card,
  CardContent,
  Grid,
  Chip,
  LinearProgress,
  Alert,
  Tabs,
  Tab,
} from '@mui/material';
import { useQuery } from '@tanstack/react-query';
import { achievementService, type Achievement, type AchievementStats } from '../../services/achievementService';
import { useThemeMode } from '../../contexts/ThemeContext';

const iconMap: Record<string, string> = {
  trophy: '🏆',
  star: '⭐',
  medal: '🥇',
  award: '🏅',
  certificate: '📜',
  'chart-line': '📈',
  code: '💻',
  building: '🏗️',
  crown: '👑',
  'hand-holding-heart': '🤝',
  users: '👥',
  fire: '🔥',
  flame: '🔥',
  route: '🗺️',
  compass: '🧭',
  'graduation-cap': '🎓',
  lightbulb: '💡',
  'chart-bar': '📊',
  link: '🔗',
  wallet: '💼',
  chat: '💬',
};

export const AchievementShowcase: React.FC = () => {
  const { mode } = useThemeMode();
  const [selectedCategory, setSelectedCategory] = useState<string>('all');

  const achievementsQuery = useQuery({
    queryKey: ['achievements'],
    queryFn: () => achievementService.getAchievements(),
  });

  const statsQuery = useQuery({
    queryKey: ['achievement-stats'],
    queryFn: () => achievementService.getStats(),
  });

  const achievements: Achievement[] = achievementsQuery.data || [];
  const stats: AchievementStats | undefined = statsQuery.data;

  const categories = ['all', ...Array.from(new Set(achievements.map(a => a.category).filter(Boolean)))];
  const filteredAchievements = selectedCategory === 'all'
    ? achievements
    : achievements.filter(a => a.category === selectedCategory);

  const earnedAchievements = achievements.filter(a => a.earned);
  const unearnedAchievements = achievements.filter(a => !a.earned);

  if (achievementsQuery.isLoading || statsQuery.isLoading) {
    return (
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <Typography>Loading achievements...</Typography>
      </Container>
    );
  }

  if (achievementsQuery.isError || statsQuery.isError) {
    return (
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <Alert severity="error">Failed to load achievements</Alert>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h4" gutterBottom>
        Achievements
      </Typography>

      {/* Stats Overview */}
      {stats && (
        <Card sx={{ mb: 4, bgcolor: mode === 'light' ? 'background.paper' : 'grey.900' }}>
          <CardContent>
            <Grid container spacing={3}>
              <Grid item xs={12} md={3}>
                <Typography variant="body2" color="text.secondary">
                  Total Achievements
                </Typography>
                <Typography variant="h4">{stats.total_achievements}</Typography>
              </Grid>
              <Grid item xs={12} md={3}>
                <Typography variant="body2" color="text.secondary">
                  Earned
                </Typography>
                <Typography variant="h4">{stats.earned_count}</Typography>
              </Grid>
              <Grid item xs={12} md={3}>
                <Typography variant="body2" color="text.secondary">
                  Completion
                </Typography>
                <Typography variant="h4">{stats.completion_percentage.toFixed(1)}%</Typography>
                <LinearProgress
                  variant="determinate"
                  value={stats.completion_percentage}
                  sx={{ mt: 1 }}
                />
              </Grid>
              <Grid item xs={12} md={3}>
                <Typography variant="body2" color="text.secondary">
                  Total Points
                </Typography>
                <Typography variant="h4">{stats.total_points}</Typography>
              </Grid>
            </Grid>
          </CardContent>
        </Card>
      )}

      {/* Category Tabs */}
      <Box sx={{ mb: 3 }}>
        <Tabs
          value={selectedCategory}
          onChange={(_, newValue) => setSelectedCategory(newValue)}
          variant="scrollable"
          scrollButtons="auto"
        >
          {categories.map(category => (
            <Tab
              key={category}
              label={category === 'all' ? 'All' : category?.charAt(0).toUpperCase() + category?.slice(1)}
              value={category || 'all'}
            />
          ))}
        </Tabs>
      </Box>

      {/* Achievements Grid */}
      <Grid container spacing={3}>
        {filteredAchievements.map(achievement => (
          <Grid item xs={12} sm={6} md={4} key={achievement.id}>
            <Card
              sx={{
                bgcolor: achievement.earned
                  ? mode === 'light' ? 'background.paper' : 'grey.900'
                  : mode === 'light' ? 'grey.100' : 'grey.800',
                opacity: achievement.earned ? 1 : 0.6,
                height: '100%',
                position: 'relative',
              }}
            >
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Typography variant="h3" sx={{ mr: 2 }}>
                    {achievement.icon ? iconMap[achievement.icon] || '🏅' : '🏅'}
                  </Typography>
                  <Box sx={{ flex: 1 }}>
                    <Typography variant="h6">{achievement.name}</Typography>
                    {achievement.category && (
                      <Chip
                        label={achievement.category}
                        size="small"
                        sx={{ mt: 0.5 }}
                      />
                    )}
                  </Box>
                </Box>

                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                  {achievement.description}
                </Typography>

                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <Chip
                    label={`${achievement.points} points`}
                    size="small"
                    color="primary"
                  />
                  {achievement.earned && (
                    <Chip
                      label="Earned"
                      size="small"
                      color="success"
                    />
                  )}
                </Box>

                {achievement.earned && achievement.earned_at && (
                  <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block' }}>
                    Earned: {new Date(achievement.earned_at).toLocaleDateString()}
                  </Typography>
                )}
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {filteredAchievements.length === 0 && (
        <Alert severity="info">No achievements found in this category.</Alert>
      )}
    </Container>
  );
};

