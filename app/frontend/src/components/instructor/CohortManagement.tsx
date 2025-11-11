/** Cohort Management Component */
import React, { useState } from 'react';
import {
  Box,
  Button,
  Card,
  CardContent,
  Typography,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  IconButton,
  Chip,
  Alert,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Autocomplete,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
} from '@mui/material';
import {
  Add,
  Cancel,
  Delete,
  Edit,
  People,
} from '@mui/icons-material';
import { cohortService, type Cohort, type CohortCreate, type CohortUpdate, type CohortMember } from '../../services/cohortService';
import { authService } from '../../services/authService';
import { type User } from '../../types/auth';
import { useThemeMode } from '../../contexts/ThemeContext';

interface CohortManagementProps {
  cohorts: Cohort[];
  onRefresh: () => void;
}

export const CohortManagement: React.FC<CohortManagementProps> = ({ cohorts, onRefresh }) => {
  const { mode } = useThemeMode();
  const [openDialog, setOpenDialog] = useState(false);
  const [openMemberDialog, setOpenMemberDialog] = useState(false);
  const [selectedCohort, setSelectedCohort] = useState<Cohort | null>(null);
  const [formData, setFormData] = useState<CohortCreate>({
    name: '',
    description: '',
    start_date: '',
    end_date: '',
    is_active: true,
  });
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [users, setUsers] = useState<User[]>([]);
  const [availableUsers, setAvailableUsers] = useState<User[]>([]);
  const [selectedUser, setSelectedUser] = useState<User | null>(null);
  const [selectedRole, setSelectedRole] = useState<'student' | 'instructor'>('student');
  const [loadingUsers, setLoadingUsers] = useState(false);

  const handleOpenDialog = (cohort?: Cohort) => {
    if (cohort) {
      setSelectedCohort(cohort);
      setFormData({
        name: cohort.name,
        description: cohort.description || '',
        start_date: cohort.start_date || '',
        end_date: cohort.end_date || '',
        is_active: cohort.is_active,
      });
    } else {
      setSelectedCohort(null);
      setFormData({
        name: '',
        description: '',
        start_date: '',
        end_date: '',
        is_active: true,
      });
    }
    setError(null);
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setSelectedCohort(null);
    setFormData({
      name: '',
      description: '',
      start_date: '',
      end_date: '',
      is_active: true,
    });
    setError(null);
  };

  const handleOpenMemberDialog = async (cohort: Cohort) => {
    setSelectedCohort(cohort);
    setError(null);
    setLoadingUsers(true);
    setOpenMemberDialog(true);
    
    try {
      // Fetch all users (students and instructors)
      const allUsers = await authService.getUsers();
      setUsers(allUsers);
      
      // Get current members
      const currentMemberIds = cohort.members.map(m => m.user_id);
      
      // Filter out users who are already members
      const available = allUsers.filter(u => !currentMemberIds.includes(u.id));
      setAvailableUsers(available);
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || 'Failed to load users';
      setError(errorMessage);
    } finally {
      setLoadingUsers(false);
    }
  };

  const handleCloseMemberDialog = () => {
    setOpenMemberDialog(false);
    setSelectedCohort(null);
    setSelectedUser(null);
    setSelectedRole('student');
    setUsers([]);
    setAvailableUsers([]);
    setError(null);
  };

  const handleAddMember = async () => {
    if (!selectedCohort || !selectedUser) return;
    
    try {
      setLoading(true);
      setError(null);
      
      await cohortService.addMember(selectedCohort.id, {
        user_id: selectedUser.id,
        role: selectedRole,
      });
      
      // Refresh cohort data
      const updatedCohort = await cohortService.getCohort(selectedCohort.id);
      setSelectedCohort(updatedCohort);
      
      // Update available users
      const currentMemberIds = updatedCohort.members.map(m => m.user_id);
      const available = users.filter(u => !currentMemberIds.includes(u.id));
      setAvailableUsers(available);
      
      // Reset selection
      setSelectedUser(null);
      setSelectedRole('student');
      
      // Refresh parent list
      onRefresh();
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || 'Failed to add member';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleRemoveMember = async (userId: number) => {
    if (!selectedCohort) return;
    
    if (!window.confirm('Are you sure you want to remove this member from the cohort?')) {
      return;
    }
    
    try {
      setLoading(true);
      setError(null);
      
      await cohortService.removeMember(selectedCohort.id, userId);
      
      // Refresh cohort data
      const updatedCohort = await cohortService.getCohort(selectedCohort.id);
      setSelectedCohort(updatedCohort);
      
      // Update available users
      const currentMemberIds = updatedCohort.members.map(m => m.user_id);
      const available = users.filter(u => !currentMemberIds.includes(u.id));
      setAvailableUsers(available);
      
      // Refresh parent list
      onRefresh();
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || 'Failed to remove member';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async () => {
    try {
      setLoading(true);
      setError(null);

      // Frontend date validation
      const today = new Date();
      today.setHours(0, 0, 0, 0);
      
      if (formData.start_date) {
        const startDate = new Date(formData.start_date);
        startDate.setHours(0, 0, 0, 0);
        if (startDate < today) {
          setError('Start date cannot be before today');
          setLoading(false);
          return;
        }
      }
      
      if (formData.end_date) {
        const endDate = new Date(formData.end_date);
        endDate.setHours(0, 0, 0, 0);
        if (endDate < today) {
          setError('End date cannot be before today');
          setLoading(false);
          return;
        }
        
        if (formData.start_date) {
          const startDate = new Date(formData.start_date);
          startDate.setHours(0, 0, 0, 0);
          if (endDate < startDate) {
            setError('End date cannot be before start date');
            setLoading(false);
            return;
          }
        }
      }

      if (selectedCohort) {
        // Update existing cohort
        const cleanedData: CohortUpdate = {
          name: formData.name,
          description: formData.description || undefined,
          start_date: formData.start_date || undefined,
          end_date: formData.end_date || undefined,
          is_active: formData.is_active,
        };
        
        await cohortService.updateCohort(selectedCohort.id, cleanedData);
        onRefresh();
        handleCloseDialog();
      } else {
        // Create new cohort - clean up empty strings to null/undefined
        const cleanedData: CohortCreate = {
          name: formData.name,
          description: formData.description || undefined,
          start_date: formData.start_date || undefined,
          end_date: formData.end_date || undefined,
          is_active: formData.is_active,
        };
        
        await cohortService.createCohort(cleanedData);
        onRefresh();
        handleCloseDialog();
      }
    } catch (err: any) {
      // Handle Pydantic validation errors
      let errorMessage = 'Failed to save cohort';
      
      if (err.response?.data) {
        const errorData = err.response.data;
        
        // Check if it's a Pydantic validation error (array of errors)
        if (Array.isArray(errorData.detail)) {
          const validationErrors = errorData.detail.map((e: any) => {
            const field = Array.isArray(e.loc) ? e.loc.slice(1).join('.') : 'field';
            return `${field}: ${e.msg}`;
          });
          errorMessage = validationErrors.join(', ');
        } else if (typeof errorData.detail === 'string') {
          errorMessage = errorData.detail;
        } else if (errorData.detail) {
          errorMessage = JSON.stringify(errorData.detail);
        }
      }
      
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3, px: 2 }}>
        <Typography variant="h6" sx={{ fontWeight: 'bold', color: 'text.primary' }}>
          Manage Cohorts
        </Typography>
        <Button
          variant="contained"
          startIcon={<Add />}
          onClick={() => handleOpenDialog()}
          sx={{
            backgroundColor: '#1976d2',
            color: 'text.primary',
            mr: 2,
          }}
        >
          Create Cohort
        </Button>
      </Box>

      {cohorts.length === 0 ? (
        <Card className="glass-surface" sx={{ borderRadius: 2, p: 4, textAlign: 'center' }}>
          <Typography variant="body1" sx={{ color: 'text.secondary', mb: 2 }}>
            No cohorts yet. Create your first cohort to get started.
          </Typography>
        </Card>
      ) : (
        <TableContainer component={Card} className="glass-surface" sx={{ borderRadius: 2 }}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell sx={{ fontWeight: 'bold', color: 'text.primary' }}>Name</TableCell>
                <TableCell sx={{ fontWeight: 'bold', color: 'text.primary' }}>Description</TableCell>
                <TableCell sx={{ fontWeight: 'bold', color: 'text.primary' }}>Members</TableCell>
                <TableCell sx={{ fontWeight: 'bold', color: 'text.primary' }}>Status</TableCell>
                <TableCell sx={{ fontWeight: 'bold', color: 'text.primary' }}>Dates</TableCell>
                <TableCell sx={{ fontWeight: 'bold', color: 'text.primary' }}>Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {cohorts.map((cohort) => {
                const isCancelled = !!cohort.cancelled_at;
                return (
                <TableRow 
                  key={cohort.id}
                  sx={{
                    opacity: isCancelled ? 0.7 : 1,
                    backgroundColor: isCancelled ? 'action.hover' : 'transparent',
                  }}
                >
                  <TableCell sx={{ color: isCancelled ? 'text.disabled' : 'text.primary' }}>
                    {cohort.name}
                    {isCancelled && (
                      <Typography variant="caption" sx={{ color: 'error.main', ml: 1, fontStyle: 'italic' }}>
                        (Cancelled)
                      </Typography>
                    )}
                  </TableCell>
                  <TableCell sx={{ color: 'text.secondary', maxWidth: 300 }}>
                    {cohort.description || 'No description'}
                  </TableCell>
                  <TableCell>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <IconButton
                        size="small"
                        onClick={() => handleOpenMemberDialog(cohort)}
                        sx={{ color: 'primary.main' }}
                        title="Manage members"
                      >
                        <People fontSize="small" />
                      </IconButton>
                      <Typography variant="body2" sx={{ color: 'text.secondary' }}>
                        {cohort.student_count} students, {cohort.instructor_count} instructors
                      </Typography>
                    </Box>
                  </TableCell>
                  <TableCell>
                    <Box sx={{ display: 'flex', gap: 1, alignItems: 'center' }}>
                      {cohort.cancelled_at ? (
                        <Chip
                          label="Cancelled"
                          color="error"
                          size="small"
                          sx={{ fontWeight: 'bold' }}
                        />
                      ) : (
                        <Chip
                          label={cohort.is_active ? 'Active' : 'Inactive'}
                          color={cohort.is_active ? 'success' : 'default'}
                          size="small"
                        />
                      )}
                      {cohort.cancelled_at && (
                        <Typography variant="caption" sx={{ color: 'text.secondary', ml: 1 }}>
                          {new Date(cohort.cancelled_at).toLocaleDateString()}
                        </Typography>
                      )}
                    </Box>
                  </TableCell>
                  <TableCell sx={{ color: 'text.secondary' }}>
                    {cohort.start_date && cohort.end_date
                      ? `${cohort.start_date} - ${cohort.end_date}`
                      : 'No dates set'}
                  </TableCell>
                  <TableCell>
                    <Box sx={{ display: 'flex', gap: 1 }}>
                      <IconButton
                        size="small"
                        onClick={() => handleOpenDialog(cohort)}
                        sx={{ color: 'text.secondary' }}
                        title="Edit cohort"
                      >
                        <Edit fontSize="small" />
                      </IconButton>
                      {(() => {
                        const today = new Date();
                        today.setHours(0, 0, 0, 0);
                        const startDate = cohort.start_date ? new Date(cohort.start_date) : null;
                        const isFuture = startDate && startDate > today;
                        const cancelledAt = cohort.cancelled_at ? new Date(cohort.cancelled_at) : null;
                        const isCancelled = cancelledAt !== null;
                        
                        // Cancel button: show if cohort is not cancelled (regardless of is_active status)
                        // This allows canceling even if cohort is marked inactive
                        const canCancel = !isCancelled;
                        
                        // Delete button logic:
                        // - If no students: can delete immediately (no need to cancel first)
                        // - If students assigned: must be cancelled first, then wait 14 days
                        const hasStudents = cohort.student_count > 0;
                        const daysSinceCancellation = cancelledAt 
                          ? Math.floor((today.getTime() - cancelledAt.getTime()) / (1000 * 60 * 60 * 24))
                          : -1;
                        
                        let canDelete = false;
                        if (!hasStudents) {
                          // No students: can delete immediately
                          canDelete = true;
                        } else {
                          // Has students: must be cancelled and wait 14 days
                          canDelete = isCancelled && daysSinceCancellation >= 14;
                        }
                        
                        return (
                          <Box sx={{ display: 'flex', gap: 0.5 }}>
                            {canCancel && (
                              <IconButton
                                size="small"
                                onClick={async () => {
                                  if (window.confirm(`Are you sure you want to cancel "${cohort.name}"?`)) {
                                    try {
                                      setError(null);
                                      await cohortService.cancelCohort(cohort.id);
                                      onRefresh();
                                    } catch (err: any) {
                                      const errorMessage = err.response?.data?.detail || 'Failed to cancel cohort';
                                      setError(errorMessage);
                                      // Show error in dialog if open
                                      if (openDialog) {
                                        setTimeout(() => setError(null), 5000);
                                      }
                                    }
                                  }
                                }}
                                sx={{ color: 'warning.main' }}
                                title="Cancel cohort"
                              >
                                <Cancel fontSize="small" />
                              </IconButton>
                            )}
                            {canDelete && (
                              <IconButton
                                size="small"
                                onClick={async () => {
                                  if (window.confirm(`Are you sure you want to permanently delete "${cohort.name}"? This action cannot be undone.`)) {
                                    try {
                                      setError(null);
                                      await cohortService.deleteCohort(cohort.id);
                                      onRefresh();
                                    } catch (err: any) {
                                      const errorMessage = err.response?.data?.detail || 'Failed to delete cohort';
                                      setError(errorMessage);
                                      // Show error in dialog if open
                                      if (openDialog) {
                                        setTimeout(() => setError(null), 5000);
                                      }
                                    }
                                  }
                                }}
                                sx={{ color: 'error.main' }}
                                title="Delete cohort permanently"
                              >
                                <Delete fontSize="small" />
                              </IconButton>
                            )}
                            {hasStudents && isCancelled && daysSinceCancellation < 14 && (
                              <IconButton
                                size="small"
                                disabled
                                sx={{ color: 'text.disabled' }}
                                title={`Cannot delete yet. ${14 - daysSinceCancellation} day(s) remaining before deletion is allowed (cohort has students).`}
                              >
                                <Delete fontSize="small" />
                              </IconButton>
                            )}
                          </Box>
                        );
                      })()}
                    </Box>
                  </TableCell>
                </TableRow>
              );
              })}
            </TableBody>
          </Table>
        </TableContainer>
      )}

      {/* Create/Edit Dialog */}
      <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
        <DialogTitle>
          {selectedCohort ? 'Edit Cohort' : 'Create New Cohort'}
        </DialogTitle>
        <DialogContent>
          {error && (
            <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>
              <Typography variant="body2">{error}</Typography>
            </Alert>
          )}
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, pt: 1 }}>
            <TextField
              label="Cohort Name"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              required
              fullWidth
            />
            <TextField
              label="Description"
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              multiline
              rows={3}
              fullWidth
            />
            <TextField
              label="Start Date"
              type="date"
              value={formData.start_date}
              onChange={(e) => {
                const newStartDate = e.target.value;
                setFormData({ ...formData, start_date: newStartDate });
                
                // If end_date is before new start_date, clear it
                if (formData.end_date && newStartDate && formData.end_date < newStartDate) {
                  setFormData(prev => ({ ...prev, start_date: newStartDate, end_date: '' }));
                }
              }}
              InputLabelProps={{ shrink: true }}
              inputProps={{ min: new Date().toISOString().split('T')[0] }}
              fullWidth
            />
            <TextField
              label="End Date"
              type="date"
              value={formData.end_date}
              onChange={(e) => setFormData({ ...formData, end_date: e.target.value })}
              InputLabelProps={{ shrink: true }}
              inputProps={{ 
                min: formData.start_date || new Date().toISOString().split('T')[0]
              }}
              fullWidth
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog} sx={{ color: 'text.secondary' }}>
            Cancel
          </Button>
          <Button
            onClick={handleSubmit}
            variant="contained"
            disabled={loading || !formData.name}
            sx={{ backgroundColor: '#1976d2', color: 'text.primary' }}
          >
            {selectedCohort ? 'Update' : 'Create'}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Member Management Dialog */}
      <Dialog open={openMemberDialog} onClose={handleCloseMemberDialog} maxWidth="md" fullWidth>
        <DialogTitle>
          Manage Members - {selectedCohort?.name}
        </DialogTitle>
        <DialogContent>
          {error && (
            <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>
              <Typography variant="body2">{error}</Typography>
            </Alert>
          )}
          
          {/* Add Member Section */}
          <Box sx={{ mb: 4 }}>
            <Typography variant="h6" sx={{ mb: 2 }}>Add Member</Typography>
            <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
              <FormControl fullWidth>
                <InputLabel>Role</InputLabel>
                <Select
                  value={selectedRole}
                  onChange={(e) => setSelectedRole(e.target.value as 'student' | 'instructor')}
                  label="Role"
                >
                  <MenuItem value="student">Student</MenuItem>
                  <MenuItem value="instructor">Instructor</MenuItem>
                </Select>
              </FormControl>
              <Autocomplete
                options={availableUsers}
                getOptionLabel={(option) => `${option.full_name || option.username || option.email} (${option.email})`}
                value={selectedUser}
                onChange={(_, newValue) => setSelectedUser(newValue)}
                loading={loadingUsers}
                fullWidth
                renderInput={(params) => (
                  <TextField
                    {...params}
                    label="Select User"
                    placeholder="Search users..."
                  />
                )}
              />
            </Box>
            <Button
              variant="contained"
              onClick={handleAddMember}
              disabled={!selectedUser || loading}
              fullWidth
            >
              Add Member
            </Button>
          </Box>

          {/* Current Members Section */}
          <Box>
            <Typography variant="h6" sx={{ mb: 2 }}>Current Members</Typography>
            {selectedCohort && selectedCohort.members.length === 0 ? (
              <Typography variant="body2" sx={{ color: 'text.secondary', textAlign: 'center', py: 4 }}>
                No members assigned yet
              </Typography>
            ) : (
              <List>
                {selectedCohort?.members.map((member: CohortMember) => {
                  const user = member.user;
                  return (
                    <ListItem key={member.id}>
                      <ListItemText
                        primary={user?.full_name || user?.username || user?.email || 'Unknown User'}
                        secondary={
                          <Box>
                            <Typography variant="body2" sx={{ color: 'text.secondary' }}>
                              {user?.email}
                            </Typography>
                            <Chip
                              label={member.role}
                              size="small"
                              color={member.role === 'instructor' ? 'primary' : 'default'}
                              sx={{ mt: 0.5 }}
                            />
                          </Box>
                        }
                      />
                      <ListItemSecondaryAction>
                        <IconButton
                          edge="end"
                          onClick={() => handleRemoveMember(member.user_id)}
                          disabled={loading}
                          sx={{ color: 'error.main' }}
                          title="Remove member"
                        >
                          <Delete fontSize="small" />
                        </IconButton>
                      </ListItemSecondaryAction>
                    </ListItem>
                  );
                })}
              </List>
            )}
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseMemberDialog}>Close</Button>
        </DialogActions>
      </Dialog>
      </Box>
    );
  };

