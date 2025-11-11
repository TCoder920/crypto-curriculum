/** Cohort service */
import apiClient from './api';

export interface CohortMember {
  id: number;
  cohort_id: number;
  user_id: number;
  role: string;
  joined_at: string;
  user?: {
    id: number;
    email: string;
    full_name?: string;
    username?: string;
  };
}

export interface Cohort {
  id: number;
  name: string;
  description?: string;
  start_date?: string;
  end_date?: string;
  is_active: boolean;
  cancelled_at?: string;
  created_by?: number;
  created_at: string;
  updated_at?: string;
  members: CohortMember[];
  member_count: number;
  student_count: number;
  instructor_count: number;
}

export interface CohortListResponse {
  cohorts: Cohort[];
  total: number;
}

export interface CohortCreate {
  name: string;
  description?: string;
  start_date?: string;
  end_date?: string;
  is_active?: boolean;
}

export interface CohortUpdate {
  name?: string;
  description?: string;
  start_date?: string;
  end_date?: string;
  is_active?: boolean;
}

export interface CohortMemberCreate {
  user_id: number;
  role: 'student' | 'instructor';
}

export const cohortService = {
  /**
   * Get all cohorts
   */
  async getCohorts(activeOnly?: boolean): Promise<CohortListResponse> {
    const params = activeOnly ? { active_only: true } : {};
    const response = await apiClient.get<CohortListResponse>('/cohorts', { params });
    return response.data;
  },

  /**
   * Get cohort details with members
   */
  async getCohort(cohortId: number): Promise<Cohort> {
    const response = await apiClient.get<Cohort>(`/cohorts/${cohortId}`);
    return response.data;
  },

  /**
   * Create a new cohort
   */
  async createCohort(data: CohortCreate): Promise<Cohort> {
    const response = await apiClient.post<Cohort>('/cohorts', data);
    return response.data;
  },

  /**
   * Add a member to a cohort
   */
  async addMember(cohortId: number, data: CohortMemberCreate): Promise<CohortMember> {
    const response = await apiClient.post<CohortMember>(`/cohorts/${cohortId}/members`, data);
    return response.data;
  },

  /**
   * Remove a member from a cohort
   */
  async removeMember(cohortId: number, userId: number): Promise<void> {
    await apiClient.delete(`/cohorts/${cohortId}/members/${userId}`);
  },

  /**
   * Update a cohort
   */
  async updateCohort(cohortId: number, data: CohortUpdate): Promise<Cohort> {
    const response = await apiClient.put<Cohort>(`/cohorts/${cohortId}`, data);
    return response.data;
  },

  /**
   * Cancel a future or inactive cohort
   */
  async cancelCohort(cohortId: number): Promise<Cohort> {
    const response = await apiClient.patch<Cohort>(`/cohorts/${cohortId}/cancel`);
    return response.data;
  },

  /**
   * Delete a cohort (only after 14 days of cancellation and no students)
   */
  async deleteCohort(cohortId: number): Promise<void> {
    await apiClient.delete(`/cohorts/${cohortId}`);
  },
};

