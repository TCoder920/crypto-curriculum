/** Sidebar navigation component - contains main navigation tabs */
import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import {
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Box,
  Typography,
  useMediaQuery,
  useTheme,
  IconButton,
} from '@mui/material';
import {
  Home,
  School,
  Assessment,
  TrendingUp,
  Groups,
  Menu as MenuIcon,
  Close,
} from '@mui/icons-material';
import { useAuth } from '../../contexts/AuthContext';
import { useThemeMode } from '../../contexts/ThemeContext';

const DRAWER_WIDTH = 240;

export const Sidebar: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { user } = useAuth();
  const { mode } = useThemeMode();

  const isInstructor = user?.role === 'instructor' || user?.role === 'admin';
  const isStudent = user?.role === 'student';

  const navItems = [
    { label: 'Home', path: '/', icon: <Home /> },
    { label: 'Modules', path: '/modules', icon: <School /> },
    { label: 'Assessments', path: '/assessments', icon: <Assessment /> },
    { label: 'Progress', path: '/progress', icon: <TrendingUp /> },
    ...(isStudent ? [{ label: 'Cohorts', path: '/cohorts', icon: <Groups /> }] : []),
    ...(isInstructor ? [{ label: 'Instructor', path: '/instructor', icon: <Groups /> }] : []),
  ];

  const handleNavClick = (path: string) => {
    navigate(path);
  };

  const drawerContent = (
    <Box 
      sx={{ 
        height: '100%', 
        display: 'flex', 
        flexDirection: 'column',
        overflow: 'hidden',
      }}
    >
      {/* Navigation Items */}
      <List 
        sx={{ 
          flexGrow: 1, 
          pt: 2,
          overflowY: 'auto',
          overflowX: 'hidden',
        }}
      >
        {navItems.map((item) => {
          const isActive =
            location.pathname === item.path ||
            (item.path !== '/' && location.pathname.startsWith(item.path));

          return (
            <ListItem key={item.path} disablePadding>
              <ListItemButton
                onClick={() => handleNavClick(item.path)}
                selected={isActive}
                sx={{
                  mx: 1,
                  mb: 0.5,
                  borderRadius: 2,
                  '&.Mui-selected': {
                    backgroundColor:
                      mode === 'light'
                        ? 'rgba(25, 118, 210, 0.1)'
                        : 'rgba(255, 255, 255, 0.1)',
                    color: mode === 'light' ? '#1976d2' : '#ffffff',
                    '&:hover': {
                      backgroundColor:
                        mode === 'light'
                          ? 'rgba(25, 118, 210, 0.15)'
                          : 'rgba(255, 255, 255, 0.15)',
                    },
                  },
                  '&:hover': {
                    backgroundColor:
                      mode === 'light'
                        ? 'rgba(0, 0, 0, 0.04)'
                        : 'rgba(255, 255, 255, 0.08)',
                  },
                }}
              >
                <ListItemIcon
                  sx={{
                    color: isActive
                      ? mode === 'light'
                        ? '#1976d2'
                        : '#ffffff'
                      : mode === 'light'
                      ? 'rgba(0, 0, 0, 0.7)'
                      : 'rgba(255, 255, 255, 0.7)',
                    minWidth: 40,
                  }}
                >
                  {item.icon}
                </ListItemIcon>
                <ListItemText
                  primary={item.label}
                  primaryTypographyProps={{
                    fontWeight: isActive ? 'bold' : 'normal',
                  }}
                />
              </ListItemButton>
            </ListItem>
          );
        })}
      </List>
    </Box>
  );

  return (
    <>
      {/* Desktop Sidebar - Fixed */}
      <Box
        sx={{
          display: { xs: 'none', md: 'block' },
          position: 'fixed',
          left: 0,
          top: 64,
          width: DRAWER_WIDTH,
          height: 'calc(100vh - 64px)',
          backgroundColor: mode === 'light' ? '#ffffff' : '#0a0e27',
          borderRight:
            mode === 'light'
              ? '1px solid rgba(0, 0, 0, 0.1)'
              : '1px solid rgba(255, 255, 255, 0.1)',
          zIndex: (theme) => theme.zIndex.drawer,
          overflow: 'hidden',
        }}
      >
        {drawerContent}
      </Box>

    </>
  );
};

// Export mobile menu button component separately for use in Header
export const SidebarMenuButton: React.FC = () => {
  const { mode } = useThemeMode();
  const muiTheme = useTheme();
  const isMobile = useMediaQuery(muiTheme.breakpoints.down('md'));
  const [mobileOpen, setMobileOpen] = React.useState(false);

  if (!isMobile) return null;

  return (
    <>
      <IconButton
        onClick={() => setMobileOpen(true)}
        sx={{
          color: mode === 'light' ? 'rgba(0, 0, 0, 0.7)' : 'rgba(255, 255, 255, 0.7)',
        }}
        aria-label="open navigation menu"
      >
        <MenuIcon />
      </IconButton>
      <Drawer
        variant="temporary"
        open={mobileOpen}
        onClose={() => setMobileOpen(false)}
        ModalProps={{
          keepMounted: true,
        }}
        sx={{
          '& .MuiDrawer-paper': {
            width: DRAWER_WIDTH,
            backgroundColor: mode === 'light' ? '#ffffff' : '#0a0e27',
          },
        }}
      >
        <SidebarContent onClose={() => setMobileOpen(false)} />
      </Drawer>
    </>
  );
};

// Extract drawer content to reusable component
const SidebarContent: React.FC<{ onClose?: () => void }> = ({ onClose }) => {
  const navigate = useNavigate();
  const location = useLocation();
  const { user } = useAuth();
  const { mode } = useThemeMode();
  const muiTheme = useTheme();
  const isMobile = useMediaQuery(muiTheme.breakpoints.down('md'));

  const isInstructor = user?.role === 'instructor' || user?.role === 'admin';
  const isStudent = user?.role === 'student';

  const navItems = [
    { label: 'Home', path: '/', icon: <Home /> },
    { label: 'Modules', path: '/modules', icon: <School /> },
    { label: 'Assessments', path: '/assessments', icon: <Assessment /> },
    { label: 'Progress', path: '/progress', icon: <TrendingUp /> },
    ...(isStudent ? [{ label: 'Cohorts', path: '/cohorts', icon: <Groups /> }] : []),
    ...(isInstructor ? [{ label: 'Instructor', path: '/instructor', icon: <Groups /> }] : []),
  ];

  const handleNavClick = (path: string) => {
    navigate(path);
    onClose?.();
  };

  return (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      {/* Close button for mobile */}
      {isMobile && (
        <Box
          sx={{
            p: 2,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'flex-end',
            borderBottom: mode === 'light' ? '1px solid rgba(0, 0, 0, 0.1)' : '1px solid rgba(255, 255, 255, 0.1)',
          }}
        >
          <IconButton
            onClick={onClose}
            sx={{
              color: mode === 'light' ? 'rgba(0, 0, 0, 0.7)' : 'rgba(255, 255, 255, 0.7)',
            }}
          >
            <Close />
          </IconButton>
        </Box>
      )}

      {/* Navigation Items */}
      <List 
        sx={{ 
          flexGrow: 1, 
          pt: 2,
          overflowY: 'auto',
          overflowX: 'hidden',
          '&::-webkit-scrollbar': {
            width: '8px',
          },
          '&::-webkit-scrollbar-track': {
            backgroundColor: 'transparent',
          },
          '&::-webkit-scrollbar-thumb': {
            backgroundColor: mode === 'light' ? 'rgba(0, 0, 0, 0.2)' : 'rgba(255, 255, 255, 0.2)',
            borderRadius: '4px',
            '&:hover': {
              backgroundColor: mode === 'light' ? 'rgba(0, 0, 0, 0.3)' : 'rgba(255, 255, 255, 0.3)',
            },
          },
        }}
      >
        {navItems.map((item) => {
          const isActive =
            location.pathname === item.path ||
            (item.path !== '/' && location.pathname.startsWith(item.path));

          return (
            <ListItem key={item.path} disablePadding>
              <ListItemButton
                onClick={() => handleNavClick(item.path)}
                selected={isActive}
                sx={{
                  mx: 1,
                  mb: 0.5,
                  borderRadius: 2,
                  '&.Mui-selected': {
                    backgroundColor:
                      mode === 'light'
                        ? 'rgba(25, 118, 210, 0.1)'
                        : 'rgba(255, 255, 255, 0.1)',
                    color: mode === 'light' ? '#1976d2' : '#ffffff',
                    '&:hover': {
                      backgroundColor:
                        mode === 'light'
                          ? 'rgba(25, 118, 210, 0.15)'
                          : 'rgba(255, 255, 255, 0.15)',
                    },
                  },
                  '&:hover': {
                    backgroundColor:
                      mode === 'light'
                        ? 'rgba(0, 0, 0, 0.04)'
                        : 'rgba(255, 255, 255, 0.08)',
                  },
                }}
              >
                <ListItemIcon
                  sx={{
                    color: isActive
                      ? mode === 'light'
                        ? '#1976d2'
                        : '#ffffff'
                      : mode === 'light'
                      ? 'rgba(0, 0, 0, 0.7)'
                      : 'rgba(255, 255, 255, 0.7)',
                    minWidth: 40,
                  }}
                >
                  {item.icon}
                </ListItemIcon>
                <ListItemText
                  primary={item.label}
                  primaryTypographyProps={{
                    fontWeight: isActive ? 'bold' : 'normal',
                  }}
                />
              </ListItemButton>
            </ListItem>
          );
        })}
      </List>
    </Box>
  );
};

