/** Instructor Dashboard Page */
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { useThemeMode } from '../contexts/ThemeContext';
import { motion } from 'framer-motion';
import {
  Box,
  Container,
  Typography,
  Card,
  CardContent,
  Tabs,
  Tab,
  Button,
  Alert,
  Grid,
} from '@mui/material';
import {
  Groups,
  Assignment,
  People,
  Assessment,
  TrendingUp,
} from '@mui/icons-material';
import { cohortService, type Cohort } from '../services/cohortService';
import { gradingService, type GradingQueueItem } from '../services/gradingService';
import { CohortManagement } from '../components/instructor/CohortManagement';
import { StudentList } from '../components/instructor/StudentList';
import { GradingQueue } from '../components/instructor/GradingQueue';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;
  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`instructor-tabpanel-${index}`}
      aria-labelledby={`instructor-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ pt: 3 }}>{children}</Box>}
    </div>
  );
}

export const InstructorDashboardPage: React.FC = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const { mode } = useThemeMode();
  const [tabValue, setTabValue] = useState(0);
  const [cohorts, setCohorts] = useState<Cohort[]>([]);
  const [gradingQueue, setGradingQueue] = useState<GradingQueueItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const backgroundColor = mode === 'light' ? '#f8f9fa' : '#0a0e27';

  // Check if user is instructor or admin
  const isInstructor = user?.role === 'instructor' || user?.role === 'admin';

  useEffect(() => {
    if (!isInstructor) {
      navigate('/');
      return;
    }

    loadDashboardData();
  }, [isInstructor, navigate]);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      setError(null);

      // Load cohorts
      const cohortsData = await cohortService.getCohorts();
      setCohorts(cohortsData.cohorts);

      // Load grading queue
      const queueData = await gradingService.getGradingQueue(10, 0);
      setGradingQueue(queueData.items);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  const handleTabChange = (_event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  if (!isInstructor) {
    return null;
  }

  // Calculate statistics
  const totalCohorts = cohorts.length;
  const activeCohorts = cohorts.filter((c) => c.is_active).length;
  const totalStudents = cohorts.reduce((sum, c) => sum + c.student_count, 0);
  const pendingGrading = gradingQueue.length;

  return (
    <Box sx={{ minHeight: '100vh', backgroundColor, py: 4 }}>
      <Container maxWidth="xl">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          {/* Header */}
          <Box sx={{ mb: 4 }}>
            <Typography
              variant="h4"
              component="h1"
              sx={{
                fontWeight: 'bold',
                color: 'text.primary',
                mb: 1,
              }}
            >
              Instructor Dashboard
            </Typography>
            <Typography
              variant="body1"
              sx={{
                color: mode === 'light' ? 'text.secondary' : 'rgba(255, 255, 255, 0.8)',
              }}
            >
              Manage cohorts, students, and assessments
            </Typography>
          </Box>

          {error && (
            <Alert severity="error" sx={{ mb: 3 }} onClose={() => setError(null)}>
              <Typography variant="body2">{error}</Typography>
            </Alert>
          )}

          {/* Statistics Cards */}
          <Grid container spacing={3} sx={{ mb: 4 }}>
            <Grid item xs={12} sm={6} md={3}>
              <Card className="glass-surface" sx={{ borderRadius: 2, p: 2 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                  <Groups sx={{ fontSize: 40, color: '#1976d2' }} />
                  <Box>
                    <Typography variant="h4" sx={{ fontWeight: 'bold', color: 'text.primary' }}>
                      {totalCohorts}
                    </Typography>
                    <Typography variant="body2" sx={{ color: 'text.secondary' }}>
                      Total Cohorts
                    </Typography>
                  </Box>
                </Box>
              </Card>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Card className="glass-surface" sx={{ borderRadius: 2, p: 2 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                  <People sx={{ fontSize: 40, color: '#1976d2' }} />
                  <Box>
                    <Typography variant="h4" sx={{ fontWeight: 'bold', color: 'text.primary' }}>
                      {totalStudents}
                    </Typography>
                    <Typography variant="body2" sx={{ color: 'text.secondary' }}>
                      Total Students
                    </Typography>
                  </Box>
                </Box>
              </Card>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Card className="glass-surface" sx={{ borderRadius: 2, p: 2 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                  <Assessment sx={{ fontSize: 40, color: '#1976d2' }} />
                  <Box>
                    <Typography variant="h4" sx={{ fontWeight: 'bold', color: 'text.primary' }}>
                      {pendingGrading}
                    </Typography>
                    <Typography variant="body2" sx={{ color: 'text.secondary' }}>
                      Pending Grading
                    </Typography>
                  </Box>
                </Box>
              </Card>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Card className="glass-surface" sx={{ borderRadius: 2, p: 2 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                  <TrendingUp sx={{ fontSize: 40, color: '#1976d2' }} />
                  <Box>
                    <Typography variant="h4" sx={{ fontWeight: 'bold', color: 'text.primary' }}>
                      {activeCohorts}
                    </Typography>
                    <Typography variant="body2" sx={{ color: 'text.secondary' }}>
                      Active Cohorts
                    </Typography>
                  </Box>
                </Box>
              </Card>
            </Grid>
          </Grid>

          {/* Tabs */}
          <Card className="glass-surface" sx={{ borderRadius: 3 }}>
            <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
              <Tabs value={tabValue} onChange={handleTabChange}>
                <Tab label="Cohorts" icon={<Groups />} iconPosition="start" />
                <Tab label="Students" icon={<People />} iconPosition="start" />
                <Tab label="Grading Queue" icon={<Assignment />} iconPosition="start" />
              </Tabs>
            </Box>

            <TabPanel value={tabValue} index={0}>
              <CohortManagement cohorts={cohorts} onRefresh={loadDashboardData} />
            </TabPanel>

            <TabPanel value={tabValue} index={1}>
              <StudentList cohorts={cohorts} />
            </TabPanel>

            <TabPanel value={tabValue} index={2}>
              <GradingQueue queue={gradingQueue} onRefresh={loadDashboardData} />
            </TabPanel>
          </Card>
        </motion.div>
      </Container>
    </Box>
  );
};

