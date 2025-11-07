/** Token storage utilities */
import type { User } from '../types/auth';

const TOKEN_KEY = 'access_token';
const USER_KEY = 'user';
const TOKEN_EXPIRY_KEY = 'token_expiry';

export const tokenStorage = {
  /**
   * Save access token and user data
   */
  save(token: string, user: User, expiresInMinutes: number = 30): void {
    localStorage.setItem(TOKEN_KEY, token);
    localStorage.setItem(USER_KEY, JSON.stringify(user));
    
    // Calculate expiry time
    const expiry = new Date();
    expiry.setMinutes(expiry.getMinutes() + expiresInMinutes);
    localStorage.setItem(TOKEN_EXPIRY_KEY, expiry.toISOString());
  },

  /**
   * Get stored access token
   */
  getToken(): string | null {
    return localStorage.getItem(TOKEN_KEY);
  },

  /**
   * Get stored user data
   */
  getUser(): User | null {
    const userStr = localStorage.getItem(USER_KEY);
    if (!userStr) return null;
    try {
      return JSON.parse(userStr) as User;
    } catch {
      return null;
    }
  },

  /**
   * Check if token is expired
   */
  isTokenExpired(): boolean {
    const expiryStr = localStorage.getItem(TOKEN_EXPIRY_KEY);
    if (!expiryStr) return true;
    
    const expiry = new Date(expiryStr);
    return expiry < new Date();
  },

  /**
   * Clear all auth data
   */
  clear(): void {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
    localStorage.removeItem(TOKEN_EXPIRY_KEY);
  },
};

