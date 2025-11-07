/** Authentication context */
import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { authService } from '../services/authService';
import { tokenStorage } from '../utils/tokenStorage';
import type { AuthContextType, LoginCredentials, RegisterData, User } from '../types/auth';

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Initialize auth state from localStorage
  useEffect(() => {
    const initAuth = async () => {
      const storedToken = tokenStorage.getToken();
      const storedUser = tokenStorage.getUser();

      if (storedToken && storedUser && !tokenStorage.isTokenExpired()) {
        // Set token in localStorage for interceptor BEFORE making API calls
        localStorage.setItem('access_token', storedToken);
        setToken(storedToken);
        setUser(storedUser);
        
        // Refresh user data from server
        try {
          const currentUser = await authService.getCurrentUser();
          setUser(currentUser);
          tokenStorage.save(storedToken, currentUser);
        } catch (error) {
          // Token might be invalid, clear storage
          tokenStorage.clear();
          localStorage.removeItem('access_token');
          setToken(null);
          setUser(null);
        }
      } else {
        tokenStorage.clear();
        localStorage.removeItem('access_token');
      }
      
      setIsLoading(false);
    };

    initAuth();
  }, []);

  const login = async (credentials: LoginCredentials) => {
    try {
      // Step 1: Login and get token
      const tokenResponse = await authService.login(credentials);
      
      // Step 2: Save token to localStorage immediately so interceptor can use it
      const token = tokenResponse.access_token;
      localStorage.setItem('access_token', token);
      
      // Step 3: Wait a tiny bit to ensure localStorage is written
      await new Promise(resolve => setTimeout(resolve, 10));
      
      // Step 4: Now get user data (token is now available in interceptor)
      const userData = await authService.getCurrentUser();
      
      // Step 5: Save complete auth data
      tokenStorage.save(token, userData);
      setToken(token);
      setUser(userData);
    } catch (error) {
      // Clear token on error
      localStorage.removeItem('access_token');
      tokenStorage.clear();
      throw error;
    }
  };

  const register = async (data: RegisterData) => {
    try {
      // Step 1: Register user
      await authService.register(data);
      
      // Step 2: Auto-login after registration
      const loginResponse = await authService.login({
        email: data.email,
        password: data.password,
      });
      
      // Step 3: Save token immediately
      const token = loginResponse.access_token;
      localStorage.setItem('access_token', token);
      
      // Step 4: Wait a tiny bit to ensure localStorage is written
      await new Promise(resolve => setTimeout(resolve, 10));
      
      // Step 5: Get user data
      const userData = await authService.getCurrentUser();
      
      // Step 6: Save complete auth data
      tokenStorage.save(token, userData);
      setToken(token);
      setUser(userData);
    } catch (error) {
      // Clear token on error
      localStorage.removeItem('access_token');
      tokenStorage.clear();
      throw error;
    }
  };

  const logout = async () => {
    try {
      // Try to logout on server (may fail if token already invalid)
      await authService.logout();
    } catch (error) {
      // Ignore errors - logout is client-side anyway
    } finally {
      // Always clear client-side storage
      tokenStorage.clear();
      localStorage.removeItem('access_token');
      setToken(null);
      setUser(null);
    }
  };

  const refreshUser = async () => {
    try {
      const userData = await authService.getCurrentUser();
      setUser(userData);
      
      const storedToken = tokenStorage.getToken();
      if (storedToken) {
        tokenStorage.save(storedToken, userData);
      }
    } catch (error) {
      // If refresh fails, logout
      await logout();
      throw error;
    }
  };

  const value: AuthContextType = {
    user,
    token,
    isLoading,
    isAuthenticated: !!user && !!token && !tokenStorage.isTokenExpired(),
    login,
    register,
    logout,
    refreshUser,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

