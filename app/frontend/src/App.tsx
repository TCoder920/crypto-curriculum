import { Routes, Route, Navigate } from 'react-router-dom'
import { Box } from '@mui/material'
import { ThemeContextProvider, useThemeMode } from './contexts/ThemeContext'
import { ProtectedRoute } from './components/auth/ProtectedRoute'
import { Navigation } from './components/layout/Navigation'
import { Sidebar } from './components/layout/Sidebar'
import { Footer } from './components/layout/Footer'
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
import { CohortsPage } from './pages/CohortsPage'
import { ForumPage } from './pages/ForumPage'
import { ForumPostPage } from './pages/ForumPostPage'
import { AIAssistantPage } from './pages/AIAssistantPage'
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
            <Box sx={{ minHeight: '100vh', backgroundColor, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
                <Navigation />
                <Box sx={{ flexGrow: 1, minWidth: 0, overflow: 'hidden', position: 'relative' }}>
                  <Sidebar />
                  <Box 
                    sx={{ 
                      flexGrow: 1, 
                      display: 'flex', 
                      flexDirection: 'column', 
                      minWidth: 0,
                      overflowY: 'auto',
                      overflowX: 'hidden',
                      height: 'calc(100vh - 64px)',
                      position: 'relative',
                      width: { xs: '100%', md: 'calc(100% - 240px)' },
                      ml: { xs: 0, md: '240px' },
                    }}
                  >
                    <Box sx={{ flexGrow: 1, pb: 4 }}>
                      <Routes>
                        <Route path="/" element={<HomePage />} />
                        <Route path="/modules" element={<ModulesListPage />} />
                        <Route path="/assessments" element={<AssessmentsListPage />} />
                        <Route path="/progress" element={<ProgressPage />} />
                        <Route path="/profile" element={<ProfileSettingsPage />} />
                        <Route path="/settings" element={<ProfileSettingsPage />} />
                        <Route path="/instructor" element={<InstructorDashboardPage />} />
                        <Route path="/cohorts" element={<CohortsPage />} />
                        <Route path="/modules/:moduleId" element={<ModulePage />} />
                        <Route path="/modules/:moduleId/assessments" element={<AssessmentPage />} />
                        <Route path="/modules/:moduleId/forums" element={<ForumPage />} />
                        <Route path="/modules/:moduleId/forums/posts/:postId" element={<ForumPostPage />} />
                        <Route path="/ai-assistant" element={<AIAssistantPage />} />
                        <Route path="*" element={<Navigate to="/" replace />} />
                      </Routes>
                    </Box>
                    <Footer />
                  </Box>
                </Box>
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
