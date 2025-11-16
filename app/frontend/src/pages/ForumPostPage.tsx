/** Forum post page - displays a single forum post with replies */
import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Container,
  Paper,
  Typography,
  Box,
  Button,
  IconButton,
  Chip,
  Avatar,
  CircularProgress,
  Alert,
} from '@mui/material';
import {
  ArrowBack,
  ThumbUp,
  ThumbDown,
  PushPin,
  CheckCircle,
} from '@mui/icons-material';
import { motion } from 'framer-motion';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { forumService, type ForumPost } from '../services/forumService';
import { useAuth } from '../contexts/AuthContext';
import { ReplyThread } from '../components/forum/ReplyThread';
import { PostComposer } from '../components/forum/PostComposer';
import ReactMarkdown from 'react-markdown';

export const ForumPostPage: React.FC = () => {
  const { moduleId, postId } = useParams<{ moduleId: string; postId: string }>();
  const navigate = useNavigate();
  const { user } = useAuth();
  const queryClient = useQueryClient();
  const [isVoting, setIsVoting] = React.useState(false);
  const [showReplyComposer, setShowReplyComposer] = React.useState(false);

  const { data: post, isLoading, error } = useQuery({
    queryKey: ['forum-post', postId],
    queryFn: () => forumService.getPost(Number(postId)),
    enabled: !!postId,
  });

  const voteMutation = useMutation({
    mutationFn: (voteType: 'upvote' | 'downvote') =>
      forumService.votePost(Number(postId), voteType),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['forum-post', postId] });
    },
  });

  const markSolvedMutation = useMutation({
    mutationFn: () => forumService.markSolved(Number(postId)),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['forum-post', postId] });
    },
  });

  const pinMutation = useMutation({
    mutationFn: () => forumService.pinPost(Number(postId)),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['forum-post', postId] });
    },
  });

  const handleVote = async (voteType: 'upvote' | 'downvote') => {
    if (!user) return;
    setIsVoting(true);
    try {
      await voteMutation.mutateAsync(voteType);
    } finally {
      setIsVoting(false);
    }
  };

  const getAuthorName = (post: ForumPost) => {
    return post.author.full_name || post.author.username || 'Anonymous';
  };

  if (isLoading) {
    return (
      <Container maxWidth="lg" sx={{ py: 4, display: 'flex', justifyContent: 'center' }}>
        <CircularProgress />
      </Container>
    );
  }

  if (error || !post) {
    return (
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <Alert severity="error">Failed to load post. Please try again.</Alert>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Button
        startIcon={<ArrowBack />}
        onClick={() => navigate(moduleId ? `/modules/${moduleId}/forums` : '/modules')}
        sx={{ mb: 2 }}
      >
        Back to Forum
      </Button>

      <Paper sx={{ p: 3, mb: 3 }}>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 1 }}>
            <IconButton
              size="small"
              color={post.user_vote === 'upvote' ? 'primary' : 'default'}
              disabled={isVoting || !user}
              onClick={() => handleVote('upvote')}
            >
              <ThumbUp />
            </IconButton>
            <Typography variant="h6" fontWeight="bold">
              {post.upvotes}
            </Typography>
            <IconButton
              size="small"
              color={post.user_vote === 'downvote' ? 'error' : 'default'}
              disabled={isVoting || !user}
              onClick={() => handleVote('downvote')}
            >
              <ThumbDown />
            </IconButton>
          </Box>

          <Box sx={{ flexGrow: 1 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
              {post.is_pinned && (
                <Chip icon={<PushPin />} label="Pinned" size="small" color="primary" />
              )}
              {post.is_solved && (
                <Chip
                  icon={<CheckCircle />}
                  label="Solved"
                  size="small"
                  color="success"
                />
              )}
              <Typography variant="h4" component="h1" sx={{ flexGrow: 1 }}>
                {post.title}
              </Typography>
            </Box>

            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
              <Avatar>{getAuthorName(post)[0].toUpperCase()}</Avatar>
              <Typography variant="body2" color="text.secondary">
                {getAuthorName(post)} • {new Date(post.created_at).toLocaleDateString()}
              </Typography>
              {user && user.id === post.user_id && (
                <Button
                  size="small"
                  onClick={() => markSolvedMutation.mutate()}
                  disabled={markSolvedMutation.isPending}
                >
                  {post.is_solved ? 'Mark as Unsolved' : 'Mark as Solved'}
                </Button>
              )}
            </Box>

            <Box sx={{ mb: 2 }}>
              <ReactMarkdown>{post.content}</ReactMarkdown>
            </Box>
          </Box>
        </Box>
      </Paper>

      <ReplyThread postId={post.id} />
    </Container>
  );
};

