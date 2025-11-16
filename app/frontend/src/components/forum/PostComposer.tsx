/** Post composer component - create/edit forum posts */
import React, { useState } from 'react';
import {
  Paper,
  Box,
  TextField,
  Button,
  Typography,
  Alert,
} from '@mui/material';
import { Send, Cancel } from '@mui/icons-material';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { forumService, type ForumPostCreate } from '../../services/forumService';
import { useAuth } from '../../contexts/AuthContext';

interface PostComposerProps {
  moduleId?: number;
  parentPostId?: number;
  onPostCreated?: () => void;
  onCancel?: () => void;
  initialTitle?: string;
  initialContent?: string;
}

export const PostComposer: React.FC<PostComposerProps> = ({
  moduleId,
  parentPostId,
  onPostCreated,
  onCancel,
  initialTitle = '',
  initialContent = '',
}) => {
  const { user } = useAuth();
  const queryClient = useQueryClient();
  const [title, setTitle] = useState(initialTitle);
  const [content, setContent] = useState(initialContent);
  const [error, setError] = useState<string | null>(null);

  const createMutation = useMutation({
    mutationFn: (postData: ForumPostCreate) => forumService.createPost(postData),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['forum-posts'] });
      setTitle('');
      setContent('');
      setError(null);
      onPostCreated?.();
    },
    onError: (err: any) => {
      setError(err.response?.data?.detail || 'Failed to create post');
    },
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!content.trim()) {
      setError('Content is required');
      return;
    }

    if (!parentPostId && !title.trim()) {
      setError('Title is required for new posts');
      return;
    }

    const postData: ForumPostCreate = {
      module_id: moduleId || null,
      title: parentPostId ? null : title.trim(),
      content: content.trim(),
      parent_post_id: parentPostId || null,
    };

    createMutation.mutate(postData);
  };

  if (!user) {
    return (
      <Alert severity="warning">
        You must be logged in to create a post.
      </Alert>
    );
  }

  return (
    <Paper sx={{ p: 3, mb: 3 }}>
      <Typography variant="h6" sx={{ mb: 2 }}>
        {parentPostId ? 'Reply to Post' : 'Create New Post'}
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      <form onSubmit={handleSubmit}>
        {!parentPostId && (
          <TextField
            fullWidth
            label="Title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
            sx={{ mb: 2 }}
          />
        )}

        <TextField
          fullWidth
          label="Content"
          value={content}
          onChange={(e) => setContent(e.target.value)}
          required
          multiline
          rows={6}
          sx={{ mb: 2 }}
        />

        <Box sx={{ display: 'flex', gap: 2, justifyContent: 'flex-end' }}>
          {onCancel && (
            <Button
              variant="outlined"
              startIcon={<Cancel />}
              onClick={onCancel}
            >
              Cancel
            </Button>
          )}
          <Button
            type="submit"
            variant="contained"
            startIcon={<Send />}
            disabled={createMutation.isPending}
          >
            {createMutation.isPending ? 'Posting...' : parentPostId ? 'Reply' : 'Post'}
          </Button>
        </Box>
      </form>
    </Paper>
  );
};

