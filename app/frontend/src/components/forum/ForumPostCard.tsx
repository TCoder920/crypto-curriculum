/** Forum post card component - displays a single forum post */
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Paper,
  Box,
  Typography,
  Chip,
  IconButton,
  Button,
  Avatar,
} from '@mui/material';
import {
  ThumbUp,
  ThumbDown,
  PushPin,
  CheckCircle,
  Reply,
} from '@mui/icons-material';
import { motion } from 'framer-motion';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { forumService, type ForumPost } from '../../services/forumService';
import { useAuth } from '../../contexts/AuthContext';

interface ForumPostCardProps {
  post: ForumPost;
}

export const ForumPostCard: React.FC<ForumPostCardProps> = ({ post }) => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const queryClient = useQueryClient();
  const [isVoting, setIsVoting] = useState(false);

  const voteMutation = useMutation({
    mutationFn: (voteType: 'upvote' | 'downvote') =>
      forumService.votePost(post.id, voteType),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['forum-posts'] });
    },
  });

  const handleVote = async (voteType: 'upvote' | 'downvote') => {
    if (!user) {
      navigate('/login');
      return;
    }
    setIsVoting(true);
    try {
      await voteMutation.mutateAsync(voteType);
    } finally {
      setIsVoting(false);
    }
  };

  const handlePostClick = () => {
    if (post.module_id) {
      navigate(`/modules/${post.module_id}/forums/posts/${post.id}`);
    }
  };

  const getAuthorName = () => {
    return post.author.full_name || post.author.username || 'Anonymous';
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      <Paper
        sx={{
          p: 2,
          cursor: 'pointer',
          '&:hover': {
            boxShadow: 4,
          },
        }}
        onClick={handlePostClick}
      >
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 1 }}>
            <IconButton
              size="small"
              color={post.user_vote === 'upvote' ? 'primary' : 'default'}
              disabled={isVoting || !user}
              onClick={(e) => {
                e.stopPropagation();
                handleVote('upvote');
              }}
            >
              <ThumbUp fontSize="small" />
            </IconButton>
            <Typography variant="body2" fontWeight="bold">
              {post.upvotes}
            </Typography>
            <IconButton
              size="small"
              color={post.user_vote === 'downvote' ? 'error' : 'default'}
              disabled={isVoting || !user}
              onClick={(e) => {
                e.stopPropagation();
                handleVote('downvote');
              }}
            >
              <ThumbDown fontSize="small" />
            </IconButton>
          </Box>

          <Box sx={{ flexGrow: 1 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
              {post.is_pinned && (
                <Chip
                  icon={<PushPin />}
                  label="Pinned"
                  size="small"
                  color="primary"
                />
              )}
              {post.is_solved && (
                <Chip
                  icon={<CheckCircle />}
                  label="Solved"
                  size="small"
                  color="success"
                />
              )}
              <Typography variant="h6" component="h3" sx={{ flexGrow: 1 }}>
                {post.title}
              </Typography>
            </Box>

            <Typography
              variant="body2"
              color="text.secondary"
              sx={{
                mb: 2,
                overflow: 'hidden',
                textOverflow: 'ellipsis',
                display: '-webkit-box',
                WebkitLineClamp: 2,
                WebkitBoxOrient: 'vertical',
              }}
            >
              {post.content}
            </Typography>

            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <Avatar sx={{ width: 24, height: 24 }}>
                  {getAuthorName()[0].toUpperCase()}
                </Avatar>
                <Typography variant="caption" color="text.secondary">
                  {getAuthorName()} • {new Date(post.created_at).toLocaleDateString()}
                </Typography>
              </Box>
              <Button
                size="small"
                startIcon={<Reply />}
                onClick={(e) => {
                  e.stopPropagation();
                  handlePostClick();
                }}
              >
                {post.reply_count} {post.reply_count === 1 ? 'reply' : 'replies'}
              </Button>
            </Box>
          </Box>
        </Box>
      </Paper>
    </motion.div>
  );
};

