/** Notification bell component - displays notification count and dropdown */
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  IconButton,
  Badge,
  Popover,
  Typography,
  Box,
  List,
  ListItem,
  ListItemText,
  Button,
  Divider,
} from '@mui/material';
import { Notifications as NotificationsIcon } from '@mui/icons-material';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { notificationService, type Notification } from '../../services/notificationService';
import { NotificationList } from './NotificationList';

export const NotificationBell: React.FC = () => {
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [anchorEl, setAnchorEl] = useState<HTMLElement | null>(null);

  const { data: notificationsData } = useQuery({
    queryKey: ['notifications', 'unread'],
    queryFn: () => notificationService.getNotifications(true, 10, 0),
    refetchInterval: 30000, // Refetch every 30 seconds
  });

  const markAllReadMutation = useMutation({
    mutationFn: () => notificationService.markAllRead(),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['notifications'] });
    },
  });

  const handleClick = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleNotificationClick = (notification: Notification) => {
    if (notification.link) {
      navigate(notification.link);
    }
    handleClose();
  };

  const handleMarkAllRead = () => {
    markAllReadMutation.mutate();
  };

  const unreadCount = notificationsData?.unread_count || 0;
  const open = Boolean(anchorEl);

  return (
    <>
      <IconButton onClick={handleClick} color="inherit">
        <Badge badgeContent={unreadCount} color="error">
          <NotificationsIcon />
        </Badge>
      </IconButton>

      <Popover
        open={open}
        anchorEl={anchorEl}
        onClose={handleClose}
        anchorOrigin={{
          vertical: 'bottom',
          horizontal: 'right',
        }}
        transformOrigin={{
          vertical: 'top',
          horizontal: 'right',
        }}
        PaperProps={{
          sx: { width: 400, maxHeight: 500, mt: 1 },
        }}
      >
        <Box sx={{ p: 2 }}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
            <Typography variant="h6">Notifications</Typography>
            {unreadCount > 0 && (
              <Button size="small" onClick={handleMarkAllRead}>
                Mark all read
              </Button>
            )}
          </Box>
          <Divider sx={{ mb: 1 }} />
          <NotificationList
            onNotificationClick={handleNotificationClick}
            limit={10}
          />
        </Box>
      </Popover>
    </>
  );
};

