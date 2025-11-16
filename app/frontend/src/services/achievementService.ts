/** Achievement service */
import apiClient from './api';

export interface Achievement {
  id: number;
  name: string;
  description: string | null;
  icon: string | null;
  category: string | null;
  points: number;
  earned: boolean;
  earned_at: string | null;
  progress: Record<string, any> | null;
}

export interface AchievementStats {
  total_achievements: number;
  earned_count: number;
  completion_percentage: number;
  total_points: number;
  by_category: Record<string, number>;
}

export interface AchievementUnlockResponse {
  unlocked_count: number;
  unlocked_achievements: Array<{
    id: number;
    name: string;
    description: string | null;
    icon: string | null;
  }>;
}

export const achievementService = {
  /**
   * Get all achievements with user's earned status
   */
  async getAchievements(): Promise<Achievement[]> {
    const response = await apiClient.get<Achievement[]>('/achievements');
    return response.data;
  },

  /**
   * Get achievement statistics for current user
   */
  async getStats(): Promise<AchievementStats> {
    const response = await apiClient.get<AchievementStats>('/achievements/stats');
    return response.data;
  },

  /**
   * Manually trigger achievement check (for testing)
   */
  async checkAchievements(
    eventType: string,
    eventData?: Record<string, any>
  ): Promise<AchievementUnlockResponse> {
    const response = await apiClient.post<AchievementUnlockResponse>(
      '/achievements/check',
      { event_type: eventType, event_data: eventData }
    );
    return response.data;
  },
};

