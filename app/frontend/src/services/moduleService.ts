/** Module and Lesson API service */
import apiClient from "./api";
import type { Module, ModuleDetail, ModuleListResponse, Lesson, Track } from "../types/module";

export const moduleService = {
  /** Get all modules with optional filtering */
  async getModules(
    track?: Track,
    page: number = 1,
    pageSize: number = 20
  ): Promise<ModuleListResponse> {
    const params = new URLSearchParams();
    if (track) params.append("track", track);
    params.append("page", page.toString());
    params.append("page_size", pageSize.toString());

    const response = await apiClient.get<ModuleListResponse>(`/modules?${params.toString()}`);
    return response.data;
  },

  /** Get module details with lessons */
  async getModule(moduleId: number): Promise<ModuleDetail> {
    const response = await apiClient.get<ModuleDetail>(`/modules/${moduleId}`);
    return response.data;
  },

  /** Get all lessons for a module */
  async getModuleLessons(moduleId: number): Promise<Lesson[]> {
    const response = await apiClient.get<Lesson[]>(`/modules/${moduleId}/lessons`);
    return response.data;
  },

  /** Get lesson content */
  async getLesson(lessonId: number): Promise<Lesson> {
    const response = await apiClient.get<Lesson>(`/modules/lessons/${lessonId}`);
    return response.data;
  },
};

