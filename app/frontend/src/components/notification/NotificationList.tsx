/** Notification list component - displays list of notifications */
import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  List,
  ListItem,
  ListItemText,
  ListItemButton,
  Typography,
  Box,
  IconButton,
  Chip,
  CircularProgress,
  Alert,
} from '@mui/material';
import {
  CheckCircle,
  Forum,
  Assessment,
  Announcement,
  LockOpen,
  Close,
} from '@mui/icons-material';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { notificationService, type Notification } from '../../services/notificationService';

interface NotificationListProps {
  onNotificationClick?: (notification: Notification) => void;
  unreadOnly?: boolean;
  limit?: number;
}

const getNotificationIcon = (type: Notification['type']) => {
  switch (type) {
    case 'forum_reply':
      return <Forum />;
    case 'assessment_graded':
      return <Assessment />;
    case 'announcement':
      return <Announcement />;
    case 'module_unlocked':
      return <LockOpen />;
    default:
      return <CheckCircle />;
  }
};

const getNotificationColor = (type: Notification['type']) => {
  switch (type) {
    case 'forum_reply':
      return 'primary';
    case 'assessment_graded':
      return 'success';
    case 'announcement':
      return 'warning';
    case 'module_unlocked':
      return 'info';
    default:
      return 'default';
  }
};

export const NotificationList: React.FC<NotificationListProps> = ({
  onNotificationClick,
  unreadOnly = false,
  limit = 50,
}) => {
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const { data: notificationsData, isLoading, error } = useQuery({
    queryKey: ['notifications', unreadOnly ? 'unread' : 'all'],
    queryFn: () => notificationService.getNotifications(unreadOnly, limit, 0),
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, isRead }: { id: number; isRead: boolean }) =>
      notificationService.updateNotification(id, isRead),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['notifications'] });
    },
  });

  const deleteMutation = useMutation({
    mutationFn: (id: number) => notificationService.deleteNotification(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['notifications'] });
    },
  });

  const handleNotificationClick = (notification: Notification) => {
    if (!notification.is_read) {
      updateMutation.mutate({ id: notification.id, isRead: true });
    }
    if (onNotificationClick) {
      onNotificationClick(notification);
    } else if (notification.link) {
      navigate(notification.link);
    }
  };

  const handleDelete = (e: React.MouseEvent, notificationId: number) => {
    e.stopPropagation();
    deleteMutation.mutate(notificationId);
  };

  if (isLoading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', p: 2 }}>
        <CircularProgress size={24} />
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error">
        Failed to load notifications. Please try again.
      </Alert>
    );
  }

  if (!notificationsData || notificationsData.notifications.length === 0) {
    return (
      <Box sx={{ p: 2, textAlign: 'center' }}>
        <Typography variant="body2" color="text.secondary">
          No notifications
        </Typography>
      </Box>
    );
  }

  return (
    <List sx={{ maxHeight: 400, overflow: 'auto' }}>
      {notificationsData.notifications.map((notification) => (
        <ListItem
          key={notification.id}
          disablePadding
          sx={{
            bgcolor: notification.is_read ? 'transparent' : 'action.hover',
            '&:hover': { bgcolor: 'action.selected' },
          }}
        >
          <ListItemButton onClick={() => handleNotificationClick(notification)}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, flexGrow: 1 }}>
              <Chip
                icon={getNotificationIcon(notification.type)}
                label={notification.type.replace('_', ' ')}
                size="small"
                color={getNotificationColor(notification.type) as any}
                sx={{ minWidth: 100 }}
              />
              <ListItemText
                primary={notification.title}
                secondary={notification.message}
                primaryTypographyProps={{
                  fontWeight: notification.is_read ? 'normal' : 'bold',
                }}
              />
              <IconButton
                size="small"
                onClick={(e) => handleDelete(e, notification.id)}
                sx={{ ml: 1 }}
              >
                <Close fontSize="small" />
              </IconButton>
            </Box>
          </ListItemButton>
        </ListItem>
      ))}
    </List>
  );
};

