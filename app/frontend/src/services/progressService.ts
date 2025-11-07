/** Progress tracking API service */
import apiClient from "./api";
import type { Progress, ProgressListResponse, ProgressUpdate } from "../types/progress";

export const progressService = {
  /** Get all progress for current user */
  async getProgress(): Promise<ProgressListResponse> {
    const response = await apiClient.get<ProgressListResponse>("/progress");
    return response.data;
  },

  /** Get progress for a specific module */
  async getModuleProgress(moduleId: number): Promise<Progress> {
    const response = await apiClient.get<Progress>(`/progress/${moduleId}`);
    return response.data;
  },

  /** Mark a module as started */
  async startModule(moduleId: number): Promise<Progress> {
    const response = await apiClient.post<Progress>(`/progress/start/${moduleId}`);
    return response.data;
  },

  /** Mark a module as completed */
  async completeModule(moduleId: number): Promise<Progress> {
    const response = await apiClient.post<Progress>(`/progress/complete/${moduleId}`);
    return response.data;
  },

  /** Update progress for a module */
  async updateProgress(moduleId: number, update: ProgressUpdate): Promise<Progress> {
    const response = await apiClient.patch<Progress>(`/progress/${moduleId}`, update);
    return response.data;
  },
};

