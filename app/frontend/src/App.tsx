import { Routes, Route, Navigate } from 'react-router-dom'
import { Box } from '@mui/material'
import { ThemeContextProvider, useThemeMode } from './contexts/ThemeContext'
import { ProtectedRoute } from './components/auth/ProtectedRoute'
import { Navigation } from './components/layout/Navigation'
import { LoginPage } from './pages/LoginPage'
import { RegisterPage } from './pages/RegisterPage'
import { HomePage } from './pages/HomePage'
import { ModulesListPage } from './pages/ModulesListPage'
import { AssessmentsListPage } from './pages/AssessmentsListPage'
import { ModulePage } from './pages/ModulePage'
import { AssessmentPage } from './pages/AssessmentPage'
import { ProgressPage } from './pages/ProgressPage'
import { ProfileSettingsPage } from './pages/ProfileSettingsPage'
import { InstructorDashboardPage } from './pages/InstructorDashboardPage'
import './App.css'

function AppContent() {
  const { mode } = useThemeMode();
  const backgroundColor = mode === 'light' ? '#f8f9fa' : '#0a0e27';

  return (
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route
          path="/*"
          element={
            <ProtectedRoute>
            <Box sx={{ minHeight: '100vh', backgroundColor }}>
                <Navigation />
                <Routes>
                  <Route path="/" element={<HomePage />} />
                  <Route path="/modules" element={<ModulesListPage />} />
                  <Route path="/assessments" element={<AssessmentsListPage />} />
                <Route path="/progress" element={<ProgressPage />} />
                <Route path="/profile" element={<ProfileSettingsPage />} />
                <Route path="/settings" element={<ProfileSettingsPage />} />
                <Route path="/instructor" element={<InstructorDashboardPage />} />
                  <Route path="/modules/:moduleId" element={<ModulePage />} />
                  <Route path="/modules/:moduleId/assessments" element={<AssessmentPage />} />
                  <Route path="*" element={<Navigate to="/" replace />} />
                </Routes>
              </Box>
            </ProtectedRoute>
          }
        />
      </Routes>
  )
}

function App() {
  return (
    <ThemeContextProvider>
      <AppContent />
    </ThemeContextProvider>
  )
}

export default App
