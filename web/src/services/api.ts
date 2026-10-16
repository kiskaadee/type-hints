import type {
  CheckRequest,
  CheckResponse,
  ExerciseCatalogResponse,
  ExerciseDetailResponse,
} from '../types/api'

const API_BASE = '/api/v1'

export class ApiError extends Error {
  status: number
  details?: unknown

  constructor(status: number, message: string, details?: unknown) {
    super(message)
    this.name = 'ApiError'
    this.status = status
    this.details = details
  }
}

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    let errorDetail = `Request failed with status ${response.status}`
    try {
      const data = await response.json()
      if (data && typeof data === 'object' && 'detail' in data) {
        errorDetail = typeof data.detail === 'string' ? data.detail : JSON.stringify(data.detail)
      }
    } catch {
      // Ignore JSON parse error on non-JSON response
    }
    throw new ApiError(response.status, errorDetail)
  }
  return response.json() as Promise<T>
}

export async function checkHealth(): Promise<{ status: string; service: string }> {
  const res = await fetch(`${API_BASE}/health`)
  return handleResponse<{ status: string; service: string }>(res)
}

export async function fetchCatalog(lang: string = 'en'): Promise<ExerciseCatalogResponse> {
  const res = await fetch(`${API_BASE}/exercises?lang=${encodeURIComponent(lang)}`)
  return handleResponse<ExerciseCatalogResponse>(res)
}

export async function fetchExercise(
  exerciseId: string,
  lang: string = 'en'
): Promise<ExerciseDetailResponse> {
  const res = await fetch(
    `${API_BASE}/exercises/${encodeURIComponent(exerciseId)}?lang=${encodeURIComponent(lang)}`
  )
  return handleResponse<ExerciseDetailResponse>(res)
}

export async function checkCode(
  exerciseId: string,
  code: string,
  lang: string = 'en'
): Promise<CheckResponse> {
  const payload: CheckRequest = {
    exercise_id: exerciseId,
    code,
  }

  const res = await fetch(`${API_BASE}/check?lang=${encodeURIComponent(lang)}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  })

  return handleResponse<CheckResponse>(res)
}
