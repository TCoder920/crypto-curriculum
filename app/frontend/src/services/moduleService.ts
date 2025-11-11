/** Module service */
import apiClient from './api';
import type { Module, ModuleDetail, Lesson } from '../types/module';

export const moduleService = {
  /**
   * Get all published modules
   */
  async getModules(): Promise<{ modules: Module[]; total: number }> {
    const response = await apiClient.get<{ modules: Module[]; total: number }>('/modules');
    return response.data;
  },

  /**
   * Get module details with lessons
   */
  async getModuleDetail(moduleId: number): Promise<ModuleDetail> {
    const response = await apiClient.get<ModuleDetail>(`/modules/${moduleId}`);
    return response.data;
  },

  /**
   * Get all lessons for a module
   */
  async getModuleLessons(moduleId: number): Promise<Lesson[]> {
    const response = await apiClient.get<Lesson[]>(`/modules/${moduleId}/lessons`);
    return response.data;
  },

  /**
   * Get a specific lesson
   */
  async getLesson(lessonId: number): Promise<Lesson> {
    const response = await apiClient.get<Lesson>(`/lessons/${lessonId}`);
    return response.data;
  },
};


