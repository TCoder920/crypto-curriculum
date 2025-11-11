/** Home page - Overview/Dashboard with dark theme */
import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { useThemeMode } from '../contexts/ThemeContext';
import { motion } from 'framer-motion';
import { Button, Box, Typography, Card, CardContent, Container } from '@mui/material';
import { School, Assessment, TrendingUp, ArrowForward } from '@mui/icons-material';

export const HomePage: React.FC = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const { mode } = useThemeMode();
  const backgroundColor = mode === 'light' ? '#f8f9fa' : '#0a0e27';

  const learningTracks = [
    {
      title: 'User Track',
      modules: 7,
      description: 'Foundations of blockchain and Web3',
      goal: 'Create an informed, safe, and competent user of Web3',
    },
    {
      title: 'Power User/Analyst Track',
      modules: 3,
      description: 'On-chain analysis and advanced DeFi',
      goal: 'Bridge the gap from using the chain to analyzing it',
    },
    {
      title: 'Developer Track',
      modules: 3,
      description: 'Smart contract and dApp development',
      goal: 'Build technical skills required to create smart contracts and dApps',
    },
    {
      title: 'Architect/Builder Track',
      modules: 4,
      description: 'Building complex systems and AI applications',
      goal: 'Use developer skills to build complex, novel systems',
    },
  ];

  return (
    <Box sx={{ minHeight: '100vh', backgroundColor, py: 4 }}>
      <Container maxWidth="lg">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          {/* Hero Section */}
          <Card
            className="glass-surface"
            sx={{
              borderRadius: 3,
              p: 4,
              mb: 4,
            }}
          >
            <Box sx={{ textAlign: 'center', mb: 4 }}>
              <Typography
                variant="h3"
                component="h1"
                sx={{
                  fontWeight: 'bold',
                  mb: 2,
                  color: 'text.primary',
                }}
              >
                Master Blockchain & Cryptocurrency
              </Typography>
              <Typography
                variant="body1"
                sx={{
                  color: mode === 'light' ? 'text.secondary' : 'rgba(255, 255, 255, 0.9)',
                  mb: 4,
                  maxWidth: '600px',
                  mx: 'auto',
                }}
              >
                Explore 17 comprehensive modules covering everything from blockchain fundamentals to advanced trading strategies. 
                Learn at your own pace with interactive lessons and assessments.
              </Typography>
              <Typography
                variant="body2"
                sx={{
                  color: mode === 'light' ? 'text.secondary' : 'rgba(255, 255, 255, 0.7)',
                  mb: 4,
                }}
              >
                Welcome back, {user?.full_name || user?.email || 'learner'}!
              </Typography>
              <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center', flexWrap: 'wrap' }}>
                <Button
                  variant="contained"
                  size="large"
                  endIcon={<ArrowForward />}
                  onClick={() => navigate('/modules')}
                  sx={{
                    backgroundColor: '#1976d2',
                    color: 'text.primary',
                    fontWeight: 'bold',
                    px: 4,
                    py: 1.5,
                    '&:hover': {
                      backgroundColor: '#1565c0',
                    },
                  }}
                >
                  START LEARNING
                </Button>
                <Button
                  variant="outlined"
                  size="large"
                  endIcon={<Assessment />}
                  onClick={() => navigate('/assessments')}
                  sx={{
                  borderColor: mode === 'light' ? 'divider' : 'rgba(255, 255, 255, 0.5)',
                    color: 'text.primary',
                    fontWeight: 'bold',
                    px: 4,
                    py: 1.5,
                    '&:hover': {
                    borderColor: mode === 'light' ? 'text.primary' : '#ffffff',
                    backgroundColor: mode === 'light' ? 'rgba(0,0,0,0.04)' : 'rgba(255, 255, 255, 0.1)',
                    },
                  }}
                >
                  ASSESS YOUR SKILLS
                </Button>
              </Box>
            </Box>
          </Card>

          {/* Stats Section */}
          <Box
            sx={{
              display: 'grid',
              gridTemplateColumns: { xs: '1fr', sm: 'repeat(4, 1fr)' },
              gap: 2,
              mb: 4,
            }}
          >
            {[
              { label: 'Comprehensive Modules', value: '17' },
              { label: 'Assessment Questions', value: '170+' },
              { label: 'Learning Tracks', value: '4' },
              { label: 'Total Hours', value: '40+' },
            ].map((stat, index) => (
              <Card
                key={index}
                className="glass-surface"
                sx={{
                  borderRadius: 2,
                  p: 2,
                  textAlign: 'center',
                }}
              >
                <Typography
                  variant="h4"
                  sx={{
                    fontWeight: 'bold',
                    color: 'text.primary',
                    mb: 0.5,
                  }}
                >
                  {stat.value}
                </Typography>
                <Typography
                  variant="body2"
                  sx={{
                    color: mode === 'light' ? 'text.secondary' : 'rgba(255, 255, 255, 0.8)',
                    fontSize: '0.875rem',
                  }}
                >
                  {stat.label}
                </Typography>
              </Card>
            ))}
          </Box>

          {/* Feature Cards */}
          <Box
            sx={{
              display: 'grid',
              gridTemplateColumns: { xs: '1fr', md: 'repeat(3, 1fr)' },
              gap: 3,
              mb: 4,
            }}
          >
            {[
              {
                icon: <School sx={{ fontSize: 48, color: '#1976d2' }} />,
                title: 'Learn',
                description: 'Explore 17 comprehensive modules covering blockchain technology, cryptocurrency, trading, and more.',
              },
              {
                icon: <Assessment sx={{ fontSize: 48, color: '#1976d2' }} />,
                title: 'Assess',
                description: 'Test your knowledge with 170+ assessment questions across all modules. Track your progress and master each topic.',
              },
              {
                icon: <TrendingUp sx={{ fontSize: 48, color: '#1976d2' }} />,
                title: 'Track Progress',
                description: 'Monitor your learning journey, view completion statistics, and track achievements.',
              },
            ].map((feature, index) => (
              <Card
                key={index}
                className="glass-surface"
                sx={{
                  borderRadius: 3,
                  p: 3,
                  textAlign: 'center',
                }}
              >
                <Box sx={{ mb: 2 }}>{feature.icon}</Box>
                <Typography
                  variant="h6"
                  sx={{
                    fontWeight: 'bold',
                    color: 'text.primary',
                    mb: 1,
                  }}
                >
                  {feature.title}
                </Typography>
                <Typography
                  variant="body2"
                  sx={{
                    color: mode === 'light' ? 'text.secondary' : 'rgba(255, 255, 255, 0.8)',
                  }}
                >
                  {feature.description}
                </Typography>
              </Card>
            ))}
          </Box>

          {/* Learning Tracks Section */}
          <Box sx={{ mb: 4 }}>
            <Typography
              variant="h5"
              sx={{
                fontWeight: 'bold',
                color: 'text.primary',
                mb: 3,
                textAlign: 'center',
              }}
            >
              Learning Tracks
            </Typography>
            <Box
              sx={{
                display: 'grid',
                gridTemplateColumns: { xs: '1fr', md: 'repeat(2, 1fr)' },
                gap: 3,
              }}
            >
              {learningTracks.map((track, index) => (
                <Card
                  key={index}
                  className="glass-surface"
                  sx={{
                    borderRadius: 3,
                    p: 3,
                  }}
                >
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', mb: 2 }}>
                    <Box>
                      <Typography
                        variant="h6"
                        sx={{
                          fontWeight: 'bold',
                          color: 'text.primary',
                          mb: 1,
                        }}
                      >
                        {track.title}
                      </Typography>
                      <Typography
                        variant="body2"
                        sx={{
                          color: mode === 'light' ? 'text.secondary' : 'rgba(255, 255, 255, 0.8)',
                          mb: 1,
                        }}
                      >
                        {track.description}
                      </Typography>
                      <Typography
                        variant="caption"
                        sx={{
                          color: mode === 'light' ? 'text.secondary' : 'rgba(255, 255, 255, 0.6)',
                        }}
                      >
                        {track.goal}
                      </Typography>
                    </Box>
                    <Button
                      variant="contained"
                      size="small"
                      sx={{
                        backgroundColor: '#1976d2',
                        color: 'text.primary',
                        minWidth: 'auto',
                        px: 2,
                        py: 0.5,
                        borderRadius: 2,
                      }}
                    >
                      {track.modules} modules
                    </Button>
                  </Box>
                </Card>
              ))}
            </Box>
          </Box>
        </motion.div>
      </Container>
    </Box>
  );
};
