export type ExerciseStatus = 'not_started' | 'in_progress' | 'completed'

export interface ExerciseListItem {
  id: string
  slug: string
  group: string
  group_title: string
  order: number
  title: string
  difficulty: string
  status: ExerciseStatus
}

export interface ExerciseCatalogResponse {
  exercises: ExerciseListItem[]
  current_streak: number
  total_solved: number
  total_exercises: number
}

export interface ExerciseDetailResponse {
  id: string
  title: string
  group: string
  problem_markdown: string
  starter_code: string
  saved_code: string | null
  hints: string[]
  prev_exercise_id: string | null
  next_exercise_id: string | null
  completed: boolean
}

export interface CheckRequest {
  exercise_id: string
  code: string
}

export interface CheckErrorItem {
  start_line: number | null
  start_column: number | null
  end_line: number | null
  end_column: number | null
  message: string
  error_code: string
  severity: 'error' | 'warning'
}

export interface CheckResponse {
  passed: boolean
  execution_time_ms: number
  terminal_output: string
  errors: CheckErrorItem[]
  next_exercise_id: string | null
  stats: Record<string, number> | null
}

export type UIState = 'empty' | 'loading' | 'error' | 'partial' | 'success'

export type ActiveMobileTab = 'spec' | 'code' | 'terminal'
