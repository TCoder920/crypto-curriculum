/** Theme context for light/dark mode toggle */
import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { ThemeProvider, createTheme, CssBaseline } from '@mui/material';

type ThemeMode = 'light' | 'dark';

interface ThemeContextType {
  mode: ThemeMode;
  toggleTheme: () => void;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export const useThemeMode = () => {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useThemeMode must be used within ThemeContextProvider');
  }
  return context;
};

interface ThemeContextProviderProps {
  children: ReactNode;
}

export const ThemeContextProvider: React.FC<ThemeContextProviderProps> = ({ children }) => {
  // Check localStorage or system preference
  const [mode, setMode] = useState<ThemeMode>(() => {
    const saved = localStorage.getItem('theme-mode');
    if (saved === 'light' || saved === 'dark') {
      return saved as ThemeMode;
    }
    // Default to dark for now (matching current design)
    return 'dark';
  });

  // Save to localStorage and update document class
  useEffect(() => {
    localStorage.setItem('theme-mode', mode);
    document.documentElement.classList.toggle('dark', mode === 'dark');
  }, [mode]);

  const toggleTheme = () => {
    setMode((prev) => (prev === 'light' ? 'dark' : 'light'));
  };

  // Create MUI theme based on mode
  const theme = React.useMemo(
    () =>
      createTheme({
        palette: {
          mode,
          primary: {
            main: mode === 'light' ? '#1976d2' : '#4dabf7',
          },
          secondary: {
            main: mode === 'light' ? '#dc004e' : '#ff6b9d',
          },
          background: {
            default: mode === 'light' ? '#f8f9fa' : '#0a0e27',
            paper: mode === 'light' ? '#ffffff' : '#1a1f3a',
          },
          text: {
            primary: mode === 'light' ? '#212529' : '#ffffff',
            secondary: mode === 'light' ? '#6c757d' : 'rgba(255, 255, 255, 0.7)',
          },
        },
        typography: {
          fontFamily: 'Inter, system-ui, Avenir, Helvetica, Arial, sans-serif',
        },
      }),
    [mode]
  );

  return (
    <ThemeContext.Provider value={{ mode, toggleTheme }}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        {children}
      </ThemeProvider>
    </ThemeContext.Provider>
  );
};

