/** Reply thread component - displays replies to a post */
import React, { useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  Avatar,
  IconButton,
  Button,
  Divider,
} from '@mui/material';
import {
  ThumbUp,
  ThumbDown,
  Reply as ReplyIcon,
} from '@mui/icons-material';
import { motion } from 'framer-motion';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { forumService, type ForumPost } from '../../services/forumService';
import { useAuth } from '../../contexts/AuthContext';
import { PostComposer } from './PostComposer';

interface ReplyThreadProps {
  postId: number;
}

export const ReplyThread: React.FC<ReplyThreadProps> = ({ postId }) => {
  const { user } = useAuth();
  const queryClient = useQueryClient();
  const [showReplyComposer, setShowReplyComposer] = useState(false);
  const [replyingTo, setReplyingTo] = useState<number | null>(null);
  const [isVoting, setIsVoting] = useState<number | null>(null);

  const { data: replies, isLoading } = useQuery({
    queryKey: ['forum-replies', postId],
    queryFn: () => forumService.getPostReplies(postId),
  });

  const voteMutation = useMutation({
    mutationFn: ({ postId, voteType }: { postId: number; voteType: 'upvote' | 'downvote' }) =>
      forumService.votePost(postId, voteType),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['forum-replies', postId] });
      queryClient.invalidateQueries({ queryKey: ['forum-posts'] });
    },
  });

  const handleVote = async (replyId: number, voteType: 'upvote' | 'downvote') => {
    if (!user) return;
    setIsVoting(replyId);
    try {
      await voteMutation.mutateAsync({ postId: replyId, voteType });
    } finally {
      setIsVoting(null);
    }
  };

  const handleReplyCreated = () => {
    setShowReplyComposer(false);
    setReplyingTo(null);
    queryClient.invalidateQueries({ queryKey: ['forum-replies', postId] });
  };

  const getAuthorName = (post: ForumPost) => {
    return post.author.full_name || post.author.username || 'Anonymous';
  };

  if (isLoading) {
    return <Typography>Loading replies...</Typography>;
  }

  return (
    <Box sx={{ mt: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
        <Typography variant="h6">
          Replies ({replies?.length || 0})
        </Typography>
        {user && (
          <Button
            variant="outlined"
            size="small"
            startIcon={<ReplyIcon />}
            onClick={() => {
              setShowReplyComposer(true);
              setReplyingTo(null);
            }}
          >
            Add Reply
          </Button>
        )}
      </Box>

      {showReplyComposer && (
        <Box sx={{ mb: 3 }}>
          <PostComposer
            parentPostId={postId}
            onPostCreated={handleReplyCreated}
            onCancel={() => {
              setShowReplyComposer(false);
              setReplyingTo(null);
            }}
          />
        </Box>
      )}

      {replies && replies.length === 0 && (
        <Paper sx={{ p: 3, textAlign: 'center' }}>
          <Typography color="text.secondary">
            No replies yet. Be the first to reply!
          </Typography>
        </Paper>
      )}

      {replies && replies.length > 0 && (
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
          {replies.map((reply) => (
            <motion.div
              key={reply.id}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.3 }}
            >
              <Paper sx={{ p: 2 }}>
                <Box sx={{ display: 'flex', gap: 2 }}>
                  <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 1 }}>
                    <IconButton
                      size="small"
                      color={reply.user_vote === 'upvote' ? 'primary' : 'default'}
                      disabled={isVoting === reply.id || !user}
                      onClick={() => handleVote(reply.id, 'upvote')}
                    >
                      <ThumbUp fontSize="small" />
                    </IconButton>
                    <Typography variant="body2" fontWeight="bold">
                      {reply.upvotes}
                    </Typography>
                    <IconButton
                      size="small"
                      color={reply.user_vote === 'downvote' ? 'error' : 'default'}
                      disabled={isVoting === reply.id || !user}
                      onClick={() => handleVote(reply.id, 'downvote')}
                    >
                      <ThumbDown fontSize="small" />
                    </IconButton>
                  </Box>

                  <Box sx={{ flexGrow: 1 }}>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                      <Avatar sx={{ width: 24, height: 24 }}>
                        {getAuthorName(reply)[0].toUpperCase()}
                      </Avatar>
                      <Typography variant="body2" fontWeight="bold">
                        {getAuthorName(reply)}
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        • {new Date(reply.created_at).toLocaleDateString()}
                      </Typography>
                    </Box>
                    <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap' }}>
                      {reply.content}
                    </Typography>
                  </Box>
                </Box>
              </Paper>
            </motion.div>
          ))}
        </Box>
      )}
    </Box>
  );
};

