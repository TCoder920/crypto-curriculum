/** Analytics service */
import apiClient from './api';

export interface StudentAnalytics {
  user_id: number;
  total_modules_completed: number;
  total_modules_started: number;
  average_score: number;
  total_attempts: number;
  current_streak_days: number;
  total_achievements: number;
  total_points: number;
  modules_by_status: {
    completed: number;
    in_progress: number;
    not_started: number;
  };
  scores_by_module: Array<{
    module_id: number;
    module_title: string;
    best_score: number;
  }>;
  recent_activity: Array<{
    module_id: number;
    module_title: string;
    status: string;
    updated_at: string | null;
  }>;
}

export interface CohortAnalytics {
  cohort_id: number;
  cohort_name: string;
  total_students: number;
  active_students: number;
  average_progress: number;
  average_score: number;
  completion_rate: number;
  students_by_progress: {
    completed: number;
    in_progress: number;
    not_started: number;
  };
  top_performers: Array<{
    user_id: number;
    modules_completed: number;
  }>;
  at_risk_students: Array<{
    user_id: number;
    reason: string;
  }>;
}

export interface PlatformAnalytics {
  total_users: number;
  total_students: number;
  total_instructors: number;
  total_modules: number;
  total_assessments: number;
  total_attempts: number;
  average_completion_rate: number;
  average_score: number;
  active_users_last_30_days: number;
  new_users_last_30_days: number;
  modules_by_track: Record<string, number>;
  completion_by_track: Record<string, number>;
}

export const analyticsService = {
  /**
   * Get analytics for a specific student
   */
  async getStudentAnalytics(userId: number): Promise<StudentAnalytics> {
    const response = await apiClient.get<StudentAnalytics>(`/analytics/student/${userId}`);
    return response.data;
  },

  /**
   * Get analytics for a cohort (instructor/admin only)
   */
  async getCohortAnalytics(cohortId: number): Promise<CohortAnalytics> {
    const response = await apiClient.get<CohortAnalytics>(`/analytics/cohort/${cohortId}`);
    return response.data;
  },

  /**
   * Get platform-wide analytics (admin only)
   */
  async getPlatformAnalytics(): Promise<PlatformAnalytics> {
    const response = await apiClient.get<PlatformAnalytics>('/analytics/platform');
    return response.data;
  },
};

