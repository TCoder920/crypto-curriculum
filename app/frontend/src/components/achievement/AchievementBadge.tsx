/** Subtle achievement badge component */
import React from 'react';
import { Box, Tooltip, Typography } from '@mui/material';
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

interface AchievementBadgeProps {
  name: string;
  description: string | null;
  icon: string | null;
  earned: boolean;
  size?: 'small' | 'medium';
}

export const AchievementBadge: React.FC<AchievementBadgeProps> = ({
  name,
  description,
  icon,
  earned,
  size = 'medium',
}) => {
  const { mode } = useThemeMode();
  const iconSize = size === 'small' ? 20 : 24;

  if (!earned) {
    return null; // Don't show unearned achievements
  }

  return (
    <Tooltip
      title={
        <Box>
          <Typography variant="body2" sx={{ fontWeight: 'bold', mb: 0.5 }}>
            {name}
          </Typography>
          {description && (
            <Typography variant="caption">{description}</Typography>
          )}
        </Box>
      }
      arrow
    >
      <Box
        sx={{
          display: 'inline-flex',
          alignItems: 'center',
          justifyContent: 'center',
          width: iconSize + 8,
          height: iconSize + 8,
          borderRadius: '50%',
          backgroundColor: mode === 'light' ? 'rgba(25, 118, 210, 0.1)' : 'rgba(255, 255, 255, 0.1)',
          border: `1px solid ${mode === 'light' ? 'rgba(25, 118, 210, 0.2)' : 'rgba(255, 255, 255, 0.2)'}`,
          fontSize: iconSize,
          lineHeight: 1,
          opacity: 0.9,
          transition: 'all 0.2s',
          '&:hover': {
            opacity: 1,
            transform: 'scale(1.1)',
            backgroundColor: mode === 'light' ? 'rgba(25, 118, 210, 0.15)' : 'rgba(255, 255, 255, 0.15)',
          },
        }}
      >
        {icon ? iconMap[icon] || '🏅' : '🏅'}
      </Box>
    </Tooltip>
  );
};

