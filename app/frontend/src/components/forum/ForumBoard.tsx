/** Forum board component - displays list of forum posts */
import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Box,
  Paper,
  Typography,
  Button,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Pagination,
  CircularProgress,
  Alert,
  Chip,
  IconButton,
} from '@mui/material';
import {
  Add,
  Search,
  ThumbUp,
  ThumbDown,
  PushPin,
  CheckCircle,
  Reply,
} from '@mui/icons-material';
import { motion } from 'framer-motion';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { forumService, type ForumPost } from '../../services/forumService';
import { PostComposer } from './PostComposer';
import { ForumPostCard } from './ForumPostCard';

export const ForumBoard: React.FC = () => {
  const { moduleId } = useParams<{ moduleId: string }>();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [sort, setSort] = useState<'recent' | 'popular' | 'unsolved'>('recent');
  const [page, setPage] = useState(1);
  const [searchQuery, setSearchQuery] = useState('');
  const [showComposer, setShowComposer] = useState(false);
  const limit = 20;

  // Fetch forum posts
  const {
    data: postsData,
    isLoading,
    error,
  } = useQuery({
    queryKey: ['forum-posts', moduleId, sort, page, searchQuery],
    queryFn: () => {
      if (searchQuery) {
        return forumService.searchPosts(searchQuery, moduleId ? Number(moduleId) : undefined, limit, (page - 1) * limit);
      }
      return forumService.getModulePosts(Number(moduleId || 0), sort, limit, (page - 1) * limit);
    },
    enabled: !!moduleId,
  });

  const handleSortChange = (newSort: 'recent' | 'popular' | 'unsolved') => {
    setSort(newSort);
    setPage(1);
  };

  const handlePageChange = (_event: React.ChangeEvent<unknown>, value: number) => {
    setPage(value);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handlePostCreated = () => {
    setShowComposer(false);
    queryClient.invalidateQueries({ queryKey: ['forum-posts'] });
  };

  const totalPages = postsData ? Math.ceil(postsData.total / limit) : 0;

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" component="h1">
          Discussion Forum
        </Typography>
        <Button
          variant="contained"
          startIcon={<Add />}
          onClick={() => setShowComposer(true)}
        >
          New Post
        </Button>
      </Box>

      {showComposer && (
        <PostComposer
          moduleId={moduleId ? Number(moduleId) : undefined}
          onPostCreated={handlePostCreated}
          onCancel={() => setShowComposer(false)}
        />
      )}

      <Box sx={{ display: 'flex', gap: 2, mb: 3, flexWrap: 'wrap' }}>
        <TextField
          placeholder="Search posts..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          size="small"
          sx={{ flexGrow: 1, minWidth: 200 }}
          InputProps={{
            startAdornment: <Search sx={{ mr: 1, color: 'text.secondary' }} />,
          }}
        />
        <FormControl size="small" sx={{ minWidth: 150 }}>
          <InputLabel>Sort by</InputLabel>
          <Select value={sort} label="Sort by" onChange={(e) => handleSortChange(e.target.value as any)}>
            <MenuItem value="recent">Most Recent</MenuItem>
            <MenuItem value="popular">Most Popular</MenuItem>
            <MenuItem value="unsolved">Unsolved</MenuItem>
          </Select>
        </FormControl>
      </Box>

      {isLoading && (
        <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
          <CircularProgress />
        </Box>
      )}

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          Failed to load forum posts. Please try again.
        </Alert>
      )}

      {postsData && postsData.posts.length === 0 && (
        <Paper sx={{ p: 4, textAlign: 'center' }}>
          <Typography variant="h6" color="text.secondary">
            No posts yet. Be the first to start a discussion!
          </Typography>
        </Paper>
      )}

      {postsData && postsData.posts.length > 0 && (
        <>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mb: 3 }}>
            {postsData.posts.map((post) => (
              <ForumPostCard key={post.id} post={post} />
            ))}
          </Box>

          {totalPages > 1 && (
            <Box sx={{ display: 'flex', justifyContent: 'center', mt: 3 }}>
              <Pagination
                count={totalPages}
                page={page}
                onChange={handlePageChange}
                color="primary"
              />
            </Box>
          )}
        </>
      )}
    </Box>
  );
};

