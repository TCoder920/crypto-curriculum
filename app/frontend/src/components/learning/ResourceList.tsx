/** Learning resource list component */
import React, { useState } from 'react';
import {
  Box,
  Container,
  Typography,
  Card,
  CardContent,
  Grid,
  Button,
  Chip,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Alert,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from '@mui/material';
import { Add, ThumbUp, OpenInNew, Delete } from '@mui/icons-material';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useAuth } from '../../contexts/AuthContext';
import {
  learningResourceService,
  type LearningResource,
  type LearningResourceCreate,
} from '../../services/learningResourceService';
import { useThemeMode } from '../../contexts/ThemeContext';
import { moduleService } from '../../services/moduleService';
import type { Module } from '../../types/module';

export const ResourceList: React.FC<{ moduleId?: number }> = ({ moduleId }) => {
  const { user } = useAuth();
  const { mode } = useThemeMode();
  const queryClient = useQueryClient();
  const [openDialog, setOpenDialog] = useState(false);
  const [filterType, setFilterType] = useState<string>('all');
  const [filterDifficulty, setFilterDifficulty] = useState<string>('all');
  const [newResource, setNewResource] = useState<LearningResourceCreate>({
    title: '',
    url: '',
    resource_type: null,
    difficulty: null,
    module_id: moduleId || null,
  });

  const resourcesQuery = useQuery({
    queryKey: ['learning-resources', moduleId, filterType, filterDifficulty],
    queryFn: () =>
      learningResourceService.getResources({
        module_id: moduleId || undefined,
        resource_type: filterType !== 'all' ? filterType : undefined,
        difficulty: filterDifficulty !== 'all' ? filterDifficulty : undefined,
      }),
  });

  const modulesQuery = useQuery({
    queryKey: ['modules'],
    queryFn: () => moduleService.getModules(),
    enabled: !moduleId, // Only fetch if we need to show module selector
  });

  const createMutation = useMutation({
    mutationFn: (resource: LearningResourceCreate) =>
      learningResourceService.createResource(resource),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['learning-resources'] });
      setOpenDialog(false);
      setNewResource({
        title: '',
        url: '',
        resource_type: null,
        difficulty: null,
        module_id: moduleId || null,
      });
    },
  });

  const upvoteMutation = useMutation({
    mutationFn: (resourceId: number) => learningResourceService.upvoteResource(resourceId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['learning-resources'] });
    },
  });

  const deleteMutation = useMutation({
    mutationFn: (resourceId: number) => learningResourceService.deleteResource(resourceId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['learning-resources'] });
    },
  });

  const resources: LearningResource[] = resourcesQuery.data || [];
  const modules: Module[] = modulesQuery.data?.modules || [];

  const handleCreate = () => {
    if (newResource.title && newResource.url) {
      createMutation.mutate(newResource);
    }
  };

  const handleUpvote = (resourceId: number) => {
    upvoteMutation.mutate(resourceId);
  };

  const handleDelete = (resourceId: number) => {
    if (window.confirm('Are you sure you want to delete this resource?')) {
      deleteMutation.mutate(resourceId);
    }
  };

  const isInstructor = user?.role === 'instructor' || user?.role === 'admin';

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
        <Typography variant="h4">
          {moduleId ? 'Module Resources' : 'Learning Resources'}
        </Typography>
        {isInstructor && (
          <Button
            variant="contained"
            startIcon={<Add />}
            onClick={() => setOpenDialog(true)}
          >
            Add Resource
          </Button>
        )}
      </Box>

      {/* Filters */}
      <Box sx={{ display: 'flex', gap: 2, mb: 3 }}>
        <FormControl size="small" sx={{ minWidth: 150 }}>
          <InputLabel>Type</InputLabel>
          <Select
            value={filterType}
            label="Type"
            onChange={(e) => setFilterType(e.target.value)}
          >
            <MenuItem value="all">All Types</MenuItem>
            <MenuItem value="video">Video</MenuItem>
            <MenuItem value="article">Article</MenuItem>
            <MenuItem value="tutorial">Tutorial</MenuItem>
            <MenuItem value="documentation">Documentation</MenuItem>
          </Select>
        </FormControl>
        <FormControl size="small" sx={{ minWidth: 150 }}>
          <InputLabel>Difficulty</InputLabel>
          <Select
            value={filterDifficulty}
            label="Difficulty"
            onChange={(e) => setFilterDifficulty(e.target.value)}
          >
            <MenuItem value="all">All Levels</MenuItem>
            <MenuItem value="beginner">Beginner</MenuItem>
            <MenuItem value="intermediate">Intermediate</MenuItem>
            <MenuItem value="advanced">Advanced</MenuItem>
          </Select>
        </FormControl>
      </Box>

      {/* Resources Grid */}
      {resourcesQuery.isLoading ? (
        <Typography>Loading resources...</Typography>
      ) : resourcesQuery.isError ? (
        <Alert severity="error">Failed to load resources</Alert>
      ) : resources.length === 0 ? (
        <Alert severity="info">No resources found</Alert>
      ) : (
        <Grid container spacing={3}>
          {resources.map((resource) => (
            <Grid item xs={12} md={6} key={resource.id}>
              <Card sx={{ bgcolor: mode === 'light' ? 'background.paper' : 'grey.900', height: '100%' }}>
                <CardContent>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', mb: 2 }}>
                    <Box sx={{ flex: 1 }}>
                      <Typography variant="h6" gutterBottom>
                        {resource.title}
                      </Typography>
                      {resource.module_title && (
                        <Chip label={resource.module_title} size="small" sx={{ mb: 1 }} />
                      )}
                    </Box>
                    {isInstructor && (
                      <IconButton
                        size="small"
                        color="error"
                        onClick={() => handleDelete(resource.id)}
                      >
                        <Delete />
                      </IconButton>
                    )}
                  </Box>

                  <Box sx={{ display: 'flex', gap: 1, mb: 2, flexWrap: 'wrap' }}>
                    {resource.resource_type && (
                      <Chip label={resource.resource_type} size="small" />
                    )}
                    {resource.difficulty && (
                      <Chip
                        label={resource.difficulty}
                        size="small"
                        color={
                          resource.difficulty === 'beginner'
                            ? 'success'
                            : resource.difficulty === 'intermediate'
                            ? 'warning'
                            : 'error'
                        }
                      />
                    )}
                  </Box>

                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <Button
                      variant="outlined"
                      size="small"
                      startIcon={<OpenInNew />}
                      href={resource.url}
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      Open
                    </Button>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <IconButton
                        size="small"
                        onClick={() => handleUpvote(resource.id)}
                        disabled={upvoteMutation.isPending}
                      >
                        <ThumbUp />
                      </IconButton>
                      <Typography variant="body2">{resource.upvotes}</Typography>
                    </Box>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}

      {/* Create Resource Dialog */}
      <Dialog open={openDialog} onClose={() => setOpenDialog(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Add Learning Resource</DialogTitle>
        <DialogContent>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, pt: 2 }}>
            <TextField
              label="Title"
              fullWidth
              value={newResource.title}
              onChange={(e) => setNewResource({ ...newResource, title: e.target.value })}
            />
            <TextField
              label="URL"
              fullWidth
              value={newResource.url}
              onChange={(e) => setNewResource({ ...newResource, url: e.target.value })}
            />
            <FormControl fullWidth>
              <InputLabel>Type</InputLabel>
              <Select
                value={newResource.resource_type || ''}
                label="Type"
                onChange={(e) =>
                  setNewResource({ ...newResource, resource_type: e.target.value || null })
                }
              >
                <MenuItem value="">None</MenuItem>
                <MenuItem value="video">Video</MenuItem>
                <MenuItem value="article">Article</MenuItem>
                <MenuItem value="tutorial">Tutorial</MenuItem>
                <MenuItem value="documentation">Documentation</MenuItem>
              </Select>
            </FormControl>
            <FormControl fullWidth>
              <InputLabel>Difficulty</InputLabel>
              <Select
                value={newResource.difficulty || ''}
                label="Difficulty"
                onChange={(e) =>
                  setNewResource({ ...newResource, difficulty: e.target.value || null })
                }
              >
                <MenuItem value="">None</MenuItem>
                <MenuItem value="beginner">Beginner</MenuItem>
                <MenuItem value="intermediate">Intermediate</MenuItem>
                <MenuItem value="advanced">Advanced</MenuItem>
              </Select>
            </FormControl>
            {!moduleId && (
              <FormControl fullWidth>
                <InputLabel>Module (Optional)</InputLabel>
                <Select
                  value={newResource.module_id || ''}
                  label="Module (Optional)"
                  onChange={(e) =>
                    setNewResource({ ...newResource, module_id: e.target.value || null })
                  }
                >
                  <MenuItem value="">None</MenuItem>
                  {modules.map((module) => (
                    <MenuItem key={module.id} value={module.id}>
                      {module.title}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            )}
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDialog(false)}>Cancel</Button>
          <Button
            variant="contained"
            onClick={handleCreate}
            disabled={!newResource.title || !newResource.url || createMutation.isPending}
          >
            Add Resource
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

