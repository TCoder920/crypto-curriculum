/** Login page */
import React, { useState } from 'react';
import { useNavigate, useLocation, Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { motion } from 'framer-motion';
import { TextField, Button, Alert, Box, Typography } from '@mui/material';
import { Login as LoginIcon } from '@mui/icons-material';

export const LoginPage: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { login, isAuthenticated } = useAuth();
  
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  // Redirect if already authenticated
  React.useEffect(() => {
    if (isAuthenticated) {
      const from = (location.state as any)?.from?.pathname || '/';
      navigate(from, { replace: true });
    }
  }, [isAuthenticated, navigate, location]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      await login({ email, password });
      const from = (location.state as any)?.from?.pathname || '/';
      // Wait a moment for state to update, then navigate
      setTimeout(() => {
        navigate(from, { replace: true });
      }, 100);
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || err.message || 'Login failed. Please check your credentials.';
      setError(typeof errorMessage === 'string' ? errorMessage : JSON.stringify(errorMessage));
      setIsLoading(false);
    }
  };

  return (
    <Box
      sx={{
        minHeight: "100vh",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        p: { xs: 2, sm: 3, md: 4 },
        width: "100%",
        maxWidth: "100vw",
        overflowX: "hidden",
      }}
    >
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <Box
          sx={{
            background: "rgba(22, 27, 34, 0.8)",
            backdropFilter: "blur(20px)",
            borderRadius: 4,
            p: 4,
            width: "100%",
            maxWidth: 400,
            border: "1px solid rgba(255, 255, 255, 0.1)",
          }}
        >
          <Box className="text-center mb-8">
            <LoginIcon sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
            <Typography variant="h4" component="h1" className="font-bold mb-2">
              Welcome Back
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Sign in to continue your learning journey
            </Typography>
          </Box>

          {error && (
            <Alert severity="error" className="mb-4">
              {error}
            </Alert>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <TextField
              fullWidth
              label="Email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              autoComplete="email"
              autoFocus
            />

            <TextField
              fullWidth
              label="Password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              autoComplete="current-password"
            />

            <Button
              type="submit"
              fullWidth
              variant="contained"
              size="large"
              disabled={isLoading}
              className="mt-6"
            >
              {isLoading ? 'Signing in...' : 'Sign In'}
            </Button>
          </form>

          <Box className="mt-6 text-center">
            <Typography variant="body2" color="text.secondary">
              Don't have an account?{' '}
              <Link to="/register" className="text-primary hover:underline">
                Sign up
              </Link>
            </Typography>
          </Box>
        </Box>
      </motion.div>
    </Box>
  );
};

