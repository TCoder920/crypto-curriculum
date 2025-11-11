import { Routes, Route, Navigate } from 'react-router-dom'
import { ThemeProvider, createTheme, CssBaseline, Box } from '@mui/material'
import { ProtectedRoute } from './components/auth/ProtectedRoute'
import { Navigation } from './components/layout/Navigation'
import { LoginPage } from './pages/LoginPage'
import { RegisterPage } from './pages/RegisterPage'
import { HomePage } from './pages/HomePage'
import { ModulesListPage } from './pages/ModulesListPage'
import { AssessmentsListPage } from './pages/AssessmentsListPage'
import { ModulePage } from './pages/ModulePage'
import { AssessmentPage } from './pages/AssessmentPage'
import './App.css'

// Create MUI theme with dark mode
const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
    background: {
      default: '#0a0e27',
      paper: '#1a1f3a',
    },
  },
})

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route
          path="/*"
          element={
            <ProtectedRoute>
              <Box sx={{ minHeight: '100vh', backgroundColor: '#0a0e27' }}>
                <Navigation />
                <Routes>
                  <Route path="/" element={<HomePage />} />
                  <Route path="/modules" element={<ModulesListPage />} />
                  <Route path="/assessments" element={<AssessmentsListPage />} />
                  <Route path="/modules/:moduleId" element={<ModulePage />} />
                  <Route path="/modules/:moduleId/assessments" element={<AssessmentPage />} />
                  <Route path="*" element={<Navigate to="/" replace />} />
                </Routes>
              </Box>
            </ProtectedRoute>
          }
        />
      </Routes>
    </ThemeProvider>
  )
}

export default App
