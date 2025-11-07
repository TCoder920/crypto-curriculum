/** Register page */
import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { motion } from 'framer-motion';
import { TextField, Button, Alert, Box, Typography, MenuItem } from '@mui/material';
import { PersonAdd as PersonAddIcon } from '@mui/icons-material';

export const RegisterPage: React.FC = () => {
  const navigate = useNavigate();
  const { register, isAuthenticated } = useAuth();
  
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: '',
    username: '',
    full_name: '',
    role: 'student' as 'student' | 'instructor' | 'admin',
  });
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  // Redirect if already authenticated
  React.useEffect(() => {
    if (isAuthenticated) {
      navigate('/', { replace: true });
    }
  }, [isAuthenticated, navigate]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    // Validation
    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    if (formData.password.length < 8) {
      setError('Password must be at least 8 characters');
      return;
    }

    setIsLoading(true);

    try {
      await register({
        email: formData.email,
        password: formData.password,
        username: formData.username || undefined,
        full_name: formData.full_name || undefined,
        role: formData.role,
      });
      
      // Wait a moment for state to update, then navigate
      // The ProtectedRoute will check token directly if state hasn't updated yet
      setTimeout(() => {
        navigate('/', { replace: true });
      }, 100);
    } catch (err: any) {
      // Handle validation errors (422)
      if (err.response?.status === 422) {
        const validationErrors = err.response?.data?.detail;
        if (Array.isArray(validationErrors)) {
          const errorMessages = validationErrors.map((e: any) => `${e.loc?.join('.')}: ${e.msg}`).join(', ');
          setError(`Validation error: ${errorMessages}`);
        } else {
          setError(err.response?.data?.detail || 'Validation error. Please check your input.');
        }
      } else {
        setError(err.response?.data?.detail || 'Registration failed. Please try again.');
      }
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-purple-50 dark:from-gray-900 dark:to-blue-900 p-4">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="w-full max-w-md"
      >
        <div className="glass-surface rounded-3xl p-8">
          <Box className="text-center mb-8">
            <PersonAddIcon sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
            <Typography variant="h4" component="h1" className="font-bold mb-2">
              Create Account
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Join the Crypto Curriculum Platform
            </Typography>
          </Box>

          {error && (
            <Alert severity="error" className="mb-4">
              {typeof error === 'string' ? error : JSON.stringify(error)}
            </Alert>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <TextField
              fullWidth
              label="Email"
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
              autoComplete="email"
              autoFocus
            />

            <TextField
              fullWidth
              label="Password"
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              required
              autoComplete="new-password"
              helperText="Must be at least 8 characters"
            />

            <TextField
              fullWidth
              label="Confirm Password"
              type="password"
              name="confirmPassword"
              value={formData.confirmPassword}
              onChange={handleChange}
              required
              autoComplete="new-password"
            />

            <TextField
              fullWidth
              label="Username (optional)"
              name="username"
              value={formData.username}
              onChange={handleChange}
              autoComplete="username"
            />

            <TextField
              fullWidth
              label="Full Name (optional)"
              name="full_name"
              value={formData.full_name}
              onChange={handleChange}
              autoComplete="name"
            />

            <TextField
              fullWidth
              select
              label="Role"
              name="role"
              value={formData.role}
              onChange={handleChange}
              required
            >
              <MenuItem value="student">Student</MenuItem>
              <MenuItem value="instructor">Instructor</MenuItem>
              <MenuItem value="admin">Admin</MenuItem>
            </TextField>

            <Button
              type="submit"
              fullWidth
              variant="contained"
              size="large"
              disabled={isLoading}
              className="mt-6"
            >
              {isLoading ? 'Creating account...' : 'Sign Up'}
            </Button>
          </form>

          <Box className="mt-6 text-center">
            <Typography variant="body2" color="text.secondary">
              Already have an account?{' '}
              <Link to="/login" className="text-primary hover:underline">
                Sign in
              </Link>
            </Typography>
          </Box>
        </div>
      </motion.div>
    </div>
  );
};

