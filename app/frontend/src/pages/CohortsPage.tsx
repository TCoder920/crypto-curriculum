/** Cohorts Page - Browse and join cohorts (student self-enrollment) */
import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useThemeMode } from '../contexts/ThemeContext';
import { cohortService, type Cohort } from '../services/cohortService';
import {
  Box,
  Container,
  Typography,
  Card,
  CardContent,
  CardActions,
  Button,
  Chip,
  Alert,
  Tabs,
  Tab,
  CircularProgress,
  Grid,
  Divider,
} from '@mui/material';
import { motion } from 'framer-motion';
import {
  Groups,
  PersonAdd,
  PersonRemove,
  CalendarToday,
  Description,
  CheckCircle,
  Cancel,
} from '@mui/icons-material';

const MAX_COHORT_STUDENTS = 25;

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
      id={`cohort-tabpanel-${index}`}
      aria-labelledby={`cohort-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ py: 3 }}>{children}</Box>}
    </div>
  );
}

export const CohortsPage: React.FC = () => {
  const { user } = useAuth();
  const { mode } = useThemeMode();
  const [tabValue, setTabValue] = useState(0);
  const [availableCohorts, setAvailableCohorts] = useState<Cohort[]>([]);
  const [myCohorts, setMyCohorts] = useState<Cohort[]>([]);
  const [loading, setLoading] = useState(true);
  const [joining, setJoining] = useState<number | null>(null);
  const [leaving, setLeaving] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const backgroundColor = mode === 'light' ? '#f8f9fa' : '#0a0e27';

  const isStudent = user?.role === 'student';

  useEffect(() => {
    if (!isStudent) {
      return;
    }
    loadCohorts();
  }, [isStudent]);

  const loadCohorts = async () => {
    try {
      setLoading(true);
      setError(null);

      // Load available cohorts (can join)
      const availableData = await cohortService.getCohorts(false, true);
      setAvailableCohorts(availableData.cohorts);

      // Load my enrolled cohorts
      const myCohortsData = await cohortService.getCohorts();
      setMyCohorts(myCohortsData.cohorts);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load cohorts');
    } finally {
      setLoading(false);
    }
  };

  const handleJoinCohort = async (cohortId: number) => {
    try {
      setJoining(cohortId);
      setError(null);
      setSuccess(null);

      await cohortService.joinCohort(cohortId);
      setSuccess(`Successfully joined cohort!`);
      
      // Reload cohorts
      await loadCohorts();
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || 'Failed to join cohort';
      setError(errorMessage);
    } finally {
      setJoining(null);
    }
  };

  const handleLeaveCohort = async (cohortId: number) => {
    if (!window.confirm('Are you sure you want to leave this cohort? You will lose access to cohort-specific content and progress.')) {
      return;
    }

    try {
      setLeaving(cohortId);
      setError(null);
      setSuccess(null);

      await cohortService.leaveCohort(cohortId);
      setSuccess(`Successfully left cohort!`);
      
      // Reload cohorts
      await loadCohorts();
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || 'Failed to leave cohort';
      setError(errorMessage);
    } finally {
      setLeaving(null);
    }
  };

  const handleTabChange = (_event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  if (!isStudent) {
    return (
      <Box sx={{ minHeight: '100vh', backgroundColor, py: 4 }}>
        <Container maxWidth="lg">
          <Alert severity="info">
            This page is only available for students.
          </Alert>
        </Container>
      </Box>
    );
  }

  const renderCohortCard = (cohort: Cohort, isAvailable: boolean) => {
    // Only students count toward the 25-member limit
    const isFull = cohort.student_count >= MAX_COHORT_STUDENTS;
    const spotsRemaining = MAX_COHORT_STUDENTS - cohort.student_count;
    const isCancelled = !!cohort.cancelled_at;

    return (
      <Card
        key={cohort.id}
        className="glass-surface"
        sx={{
          borderRadius: 3,
          height: '100%',
          display: 'flex',
          flexDirection: 'column',
          opacity: isCancelled ? 0.7 : 1,
          backgroundColor: isCancelled ? 'action.hover' : 'transparent',
        }}
      >
        <CardContent sx={{ flexGrow: 1 }}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', mb: 2 }}>
            <Typography variant="h6" sx={{ fontWeight: 'bold', color: 'text.primary' }}>
              {cohort.name}
              {isCancelled && (
                <Chip
                  label="Cancelled"
                  color="error"
                  size="small"
                  sx={{ ml: 1, fontWeight: 'bold' }}
                />
              )}
            </Typography>
            <Chip
              label={isFull ? 'Full' : `${spotsRemaining} spots left`}
              color={isFull ? 'error' : 'success'}
              size="small"
            />
          </Box>

          {cohort.description && (
            <Box sx={{ display: 'flex', alignItems: 'start', mb: 2 }}>
              <Description sx={{ mr: 1, mt: 0.5, fontSize: 18, color: 'text.secondary' }} />
              <Typography variant="body2" sx={{ color: 'text.secondary', flex: 1 }}>
                {cohort.description}
              </Typography>
            </Box>
          )}

          <Divider sx={{ my: 2 }} />

          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <Groups sx={{ fontSize: 18, color: 'text.secondary' }} />
              <Typography variant="body2" sx={{ color: 'text.secondary' }}>
                {cohort.student_count} / {MAX_COHORT_STUDENTS} students
                {cohort.instructor_count > 0 && ` • ${cohort.instructor_count} instructor${cohort.instructor_count > 1 ? 's' : ''}`}
                {cohort.member_count !== cohort.student_count + cohort.instructor_count && ` • ${cohort.member_count} total members`}
              </Typography>
            </Box>

            {cohort.start_date && (
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <CalendarToday sx={{ fontSize: 18, color: 'text.secondary' }} />
                <Typography variant="body2" sx={{ color: 'text.secondary' }}>
                  {cohort.start_date && new Date(cohort.start_date).toLocaleDateString()}
                  {cohort.end_date && ` - ${new Date(cohort.end_date).toLocaleDateString()}`}
                </Typography>
              </Box>
            )}

            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              {cohort.status === 'active' && (
                <>
                  <CheckCircle sx={{ fontSize: 18, color: 'success.main' }} />
                  <Typography variant="body2" sx={{ color: 'success.main', fontWeight: 'bold' }}>
                    Active
                  </Typography>
                </>
              )}
              {cohort.status === 'upcoming' && (
                <>
                  <CalendarToday sx={{ fontSize: 18, color: 'info.main' }} />
                  <Typography variant="body2" sx={{ color: 'info.main', fontWeight: 'bold' }}>
                    Upcoming
                  </Typography>
                </>
              )}
              {cohort.status === 'inactive' && (
                <>
                  <Cancel sx={{ fontSize: 18, color: 'text.disabled' }} />
                  <Typography variant="body2" sx={{ color: 'text.disabled', fontWeight: 'bold' }}>
                    Inactive
                  </Typography>
                </>
              )}
            </Box>
          </Box>
        </CardContent>

        {isAvailable && !isCancelled && (
          <CardActions sx={{ p: 2, pt: 0 }}>
            <Button
              variant="contained"
              fullWidth
              onClick={() => handleJoinCohort(cohort.id)}
              disabled={joining === cohort.id || isFull || cohort.status === 'inactive' || isCancelled}
              startIcon={<PersonAdd />}
              sx={{ backgroundColor: '#1976d2', color: 'text.primary' }}
            >
              {joining === cohort.id ? (
                <>
                  <CircularProgress size={16} sx={{ mr: 1 }} />
                  Joining...
                </>
              ) : isFull ? (
                'Full'
              ) : cohort.status === 'inactive' ? (
                'Inactive'
              ) : isCancelled ? (
                'Cancelled'
              ) : (
                'Join Cohort'
              )}
            </Button>
          </CardActions>
        )}

        {!isAvailable && !isCancelled && (
          <CardActions sx={{ p: 2, pt: 0 }}>
            <Button
              variant="outlined"
              fullWidth
              onClick={() => handleLeaveCohort(cohort.id)}
              disabled={leaving === cohort.id}
              startIcon={<PersonRemove />}
              sx={{ 
                borderColor: 'error.main', 
                color: 'error.main',
                '&:hover': {
                  borderColor: 'error.dark',
                  backgroundColor: 'error.light',
                  color: 'error.dark',
                }
              }}
            >
              {leaving === cohort.id ? (
                <>
                  <CircularProgress size={16} sx={{ mr: 1 }} />
                  Leaving...
                </>
              ) : (
                'Leave Cohort'
              )}
            </Button>
          </CardActions>
        )}
      </Card>
    );
  };

  return (
    <Box sx={{ minHeight: '100vh', backgroundColor, py: 4 }}>
      <Container maxWidth="lg">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <Typography variant="h4" sx={{ fontWeight: 'bold', mb: 1, color: 'text.primary' }}>
            Cohorts
          </Typography>
          <Typography variant="body1" sx={{ mb: 4, color: 'text.secondary' }}>
            Browse available cohorts and join the ones that interest you. Each cohort can have up to {MAX_COHORT_STUDENTS} students (instructors don't count toward the limit).
          </Typography>

          {error && (
            <Alert severity="error" sx={{ mb: 3 }} onClose={() => setError(null)}>
              {error}
            </Alert>
          )}

          {success && (
            <Alert severity="success" sx={{ mb: 3 }} onClose={() => setSuccess(null)}>
              {success}
            </Alert>
          )}

          <Card className="glass-surface" sx={{ borderRadius: 3 }}>
            <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
              <Tabs value={tabValue} onChange={handleTabChange}>
                <Tab
                  label={`Available Cohorts (${availableCohorts.length})`}
                  icon={<PersonAdd />}
                  iconPosition="start"
                />
                <Tab
                  label={`My Cohorts (${myCohorts.length})`}
                  icon={<Groups />}
                  iconPosition="start"
                />
              </Tabs>
            </Box>

            <TabPanel value={tabValue} index={0}>
              {loading ? (
                <Box sx={{ display: 'flex', justifyContent: 'center', py: 4 }}>
                  <CircularProgress />
                </Box>
              ) : availableCohorts.length === 0 ? (
                <Alert severity="info">
                  No available cohorts to join at this time. Check back later!
                </Alert>
              ) : (
                <Grid container spacing={3}>
                  {availableCohorts.map((cohort) => (
                    <Grid item xs={12} sm={6} md={4} key={cohort.id}>
                      {renderCohortCard(cohort, true)}
                    </Grid>
                  ))}
                </Grid>
              )}
            </TabPanel>

            <TabPanel value={tabValue} index={1}>
              {loading ? (
                <Box sx={{ display: 'flex', justifyContent: 'center', py: 4 }}>
                  <CircularProgress />
                </Box>
              ) : myCohorts.length === 0 ? (
                <Alert severity="info">
                  You haven't joined any cohorts yet. Browse available cohorts to get started!
                </Alert>
              ) : (
                <Grid container spacing={3}>
                  {myCohorts.map((cohort) => (
                    <Grid item xs={12} sm={6} md={4} key={cohort.id}>
                      {renderCohortCard(cohort, false)}
                    </Grid>
                  ))}
                </Grid>
              )}
            </TabPanel>
          </Card>
        </motion.div>
      </Container>
    </Box>
  );
};

