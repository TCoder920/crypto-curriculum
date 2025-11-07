/** Home page */
import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { motion } from 'framer-motion';
import { Button, Box, Typography, Card, CardContent } from '@mui/material';
import { School, Assessment, TrendingUp, Logout } from '@mui/icons-material';

export const HomePage: React.FC = () => {
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 dark:from-gray-900 dark:to-blue-900 p-4">
      <div className="container mx-auto max-w-6xl">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          {/* Header */}
          <div className="glass-surface rounded-3xl p-6 mb-6">
            <div className="flex justify-between items-center">
              <div>
                <Typography variant="h4" component="h1" className="font-bold mb-2">
                  Crypto Curriculum Platform
                </Typography>
                <Typography variant="body1" color="text.secondary">
                  Welcome back, {user?.full_name || user?.email || 'User'}!
                </Typography>
                <Typography variant="body2" color="text.secondary" className="mt-1">
                  Role: {user?.role || 'student'}
                </Typography>
              </div>
              <Button
                variant="outlined"
                startIcon={<Logout />}
                onClick={handleLogout}
                className="ml-4"
              >
                Logout
              </Button>
            </div>
          </div>

          {/* Feature Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <motion.div
              whileHover={{ scale: 1.05 }}
              transition={{ duration: 0.2 }}
            >
              <Card className="glass-surface rounded-3xl">
                <CardContent className="p-6 text-center">
                  <School sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
                  <Typography variant="h6" component="h2" className="font-bold mb-2">
                    Learn
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Explore 17 comprehensive modules on blockchain and cryptocurrency
                  </Typography>
                </CardContent>
              </Card>
            </motion.div>

            <motion.div
              whileHover={{ scale: 1.05 }}
              transition={{ duration: 0.2 }}
            >
              <Card className="glass-surface rounded-3xl">
                <CardContent className="p-6 text-center">
                  <Assessment sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
                  <Typography variant="h6" component="h2" className="font-bold mb-2">
                    Assess
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Test your knowledge with 170+ assessment questions
                  </Typography>
                </CardContent>
              </Card>
            </motion.div>

            <motion.div
              whileHover={{ scale: 1.05 }}
              transition={{ duration: 0.2 }}
            >
              <Card className="glass-surface rounded-3xl">
                <CardContent className="p-6 text-center">
                  <TrendingUp sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
                  <Typography variant="h6" component="h2" className="font-bold mb-2">
                    Track Progress
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Monitor your learning journey and achievements
                  </Typography>
                </CardContent>
              </Card>
            </motion.div>
          </div>

          {/* Status */}
          <Box className="mt-8 text-center">
            <Typography variant="body2" color="text.secondary">
              Phase 3: Authentication & User Management - Complete
            </Typography>
          </Box>
        </motion.div>
      </div>
    </div>
  );
};

