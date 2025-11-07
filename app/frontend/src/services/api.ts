/** API client configuration */
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:9000';

export const apiClient = axios.create({
  baseURL: `${API_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
apiClient.interceptors.request.use(
  (config) => {
    // Always read fresh token from localStorage (don't cache)
    const token = localStorage.getItem('access_token');
    if (token) {
      // Ensure Authorization header is set correctly
      config.headers = config.headers || {};
      config.headers.Authorization = `Bearer ${token}`;
      // Debug: log token being sent (remove in production)
      console.log('Sending request with token:', token.substring(0, 20) + '...');
    } else {
      // Remove Authorization header if no token
      if (config.headers) {
        delete config.headers.Authorization;
      }
      console.warn('No token found in localStorage');
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle errors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid - but don't redirect if we're already on login/register
      const currentPath = window.location.pathname;
      if (currentPath !== '/login' && currentPath !== '/register') {
        localStorage.removeItem('access_token');
        localStorage.removeItem('user');
        localStorage.removeItem('token_expiry');
        // Only redirect if not already on auth pages
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

export default apiClient;

