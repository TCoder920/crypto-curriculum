/** Assessment service */
import apiClient from './api';
import type {
  AssessmentListResponse,
  AssessmentSubmit,
  AssessmentSubmitResponse,
  ModuleResultsResponse,
} from '../types/assessment';

export const assessmentService = {
  /**
   * Get all assessment questions for a module
   */
  async getModuleAssessments(moduleId: number): Promise<AssessmentListResponse> {
    const response = await apiClient.get<AssessmentListResponse>(
      `/modules/${moduleId}/assessments`
    );
    return response.data;
  },

  /**
   * Submit an answer to an assessment question
   */
  async submitAnswer(
    assessmentId: number,
    submission: AssessmentSubmit
  ): Promise<AssessmentSubmitResponse> {
    const response = await apiClient.post<AssessmentSubmitResponse>(
      `/assessments/${assessmentId}/submit`,
      submission
    );
    return response.data;
  },

  /**
   * Get user's assessment results for a module
   */
  async getModuleResults(moduleId: number): Promise<ModuleResultsResponse> {
    const response = await apiClient.get<ModuleResultsResponse>(
      `/assessments/results/${moduleId}`
    );
    return response.data;
  },
};

