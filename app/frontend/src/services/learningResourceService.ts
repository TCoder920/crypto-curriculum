/** Learning resource service */
import apiClient from './api';

export interface LearningResource {
  id: number;
  title: string;
  url: string;
  resource_type: string | null;
  difficulty: string | null;
  upvotes: number;
  module_id: number | null;
  module_title: string | null;
  added_by: number | null;
  created_at: string;
}

export interface LearningResourceCreate {
  title: string;
  url: string;
  resource_type?: string | null;
  difficulty?: string | null;
  module_id?: number | null;
}

export interface LearningResourceUpdate {
  title?: string;
  url?: string;
  resource_type?: string | null;
  difficulty?: string | null;
}

export const learningResourceService = {
  /**
   * Get all learning resources with optional filters
   */
  async getResources(params?: {
    module_id?: number;
    resource_type?: string;
    difficulty?: string;
  }): Promise<LearningResource[]> {
    const response = await apiClient.get<LearningResource[]>('/learning-resources', { params });
    return response.data;
  },

  /**
   * Get a specific learning resource
   */
  async getResource(resourceId: number): Promise<LearningResource> {
    const response = await apiClient.get<LearningResource>(`/learning-resources/${resourceId}`);
    return response.data;
  },

  /**
   * Create a new learning resource
   */
  async createResource(resource: LearningResourceCreate): Promise<LearningResource> {
    const response = await apiClient.post<LearningResource>('/learning-resources', resource);
    return response.data;
  },

  /**
   * Update a learning resource
   */
  async updateResource(
    resourceId: number,
    resource: LearningResourceUpdate
  ): Promise<LearningResource> {
    const response = await apiClient.put<LearningResource>(
      `/learning-resources/${resourceId}`,
      resource
    );
    return response.data;
  },

  /**
   * Upvote a learning resource
   */
  async upvoteResource(resourceId: number): Promise<LearningResource> {
    const response = await apiClient.post<LearningResource>(
      `/learning-resources/${resourceId}/upvote`
    );
    return response.data;
  },

  /**
   * Delete a learning resource (instructor/admin only)
   */
  async deleteResource(resourceId: number): Promise<void> {
    await apiClient.delete(`/learning-resources/${resourceId}`);
  },
};

