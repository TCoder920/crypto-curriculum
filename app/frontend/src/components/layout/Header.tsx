/** Header component with user profile, theme toggle, and notifications */
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  AppBar,
  Toolbar,
  Box,
  IconButton,
  Avatar,
  Menu,
  MenuItem,
  Badge,
  Typography,
  Divider,
  Tooltip,
} from '@mui/material';
import {
  Brightness4,
  Brightness7,
  Notifications,
  AccountCircle,
  Settings,
  Logout,
} from '@mui/icons-material';
import { motion, useScroll, useTransform } from 'framer-motion';
import { useAuth } from '../../contexts/AuthContext';
import { useThemeMode } from '../../contexts/ThemeContext';

export const Header: React.FC = () => {
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const { mode, toggleTheme } = useThemeMode();
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const [notificationAnchor, setNotificationAnchor] = useState<null | HTMLElement>(null);
  const [notificationCount, setNotificationCount] = useState(0);

  // Scroll-based shrinking effect
  const { scrollY } = useScroll();
  const headerHeight = useTransform(scrollY, [0, 100], [80, 60]);
  const headerOpacity = useTransform(scrollY, [0, 50], [1, 0.95]);

  const handleProfileMenuOpen = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleProfileMenuClose = () => {
    setAnchorEl(null);
  };

  const handleNotificationMenuOpen = (event: React.MouseEvent<HTMLElement>) => {
    setNotificationAnchor(event.currentTarget);
  };

  const handleNotificationMenuClose = () => {
    setNotificationAnchor(null);
  };

  const handleLogout = async () => {
    handleProfileMenuClose();
    await logout();
    navigate('/login');
  };

  const handleProfile = () => {
    handleProfileMenuClose();
    navigate('/profile');
  };

  const handleSettings = () => {
    handleProfileMenuClose();
    navigate('/settings');
  };

  // Get user initials for avatar
  const getUserInitials = () => {
    if (user?.full_name) {
      return user.full_name
        .split(' ')
        .map((n) => n[0])
        .join('')
        .toUpperCase()
        .slice(0, 2);
    }
    if (user?.email) {
      return user.email[0].toUpperCase();
    }
    return 'U';
  };

  const isProfileMenuOpen = Boolean(anchorEl);
  const isNotificationMenuOpen = Boolean(notificationAnchor);

  return (
    <motion.div
      style={{
        height: headerHeight,
        opacity: headerOpacity,
      }}
    >
      <AppBar
        position="sticky"
        sx={{
          backgroundColor: mode === 'light' ? '#ffffff' : '#0a0e27',
          borderBottom: mode === 'light' ? '1px solid rgba(0, 0, 0, 0.1)' : '1px solid rgba(255, 255, 255, 0.1)',
          boxShadow: 'none',
          transition: 'all 0.3s ease',
        }}
      >
        <Toolbar
          sx={{
            justifyContent: 'space-between',
            px: 3,
            minHeight: { xs: 56, sm: 64 },
            height: '100%',
          }}
        >
          {/* Left side - Logo/Brand */}
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Typography
              variant="h6"
              component="div"
              sx={{
                fontWeight: 'bold',
                color: mode === 'light' ? '#1976d2' : '#ffffff',
                cursor: 'pointer',
                display: { xs: 'none', sm: 'block' },
              }}
              onClick={() => navigate('/')}
            >
              Crypto Curriculum
            </Typography>
          </Box>

          {/* Right side - Actions */}
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            {/* Theme Toggle */}
            <Tooltip title={mode === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'}>
              <IconButton
                onClick={toggleTheme}
                sx={{
                  color: mode === 'light' ? 'rgba(0, 0, 0, 0.7)' : 'rgba(255, 255, 255, 0.7)',
                  '&:hover': {
                    color: mode === 'light' ? '#1976d2' : '#ffffff',
                    backgroundColor: mode === 'light' ? 'rgba(25, 118, 210, 0.1)' : 'rgba(255, 255, 255, 0.1)',
                  },
                }}
                aria-label="toggle theme"
              >
                {mode === 'dark' ? <Brightness7 /> : <Brightness4 />}
              </IconButton>
            </Tooltip>

            {/* Notifications */}
            <Tooltip title="Notifications">
              <IconButton
                onClick={handleNotificationMenuOpen}
                sx={{
                  color: mode === 'light' ? 'rgba(0, 0, 0, 0.7)' : 'rgba(255, 255, 255, 0.7)',
                  '&:hover': {
                    color: mode === 'light' ? '#1976d2' : '#ffffff',
                    backgroundColor: mode === 'light' ? 'rgba(25, 118, 210, 0.1)' : 'rgba(255, 255, 255, 0.1)',
                  },
                }}
                aria-label="notifications"
              >
                <Badge badgeContent={notificationCount} color="error">
                  <Notifications />
                </Badge>
              </IconButton>
            </Tooltip>

            {/* User Profile */}
            <Tooltip title="Account settings">
              <IconButton
                onClick={handleProfileMenuOpen}
                sx={{
                  p: 0.5,
                  '&:hover': {
                    opacity: 0.8,
                  },
                }}
                aria-label="account menu"
              >
                <Avatar
                  sx={{
                    width: 36,
                    height: 36,
                    bgcolor: mode === 'light' ? '#1976d2' : '#4dabf7',
                    color: '#ffffff',
                    fontSize: '0.875rem',
                    fontWeight: 'bold',
                  }}
                >
                  {getUserInitials()}
                </Avatar>
              </IconButton>
            </Tooltip>
          </Box>
        </Toolbar>
      </AppBar>

      {/* Profile Menu */}
      <Menu
        anchorEl={anchorEl}
        open={isProfileMenuOpen}
        onClose={handleProfileMenuClose}
        onClick={handleProfileMenuClose}
        PaperProps={{
          elevation: 3,
          sx: {
            mt: 1.5,
            minWidth: 200,
            borderRadius: 2,
            backgroundColor: mode === 'light' ? '#ffffff' : '#1a1f3a',
            border: mode === 'light' ? '1px solid rgba(0, 0, 0, 0.1)' : '1px solid rgba(255, 255, 255, 0.1)',
            '& .MuiMenuItem-root': {
              color: mode === 'light' ? 'rgba(0, 0, 0, 0.87)' : 'rgba(255, 255, 255, 0.87)',
              '&:hover': {
                backgroundColor: mode === 'light' ? 'rgba(0, 0, 0, 0.04)' : 'rgba(255, 255, 255, 0.08)',
              },
            },
          },
        }}
        transformOrigin={{ horizontal: 'right', vertical: 'top' }}
        anchorOrigin={{ horizontal: 'right', vertical: 'bottom' }}
      >
        <Box sx={{ px: 2, py: 1.5 }}>
          <Typography variant="subtitle2" sx={{ fontWeight: 'bold', color: mode === 'light' ? '#1976d2' : '#4dabf7' }}>
            {user?.full_name || user?.email || 'User'}
          </Typography>
          <Typography variant="caption" sx={{ color: mode === 'light' ? 'rgba(0, 0, 0, 0.6)' : 'rgba(255, 255, 255, 0.6)' }}>
            {user?.email}
          </Typography>
          {user?.role && (
            <Typography variant="caption" sx={{ display: 'block', mt: 0.5, textTransform: 'capitalize' }}>
              {user.role}
            </Typography>
          )}
        </Box>
        <Divider sx={{ my: 1 }} />
        <MenuItem onClick={handleProfile}>
          <AccountCircle sx={{ mr: 2, fontSize: 20 }} />
          Profile
        </MenuItem>
        <MenuItem onClick={handleSettings}>
          <Settings sx={{ mr: 2, fontSize: 20 }} />
          Settings
        </MenuItem>
        <Divider sx={{ my: 1 }} />
        <MenuItem onClick={handleLogout}>
          <Logout sx={{ mr: 2, fontSize: 20 }} />
          Logout
        </MenuItem>
      </Menu>

      {/* Notifications Menu */}
      <Menu
        anchorEl={notificationAnchor}
        open={isNotificationMenuOpen}
        onClose={handleNotificationMenuClose}
        PaperProps={{
          elevation: 3,
          sx: {
            mt: 1.5,
            minWidth: 320,
            maxWidth: 400,
            maxHeight: 400,
            borderRadius: 2,
            backgroundColor: mode === 'light' ? '#ffffff' : '#1a1f3a',
            border: mode === 'light' ? '1px solid rgba(0, 0, 0, 0.1)' : '1px solid rgba(255, 255, 255, 0.1)',
          },
        }}
        transformOrigin={{ horizontal: 'right', vertical: 'top' }}
        anchorOrigin={{ horizontal: 'right', vertical: 'bottom' }}
      >
        <Box sx={{ px: 2, py: 1.5 }}>
          <Typography variant="subtitle1" sx={{ fontWeight: 'bold' }}>
            Notifications
          </Typography>
        </Box>
        <Divider />
        {notificationCount === 0 ? (
          <Box sx={{ px: 2, py: 4, textAlign: 'center' }}>
            <Typography variant="body2" sx={{ color: mode === 'light' ? 'rgba(0, 0, 0, 0.6)' : 'rgba(255, 255, 255, 0.6)' }}>
              No new notifications
            </Typography>
          </Box>
        ) : (
          <Box sx={{ maxHeight: 300, overflow: 'auto' }}>
            {/* Notification items would go here */}
            <MenuItem onClick={handleNotificationMenuClose}>
              <Typography variant="body2">Sample notification</Typography>
            </MenuItem>
          </Box>
        )}
      </Menu>
    </motion.div>
  );
};

