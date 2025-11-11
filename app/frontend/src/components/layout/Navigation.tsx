/** Navigation bar component - visible across all pages */
import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { AppBar, Toolbar, Button, Box, Typography } from '@mui/material';
import { Home, School, Assessment, TrendingUp, Logout } from '@mui/icons-material';
import { useAuth } from '../../contexts/AuthContext';

export const Navigation: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { user, logout } = useAuth();

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  const navItems = [
    { label: 'HOME', path: '/', icon: <Home /> },
    { label: 'MODULES', path: '/modules', icon: <School /> },
    { label: 'ASSESSMENTS', path: '/assessments', icon: <Assessment /> },
    { label: 'PROGRESS', path: '/progress', icon: <TrendingUp /> },
  ];

  return (
    <AppBar 
      position="sticky" 
      sx={{ 
        backgroundColor: '#0a0e27',
        borderBottom: '1px solid rgba(255, 255, 255, 0.1)',
        boxShadow: 'none',
      }}
    >
      <Toolbar sx={{ justifyContent: 'space-between', px: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <Typography 
            variant="h6" 
            component="div" 
            sx={{ 
              fontWeight: 'bold',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: 1,
            }}
            onClick={() => navigate('/')}
          >
            <School sx={{ fontSize: 28 }} />
            Crypto Curriculum
          </Typography>
        </Box>

        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          {navItems.map((item) => {
            const isActive = location.pathname === item.path || 
              (item.path !== '/' && location.pathname.startsWith(item.path));
            
            return (
              <Button
                key={item.path}
                startIcon={item.icon}
                onClick={() => navigate(item.path)}
                sx={{
                  color: isActive ? '#ffffff' : 'rgba(255, 255, 255, 0.7)',
                  fontWeight: isActive ? 'bold' : 'normal',
                  borderBottom: isActive ? '2px solid #ffffff' : '2px solid transparent',
                  borderRadius: 0,
                  px: 2,
                  py: 1,
                  '&:hover': {
                    color: '#ffffff',
                    backgroundColor: 'rgba(255, 255, 255, 0.1)',
                  },
                }}
              >
                {item.label}
              </Button>
            );
          })}
          
          <Button
            startIcon={<Logout />}
            onClick={handleLogout}
            sx={{
              color: 'rgba(255, 255, 255, 0.7)',
              ml: 2,
              '&:hover': {
                color: '#ffffff',
                backgroundColor: 'rgba(255, 255, 255, 0.1)',
              },
            }}
          >
            Logout
          </Button>
        </Box>
      </Toolbar>
    </AppBar>
  );
};


