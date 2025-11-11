/** Grading service */
import apiClient from './api';

export interface GradingQueueItem {
  attempt_id: number;
  user_id: number;
  user_name: string;
  user_email: string;
  assessment_id: number;
  question_text: string;
  question_type: string;
  user_answer?: string;
  correct_answer: string;
  module_id: number;
  module_title: string;
  attempted_at: string;
  time_spent_seconds?: number;
}

export interface GradingQueueResponse {
  items: GradingQueueItem[];
  total: number;
}

export interface GradeSubmission {
  is_correct: boolean;
  points_earned: number;
  feedback?: string;
  partial_credit?: boolean;
}

export interface GradedAttempt {
  id: number;
  user_id: number;
  assessment_id: number;
  user_answer?: string;
  is_correct: boolean;
  points_earned: number;
  review_status: string;
  graded_by?: number;
  feedback?: string;
  partial_credit: boolean;
  graded_at?: string;
  attempted_at: string;
}

export interface GradingHistoryResponse {
  items: GradedAttempt[];
  total: number;
}

export const gradingService = {
  /**
   * Get grading queue (pending reviews)
   */
  async getGradingQueue(limit = 50, offset = 0): Promise<GradingQueueResponse> {
    const response = await apiClient.get<GradingQueueResponse>('/grading/queue', {
      params: { limit, offset },
    });
    return response.data;
  },

  /**
   * Grade an attempt
   */
  async gradeAttempt(attemptId: number, grade: GradeSubmission): Promise<GradedAttempt> {
    const response = await apiClient.post<GradedAttempt>(`/grading/${attemptId}`, grade);
    return response.data;
  },

  /**
   * Get grading history
   */
  async getGradingHistory(
    userId?: number,
    moduleId?: number,
    limit = 50,
    offset = 0
  ): Promise<GradingHistoryResponse> {
    const params: Record<string, any> = { limit, offset };
    if (userId) params.user_id = userId;
    if (moduleId) params.module_id = moduleId;
    
    const response = await apiClient.get<GradingHistoryResponse>('/grading/history', { params });
    return response.data;
  },
};

