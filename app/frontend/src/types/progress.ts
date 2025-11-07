/** Progress tracking types */
export type ProgressStatus = "not_started" | "in_progress" | "completed";

export interface Progress {
  id: number;
  user_id: number;
  module_id: number;
  status: ProgressStatus;
  completion_percentage: number;
  started_at: string | null;
  completed_at: string | null;
  last_accessed_at: string;
  created_at: string;
  updated_at: string | null;
}

export interface ProgressListResponse {
  progress: Progress[];
  total: number;
}

export interface ProgressUpdate {
  status?: ProgressStatus;
  completion_percentage?: number;
}

