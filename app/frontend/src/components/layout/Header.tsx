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
  Typography,
  Divider,
  Tooltip,
  Dialog,
  DialogContent,
  DialogTitle,
  IconButton as DialogIconButton,
} from '@mui/material';
import {
  Brightness4,
  Brightness7,
  AccountCircle,
  Settings,
  Logout,
  SmartToy,
  Close,
} from '@mui/icons-material';
import { motion, useScroll, useTransform } from 'framer-motion';
import { useAuth } from '../../contexts/AuthContext';
import { useThemeMode } from '../../contexts/ThemeContext';
import { NotificationBell } from '../notification/NotificationBell';
import { ChatInterface } from '../ai/ChatInterface';

export const Header: React.FC = () => {
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const { mode, toggleTheme } = useThemeMode();
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const [aiChatOpen, setAiChatOpen] = useState(false);

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

            {/* AI Chat Assistant */}
            {user && (
              <Tooltip title="AI Learning Assistant">
                <IconButton
                  onClick={() => setAiChatOpen(true)}
                  sx={{
                    color: mode === 'light' ? 'rgba(0, 0, 0, 0.7)' : 'rgba(255, 255, 255, 0.7)',
                    '&:hover': {
                      color: mode === 'light' ? '#1976d2' : '#ffffff',
                      backgroundColor: mode === 'light' ? 'rgba(25, 118, 210, 0.1)' : 'rgba(255, 255, 255, 0.1)',
                    },
                  }}
                  aria-label="AI assistant"
                >
                  <SmartToy />
                </IconButton>
              </Tooltip>
            )}

            {/* Notifications */}
            {user && <NotificationBell />}

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

      {/* AI Chat Dialog */}
      <Dialog
        open={aiChatOpen}
        onClose={() => setAiChatOpen(false)}
        maxWidth="md"
        fullWidth
        PaperProps={{
          sx: {
            height: '80vh',
            maxHeight: 800,
          },
        }}
      >
        <DialogTitle sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <SmartToy color="primary" />
            <Typography variant="h6">AI Learning Assistant</Typography>
          </Box>
          <DialogIconButton
            onClick={() => setAiChatOpen(false)}
            aria-label="close"
          >
            <Close />
          </DialogIconButton>
        </DialogTitle>
        <DialogContent sx={{ p: 0, display: 'flex', flexDirection: 'column', height: '100%' }}>
          <ChatInterface />
        </DialogContent>
      </Dialog>

    </motion.div>
  );
};

