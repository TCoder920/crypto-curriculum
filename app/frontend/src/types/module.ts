/** Module and Lesson types */
export type Track = "user" | "analyst" | "developer" | "architect";

export interface Lesson {
  id: number;
  module_id: number;
  title: string;
  content: string;
  order_index: number;
  estimated_minutes: number | null;
  lesson_type: string;
  media_url: string | null;
  is_active: boolean;
  created_at: string;
  updated_at: string | null;
}

export interface Module {
  id: number;
  title: string;
  description: string | null;
  track: Track;
  order_index: number;
  duration_hours: number;
  prerequisites: number[] | null;
  learning_objectives: string[] | null;
  is_active: boolean;
  is_published: boolean;
  created_at: string;
  updated_at: string | null;
  can_access?: boolean;
  missing_prerequisites?: number[];
}

export interface ModuleDetail extends Module {
  lessons: Lesson[];
}

export interface ModuleListResponse {
  modules: Module[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

