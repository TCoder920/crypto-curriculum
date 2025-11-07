/** Authentication service */
import apiClient from './api';
import type { LoginCredentials, RegisterData, TokenResponse, User } from '../types/auth';

export const authService = {
  /**
   * Login with email and password
   */
  async login(credentials: LoginCredentials): Promise<TokenResponse> {
    const response = await apiClient.post<TokenResponse>('/auth/login/json', credentials);
    return response.data;
  },

  /**
   * Register a new user
   */
  async register(data: RegisterData): Promise<User> {
    const response = await apiClient.post<User>('/auth/register', data);
    return response.data;
  },

  /**
   * Get current user information
   */
  async getCurrentUser(): Promise<User> {
    // Ensure token is available before making request
    const token = localStorage.getItem('access_token');
    if (!token) {
      throw new Error('No access token available');
    }
    
    // Let the interceptor handle adding the Authorization header
    const response = await apiClient.get<User>('/auth/me');
    return response.data;
  },

  /**
   * Refresh access token
   */
  async refreshToken(): Promise<TokenResponse> {
    const response = await apiClient.post<TokenResponse>('/auth/refresh');
    return response.data;
  },

  /**
   * Logout (client-side token removal)
   */
  async logout(): Promise<void> {
    try {
      // Only try to logout if we have a token
      const token = localStorage.getItem('access_token');
      if (token) {
        await apiClient.post('/auth/logout');
      }
    } catch (error) {
      // Ignore errors on logout - always clear client-side
    } finally {
      // Always clear client-side storage
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');
      localStorage.removeItem('token_expiry');
    }
  },

  /**
   * Update user profile
   */
  async updateProfile(data: Partial<User>): Promise<User> {
    const response = await apiClient.put<User>('/auth/me', data);
    return response.data;
  },

  /**
   * Change password
   */
  async changePassword(currentPassword: string, newPassword: string): Promise<void> {
    await apiClient.post('/auth/change-password', {
      current_password: currentPassword,
      new_password: newPassword,
    });
  },
};

