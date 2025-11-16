/** Notification service for API calls */
import { apiClient } from './api';

export interface Notification {
  id: number;
  user_id: number;
  type: 'assessment_graded' | 'forum_reply' | 'announcement' | 'module_unlocked';
  title: string;
  message: string;
  link: string | null;
  is_read: boolean;
  created_at: string;
  read_at: string | null;
}

export interface NotificationListResponse {
  notifications: Notification[];
  total: number;
  unread_count: number;
}

export const notificationService = {
  /** Get user's notifications */
  getNotifications: async (
    unreadOnly: boolean = false,
    limit: number = 50,
    offset: number = 0
  ): Promise<NotificationListResponse> => {
    const response = await apiClient.get('/notifications', {
      params: { unread_only: unreadOnly, limit, offset },
    });
    return response.data;
  },

  /** Mark notification as read/unread */
  updateNotification: async (
    notificationId: number,
    isRead: boolean
  ): Promise<Notification> => {
    const response = await apiClient.patch(`/notifications/${notificationId}`, {
      is_read: isRead,
    });
    return response.data;
  },

  /** Mark all notifications as read */
  markAllRead: async (): Promise<void> => {
    await apiClient.patch('/notifications/mark-all-read');
  },

  /** Delete a notification */
  deleteNotification: async (notificationId: number): Promise<void> => {
    await apiClient.delete(`/notifications/${notificationId}`);
  },
};

