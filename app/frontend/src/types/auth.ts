/** Authentication types */
export interface User {
  id: number;
  email: string;
  username: string | null;
  full_name: string | null;
  role: 'student' | 'instructor' | 'admin';
  is_active: boolean;
  is_verified: boolean;
  last_login: string | null;
  created_at: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  password: string;
  username?: string;
  full_name?: string;
  // Role is always 'student' - set by backend for security
  // Admin and instructor roles can only be assigned via seed script or admin endpoint
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export interface AuthContextType {
  user: User | null;
  token: string | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  login: (credentials: LoginCredentials) => Promise<void>;
  register: (data: RegisterData) => Promise<void>;
  logout: () => void;
  refreshUser: () => Promise<void>;
}

