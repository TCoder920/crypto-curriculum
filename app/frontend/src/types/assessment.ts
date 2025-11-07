/** Assessment types */
export enum QuestionType {
  MULTIPLE_CHOICE = 'multiple_choice',
  TRUE_FALSE = 'true_false',
  SHORT_ANSWER = 'short_answer',
  CODING_TASK = 'coding_task',
}

export enum ReviewStatus {
  PENDING = 'pending',
  GRADED = 'graded',
  NEEDS_REVIEW = 'needs_review',
}

export interface Assessment {
  id: number;
  module_id: number;
  question_text: string;
  question_type: QuestionType;
  order_index: number;
  points: number;
  options?: Record<string, string>; // For multiple choice: { "A": "...", "B": "..." }
  explanation?: string;
}

export interface AssessmentListResponse {
  module_id: number;
  module_title: string;
  assessments: Assessment[];
  total_points: number;
  estimated_time_minutes: number;
}

export interface AssessmentSubmit {
  user_answer: string;
  time_spent_seconds?: number;
}

export interface AssessmentSubmitResponse {
  attempt_id: number;
  is_correct: boolean | null;
  points_earned: number | null;
  review_status: ReviewStatus;
  explanation?: string;
  correct_answer?: string;
}

export interface QuizAttempt {
  attempt_id: number;
  assessment_id: number;
  question_text: string;
  question_type: QuestionType;
  user_answer: string | null;
  is_correct: boolean | null;
  points_earned: number | null;
  review_status: ReviewStatus;
  feedback?: string;
  attempted_at: string;
}

export interface ModuleResultsResponse {
  module_id: number;
  module_title: string;
  total_questions: number;
  attempted: number;
  correct: number;
  pending_review: number;
  score_percent: number;
  points_earned: number;
  points_possible: number;
  attempts: QuizAttempt[];
  can_progress: boolean;
  best_score_percent: number | null;
  attempt_count: number;
}

