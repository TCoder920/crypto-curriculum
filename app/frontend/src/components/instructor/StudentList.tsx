/** Student List Component with Progress Tracking */
import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  LinearProgress,
  Alert,
} from '@mui/material';
import { cohortService, type Cohort } from '../../services/cohortService';
import { useThemeMode } from '../../contexts/ThemeContext';

interface StudentListProps {
  cohorts: Cohort[];
}

interface StudentWithProgress {
  id: number;
  email: string;
  full_name?: string;
  username?: string;
  cohort_id: number;
  cohort_name: string;
  last_activity?: string;
  modules_completed: number;
  total_modules: number;
  avg_score?: number;
  is_at_risk: boolean;
}

export const StudentList: React.FC<StudentListProps> = ({ cohorts }) => {
  const { mode } = useThemeMode();
  const [selectedCohortId, setSelectedCohortId] = useState<number | 'all'>('all');
  const [students, setStudents] = useState<StudentWithProgress[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadStudents();
  }, [cohorts, selectedCohortId]);

  const loadStudents = async () => {
    try {
      setLoading(true);
      setError(null);

      // Get all students from cohorts
      const allStudents: StudentWithProgress[] = [];

      for (const cohort of cohorts) {
        if (selectedCohortId !== 'all' && cohort.id !== selectedCohortId) {
          continue;
        }

        for (const member of cohort.members) {
          if (member.role === 'student' && member.user) {
            // Calculate days since last activity (simplified - would need actual progress data)
            // In a real implementation, this would query UserProgress.last_accessed_at
            const daysSinceActivity = 0; // Placeholder - would calculate from UserProgress
            const isAtRisk = daysSinceActivity > 7; // At risk if inactive > 7 days

            allStudents.push({
              id: member.user.id,
              email: member.user.email,
              full_name: member.user.full_name || undefined,
              username: member.user.username || undefined,
              cohort_id: cohort.id,
              cohort_name: cohort.name,
              last_activity: undefined, // Would get from UserProgress
              modules_completed: 0, // Would calculate from UserProgress
              total_modules: 17, // Total modules in curriculum
              avg_score: undefined, // Would calculate from QuizAttempts
              is_at_risk: isAtRisk,
            });
          }
        }
      }

      setStudents(allStudents);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load students');
    } finally {
      setLoading(false);
    }
  };

  const filteredStudents = selectedCohortId === 'all'
    ? students
    : students.filter((s) => s.cohort_id === selectedCohortId);

  const atRiskStudents = filteredStudents.filter((s) => s.is_at_risk);

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3, px: 2 }}>
        <Typography variant="h6" sx={{ fontWeight: 'bold', color: 'text.primary' }}>
          Student Progress
        </Typography>
        <FormControl size="small" sx={{ minWidth: 200, mr: 2 }}>
          <InputLabel sx={{ color: 'text.secondary' }}>Filter by Cohort</InputLabel>
          <Select
            value={selectedCohortId}
            onChange={(e) => setSelectedCohortId(e.target.value as number | 'all')}
            label="Filter by Cohort"
            sx={{ color: 'text.primary' }}
          >
            <MenuItem value="all">All Cohorts</MenuItem>
            {cohorts.map((cohort) => (
              <MenuItem key={cohort.id} value={cohort.id}>
                {cohort.name}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      </Box>

      {atRiskStudents.length > 0 && (
        <Alert severity="warning" sx={{ mb: 3 }}>
          {atRiskStudents.length} student{atRiskStudents.length > 1 ? 's' : ''} at risk (inactive &gt; 7 days)
        </Alert>
      )}

      {error && (
        <Alert severity="error" sx={{ mb: 3 }} onClose={() => setError(null)}>
          <Typography variant="body2">{error}</Typography>
        </Alert>
      )}

      {loading ? (
        <LinearProgress />
      ) : filteredStudents.length === 0 ? (
        <Card className="glass-surface" sx={{ borderRadius: 2, p: 4, textAlign: 'center' }}>
          <Typography variant="body1" sx={{ color: 'text.secondary' }}>
            No students found.
          </Typography>
        </Card>
      ) : (
        <TableContainer component={Card} className="glass-surface" sx={{ borderRadius: 2 }}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell sx={{ fontWeight: 'bold', color: 'text.primary' }}>Student</TableCell>
                <TableCell sx={{ fontWeight: 'bold', color: 'text.primary' }}>Cohort</TableCell>
                <TableCell sx={{ fontWeight: 'bold', color: 'text.primary' }}>Progress</TableCell>
                <TableCell sx={{ fontWeight: 'bold', color: 'text.primary' }}>Modules Completed</TableCell>
                <TableCell sx={{ fontWeight: 'bold', color: 'text.primary' }}>Avg Score</TableCell>
                <TableCell sx={{ fontWeight: 'bold', color: 'text.primary' }}>Status</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {filteredStudents.map((student) => {
                const progressPercent = student.total_modules > 0
                  ? (student.modules_completed / student.total_modules) * 100
                  : 0;

                return (
                  <TableRow key={student.id}>
                    <TableCell sx={{ color: 'text.primary' }}>
                      <Box>
                        <Typography variant="body2" sx={{ fontWeight: 'bold' }}>
                          {student.full_name || student.username || student.email}
                        </Typography>
                        <Typography variant="caption" sx={{ color: 'text.secondary' }}>
                          {student.email}
                        </Typography>
                      </Box>
                    </TableCell>
                    <TableCell sx={{ color: 'text.secondary' }}>{student.cohort_name}</TableCell>
                    <TableCell>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, minWidth: 150 }}>
                        <LinearProgress
                          variant="determinate"
                          value={progressPercent}
                          sx={{ flexGrow: 1, height: 8, borderRadius: 1 }}
                        />
                        <Typography variant="body2" sx={{ color: 'text.secondary', minWidth: 40 }}>
                          {Math.round(progressPercent)}%
                        </Typography>
                      </Box>
                    </TableCell>
                    <TableCell sx={{ color: 'text.secondary' }}>
                      {student.modules_completed} / {student.total_modules}
                    </TableCell>
                    <TableCell sx={{ color: 'text.secondary' }}>
                      {student.avg_score !== undefined
                        ? `${Math.round(student.avg_score)}%`
                        : 'N/A'}
                    </TableCell>
                    <TableCell>
                      {student.is_at_risk ? (
                        <Chip label="At Risk" color="warning" size="small" />
                      ) : (
                        <Chip label="Active" color="success" size="small" />
                      )}
                    </TableCell>
                  </TableRow>
                );
              })}
            </TableBody>
          </Table>
        </TableContainer>
      )}
    </Box>
  );
};

