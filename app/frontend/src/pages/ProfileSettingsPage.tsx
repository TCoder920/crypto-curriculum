/** Profile and Settings page */
import React, { useState } from 'react';
import { Box, Container, Typography, Paper, TextField, Button, Divider, Alert, Grid, Chip } from '@mui/material';
import { useThemeMode } from '../contexts/ThemeContext';
import { useAuth } from '../contexts/AuthContext';
import { useQuery } from '@tanstack/react-query';
import { achievementService } from '../services/achievementService';
import { AchievementBadge } from '../components/achievement/AchievementBadge';

export const ProfileSettingsPage: React.FC = () => {
  const { mode } = useThemeMode();
  const { user } = useAuth();
  const backgroundColor = mode === 'light' ? '#f8f9fa' : '#0a0e27';

  // Simple local state placeholders
  const [fullName, setFullName] = useState(user?.full_name || '');
  const [username, setUsername] = useState(user?.username || '');
  const [message, setMessage] = useState<string | null>(null);

  // Fetch achievements
  const achievementsQuery = useQuery({
    queryKey: ['achievements'],
    queryFn: () => achievementService.getAchievements(),
  });

  const statsQuery = useQuery({
    queryKey: ['achievement-stats'],
    queryFn: () => achievementService.getStats(),
  });

  const achievements = achievementsQuery.data || [];
  const stats = statsQuery.data;
  const earnedAchievements = achievements.filter(a => a.earned);

  const onSave = () => {
    // Placeholder only; wire to backend update endpoint later
    setMessage('Settings saved (mock).');
    setTimeout(() => setMessage(null), 2000);
  };

  return (
    <Box sx={{ minHeight: '100vh', backgroundColor, py: 4 }}>
      <Container maxWidth="md">
        <Typography variant="h4" sx={{ fontWeight: 'bold', color: 'text.primary', mb: 2 }}>
          Profile & Settings
        </Typography>
        <Typography variant="body2" sx={{ color: mode === 'light' ? 'text.secondary' : 'rgba(255,255,255,0.8)', mb: 3 }}>
          Manage your account details and preferences.
        </Typography>

        {message && <Alert severity="success" sx={{ mb: 2 }}>{message}</Alert>}

        <Paper className="glass-surface" sx={{ p: 3, borderRadius: 3, mb: 3 }}>
          <Typography variant="h6" sx={{ color: 'text.primary', mb: 2 }}>
            Account
          </Typography>
          <Box sx={{ display: 'grid', gap: 2, gridTemplateColumns: { xs: '1fr', sm: '1fr 1fr' } }}>
            <TextField
              label="Full name"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              fullWidth
            />
            <TextField
              label="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              fullWidth
            />
            <TextField label="Email" value={user?.email || ''} fullWidth disabled />
          </Box>
          <Box sx={{ mt: 2 }}>
            <Button variant="contained" onClick={onSave}>
              Save changes
            </Button>
          </Box>
        </Paper>

        <Paper className="glass-surface" sx={{ p: 3, borderRadius: 3, mb: 3 }}>
          <Typography variant="h6" sx={{ color: 'text.primary', mb: 2 }}>
            Achievements
          </Typography>
          {stats && (
            <Box sx={{ mb: 2 }}>
              <Typography variant="body2" sx={{ color: mode === 'light' ? 'text.secondary' : 'rgba(255,255,255,0.8)', mb: 1 }}>
                {stats.earned_count} of {stats.total_achievements} achievements earned
              </Typography>
              <Box sx={{ display: 'flex', gap: 1, alignItems: 'center' }}>
                <Chip
                  label={`${stats.completion_percentage.toFixed(0)}%`}
                  size="small"
                  color="primary"
                  variant="outlined"
                />
                <Chip
                  label={`${stats.total_points} points`}
                  size="small"
                  color="primary"
                  variant="outlined"
                />
              </Box>
            </Box>
          )}
          {earnedAchievements.length > 0 ? (
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1.5 }}>
              {earnedAchievements.map((achievement) => (
                <AchievementBadge
                  key={achievement.id}
                  name={achievement.name}
                  description={achievement.description}
                  icon={achievement.icon}
                  earned={achievement.earned}
                />
              ))}
            </Box>
          ) : (
            <Typography variant="body2" sx={{ color: mode === 'light' ? 'text.secondary' : 'rgba(255,255,255,0.6)' }}>
              Complete modules and assessments to earn achievements.
            </Typography>
          )}
        </Paper>

        <Paper className="glass-surface" sx={{ p: 3, borderRadius: 3 }}>
          <Typography variant="h6" sx={{ color: 'text.primary', mb: 2 }}>
            Preferences
          </Typography>
          <Typography variant="body2" sx={{ color: mode === 'light' ? 'text.secondary' : 'rgba(255,255,255,0.8)' }}>
            Theme preferences can be toggled from the header. More settings coming soon.
          </Typography>
          <Divider sx={{ my: 2 }} />
          <Typography variant="caption" sx={{ color: mode === 'light' ? 'text.secondary' : 'rgba(255,255,255,0.6)' }}>
            Tip: Use the bell icon in the header to view notifications.
          </Typography>
        </Paper>
      </Container>
    </Box>
  );
};


