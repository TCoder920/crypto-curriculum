/** AI Chat Interface component */
import React, { useState, useEffect, useRef } from 'react';
import {
  Box,
  TextField,
  IconButton,
  Typography,
  CircularProgress,
  Alert,
  Avatar,
} from '@mui/material';
import { Send, SmartToy } from '@mui/icons-material';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { aiAssistantService, type ChatMessage } from '../../services/aiAssistantService';
import { useAuth } from '../../contexts/AuthContext';

interface ChatInterfaceProps {
  moduleId?: number;
  lessonId?: number;
}

export const ChatInterface: React.FC<ChatInterfaceProps> = ({ moduleId, lessonId }) => {
  const { user } = useAuth();
  const queryClient = useQueryClient();
  const [message, setMessage] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const chatContainerRef = useRef<HTMLDivElement>(null);

  const { data: chatHistory } = useQuery({
    queryKey: ['ai-chat-history'],
    queryFn: () => aiAssistantService.getHistory(50),
    enabled: !!user,
  });

  const sendMutation = useMutation({
    mutationFn: (messageText: string) =>
      aiAssistantService.sendMessage({
        message: messageText,
        // Context will be gathered on the backend with full user-specific app context
        // Only include additional context if on a specific module/lesson page
        context: moduleId ? { current_module_id: moduleId, current_lesson_id: lessonId } : undefined,
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['ai-chat-history'] });
      setMessage('');
    },
  });

  useEffect(() => {
    scrollToBottom();
  }, [chatHistory]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!message.trim() || sendMutation.isPending) return;

    sendMutation.mutate(message.trim());
  };

  if (!user) {
    return (
      <Alert severity="info">
        Please log in to use the AI assistant.
      </Alert>
    );
  }

  const messages = chatHistory?.messages || [];

  return (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <Box
        ref={chatContainerRef}
        sx={{
          flexGrow: 1,
          overflow: 'auto',
          p: 2,
          display: 'flex',
          flexDirection: 'column',
          gap: 2,
        }}
      >
        {messages.length === 0 && (
          <Box sx={{ textAlign: 'center', mt: 4 }}>
            <SmartToy sx={{ fontSize: 48, color: 'text.secondary', mb: 2 }} />
            <Typography variant="body1" color="text.secondary">
              Start a conversation! Ask me about blockchain concepts, definitions, or how things work.
            </Typography>
          </Box>
        )}

        {messages.map((msg) => (
          <Box
            key={msg.id}
            sx={{
              display: 'flex',
              gap: 1,
              flexDirection: msg.user_id === user.id ? 'row-reverse' : 'row',
            }}
          >
            <Avatar sx={{ width: 32, height: 32 }}>
              {msg.user_id === user.id ? user.email?.[0].toUpperCase() : 'AI'}
            </Avatar>
            <Box
              sx={{
                maxWidth: '70%',
                bgcolor: msg.user_id === user.id ? 'primary.main' : 'grey.200',
                color: msg.user_id === user.id ? 'white' : 'text.primary',
                p: 1.5,
                borderRadius: 2,
              }}
            >
              <Typography variant="body2" sx={{ whiteSpace: 'pre-wrap' }}>
                {msg.message}
              </Typography>
              {msg.response && (
                <Box sx={{ mt: 1, pt: 1, borderTop: 1, borderColor: 'rgba(255,255,255,0.2)' }}>
                  <Typography variant="body2" sx={{ whiteSpace: 'pre-wrap' }}>
                    {msg.response}
                  </Typography>
                </Box>
              )}
            </Box>
          </Box>
        ))}

        {sendMutation.isPending && (
          <Box sx={{ display: 'flex', gap: 1, alignItems: 'center' }}>
            <Avatar sx={{ width: 32, height: 32 }}>AI</Avatar>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <CircularProgress size={16} />
              <Typography variant="body2" color="text.secondary">
                Thinking...
              </Typography>
            </Box>
          </Box>
        )}

        {sendMutation.isError && (
          <Alert severity="error" sx={{ mt: 1 }}>
            {sendMutation.error instanceof Error
              ? sendMutation.error.message
              : 'Failed to send message. Please try again.'}
          </Alert>
        )}

        <div ref={messagesEndRef} />
      </Box>

      <Box sx={{ p: 2, borderTop: 1, borderColor: 'divider' }}>
        <form onSubmit={handleSubmit}>
          <Box sx={{ display: 'flex', gap: 1 }}>
            <TextField
              fullWidth
              size="small"
              placeholder="Ask a question about the curriculum..."
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              disabled={sendMutation.isPending}
            />
            <IconButton
              type="submit"
              color="primary"
              disabled={!message.trim() || sendMutation.isPending}
            >
              <Send />
            </IconButton>
          </Box>
        </form>
      </Box>
    </Box>
  );
};

