/** Header component with utility icons - logo, AI chat, theme toggle, notifications, profile */
import React from 'react';
import { useNavigate } from 'react-router-dom';
import { AppBar, Toolbar, Box, Typography, IconButton, Avatar, Badge, Menu, MenuItem, Divider, ListItemIcon, Tooltip, Dialog, DialogContent, DialogTitle, Button } from '@mui/material';
import { School, Logout, Brightness4, Brightness7, Notifications, Settings, Person, SmartToy, Close } from '@mui/icons-material';
import { useAuth } from '../../contexts/AuthContext';
import { useThemeMode } from '../../contexts/ThemeContext';
import { ChatInterface } from '../ai/ChatInterface';
import { SidebarMenuButton } from './Sidebar';

export const Navigation: React.FC = () => {
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const { mode, toggleTheme } = useThemeMode();

  // Header menus state
  const [profileAnchorEl, setProfileAnchorEl] = React.useState<null | HTMLElement>(null);
  const [notifAnchorEl, setNotifAnchorEl] = React.useState<null | HTMLElement>(null);
  const [aiChatOpen, setAiChatOpen] = React.useState(false);
  const isProfileOpen = Boolean(profileAnchorEl);
  const isNotifOpen = Boolean(notifAnchorEl);

  // Simple notifications model (can be wired to API later)
  const [notifications, setNotifications] = React.useState<
    { id: number; title: string; message?: string; read: boolean; href?: string }[]
  >([
    { id: 1, title: 'Welcome to Crypto Curriculum!', message: 'Start with Module 1.', read: false, href: '/' },
    { id: 2, title: 'New assessments available', message: 'Check the Assessments page.', read: false, href: '/assessments' },
  ]);
  const unreadCount = notifications.filter(n => !n.read).length;

  const markAllAsRead = () => {
    setNotifications(prev => prev.map(n => ({ ...n, read: true })));
  };
  const clearAll = () => setNotifications([]);
  const goToNotification = (href?: string, id?: number) => {
    if (id) {
      setNotifications(prev => prev.map(n => (n.id === id ? { ...n, read: true } : n)));
    }
    if (href) navigate(href);
    setNotifAnchorEl(null);
  };

  const getInitials = (nameOrEmail?: string) => {
    if (!nameOrEmail) return 'U';
    const name = nameOrEmail.includes('@') ? nameOrEmail.split('@')[0] : nameOrEmail;
    const parts = name.split(/[.\s_]+/).filter(Boolean);
    if (parts.length === 1) return parts[0].slice(0, 2).toUpperCase();
    return (parts[0][0] + parts[1][0]).toUpperCase();
  };

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  return (
    <>
      <AppBar 
        position="sticky" 
        sx={{ 
          backgroundColor: mode === 'light' ? '#ffffff' : '#0a0e27',
          borderBottom: mode === 'light' ? '1px solid rgba(0, 0, 0, 0.1)' : '1px solid rgba(255, 255, 255, 0.1)',
          boxShadow: 'none',
          zIndex: (theme) => theme.zIndex.drawer + 1,
          width: '100%',
        }}
      >
        <Toolbar 
          sx={{ 
            justifyContent: 'space-between', 
            px: { xs: 2, sm: 3 },
            minHeight: { xs: 56, sm: 64 },
          }}
        >
          {/* Left side - Logo and Sidebar toggle (mobile) */}
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <SidebarMenuButton />
            <Typography 
              variant="h6" 
              component="div" 
              sx={{ 
                fontWeight: 'bold',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: 1,
                color: mode === 'light' ? '#1976d2' : '#ffffff',
                fontSize: { xs: '1rem', sm: '1.25rem' },
              }}
              onClick={() => navigate('/')}
            >
              <School sx={{ fontSize: { xs: 24, sm: 28 } }} />
              <Box component="span" sx={{ display: { xs: 'none', sm: 'inline' } }}>
                Crypto Curriculum
              </Box>
            </Typography>
          </Box>

          {/* Right side - Utility icons */}
          <Box 
            sx={{ 
              display: 'flex', 
              alignItems: 'center', 
              gap: { xs: 0.5, sm: 1 },
              flexShrink: 0,
            }}
          >
            {/* AI Chat Assistant - visible for all logged-in users */}
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

            {/* Theme toggle */}
            <Tooltip title="Toggle theme">
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
                onClick={(e) => setNotifAnchorEl(e.currentTarget)}
                sx={{
                  color: mode === 'light' ? 'rgba(0, 0, 0, 0.7)' : 'rgba(255, 255, 255, 0.7)',
                  '&:hover': {
                    color: mode === 'light' ? '#1976d2' : '#ffffff',
                    backgroundColor: mode === 'light' ? 'rgba(25, 118, 210, 0.1)' : 'rgba(255, 255, 255, 0.1)',
                  },
                }}
                aria-label="notifications"
              >
                <Badge color="error" badgeContent={unreadCount} overlap="circular">
                  <Notifications />
                </Badge>
              </IconButton>
            </Tooltip>
            <Menu
              anchorEl={notifAnchorEl}
              open={isNotifOpen}
              onClose={() => setNotifAnchorEl(null)}
              PaperProps={{
                sx: { minWidth: 320, mt: 1 }
              }}
            >
              <Box sx={{ px: 2, py: 1, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <Typography variant="subtitle2" sx={{ color: 'text.primary' }}>Notifications</Typography>
                <Box sx={{ display: 'flex', gap: 1 }}>
                  <Button size="small" onClick={markAllAsRead}>Mark all read</Button>
                  <Button size="small" onClick={clearAll}>Clear</Button>
                </Box>
              </Box>
              <Divider />
              {notifications.length === 0 ? (
                <MenuItem disabled>
                  <Typography variant="body2" sx={{ color: 'text.secondary' }}>No notifications</Typography>
                </MenuItem>
              ) : (
                notifications.map(n => (
                  <MenuItem key={n.id} onClick={() => goToNotification(n.href, n.id)} dense>
                    <ListItemIcon>
                      <Notifications fontSize="small" color={n.read ? 'inherit' : 'primary'} />
                    </ListItemIcon>
                    <Box sx={{ display: 'flex', flexDirection: 'column' }}>
                      <Typography variant="body2" sx={{ color: 'text.primary' }}>{n.title}</Typography>
                      {n.message && (
                        <Typography variant="caption" sx={{ color: 'text.secondary' }}>{n.message}</Typography>
                      )}
                    </Box>
                  </MenuItem>
                ))
              )}
            </Menu>

            {/* Profile */}
            <Tooltip title="Account">
              <IconButton
                onClick={(e) => setProfileAnchorEl(e.currentTarget)}
                sx={{
                  p: 0.5,
                  borderRadius: '50%',
                  border: mode === 'light' ? '1px solid rgba(0,0,0,0.08)' : '1px solid rgba(255,255,255,0.12)',
                  flexShrink: 0,
                }}
                aria-label="account"
              >
                <Avatar
                  sx={{
                    width: { xs: 32, sm: 36 },
                    height: { xs: 32, sm: 36 },
                    fontSize: { xs: 14, sm: 16 },
                    bgcolor: mode === 'light' ? '#1976d2' : '#1e88e5'
                  }}
                >
                  {getInitials(user?.full_name || user?.email)}
                </Avatar>
              </IconButton>
            </Tooltip>
            <Menu
              anchorEl={profileAnchorEl}
              open={isProfileOpen}
              onClose={() => setProfileAnchorEl(null)}
              PaperProps={{
                sx: { mt: 1, minWidth: 220 }
              }}
            >
              <MenuItem disabled>
                <ListItemIcon>
                  <Person fontSize="small" />
                </ListItemIcon>
                <Box sx={{ display: 'flex', flexDirection: 'column' }}>
                  <Typography variant="body2" sx={{ color: 'text.primary' }}>
                    {user?.full_name || user?.email}
                  </Typography>
                  <Typography variant="caption" sx={{ color: 'text.secondary' }}>
                    {user?.email}
                  </Typography>
                </Box>
              </MenuItem>
              <Divider />
              <MenuItem onClick={() => { setProfileAnchorEl(null); navigate('/profile'); }}>
                <ListItemIcon>
                  <Settings fontSize="small" />
                </ListItemIcon>
                Settings
              </MenuItem>
              <MenuItem onClick={handleLogout}>
                <ListItemIcon>
                  <Logout fontSize="small" />
                </ListItemIcon>
                Logout
              </MenuItem>
            </Menu>
          </Box>
        </Toolbar>
      </AppBar>

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
        <IconButton
          onClick={() => setAiChatOpen(false)}
          aria-label="close"
        >
          <Close />
        </IconButton>
      </DialogTitle>
      <DialogContent sx={{ p: 0, display: 'flex', flexDirection: 'column', height: '100%' }}>
        <ChatInterface />
      </DialogContent>
    </Dialog>
    </>
  );
};


