/** Module and lesson types */
export type Track = 'user' | 'analyst' | 'developer' | 'architect';

export interface Module {
  id: number;
  title: string;
  description: string | null;
  track: Track;
  order_index: number;
  duration_hours: number;
  prerequisites: number[] | null;
  learning_objectives: string[] | null;
  is_published: boolean;
}

export interface Lesson {
  id: number;
  module_id: number;
  title: string;
  content: string;
  order_index: number;
  estimated_minutes: number | null;
  lesson_type: string;
}

export interface ModuleDetail extends Module {
  lessons: Lesson[];
  has_assessment: boolean;
}


