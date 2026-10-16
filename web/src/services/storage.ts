const DRAFT_PREFIX = 'revex_draft_'
const LAST_EXERCISE_KEY = 'revex_last_exercise_id'
const LANG_KEY = 'revex_language'

export function getDraft(exerciseId: string): string | null {
  try {
    return localStorage.getItem(`${DRAFT_PREFIX}${exerciseId}`)
  } catch (e) {
    console.warn('Failed to read draft from localStorage', e)
    return null
  }
}

export function saveDraft(exerciseId: string, code: string): void {
  try {
    localStorage.setItem(`${DRAFT_PREFIX}${exerciseId}`, code)
  } catch (e) {
    console.warn('Failed to save draft to localStorage', e)
  }
}

export function removeDraft(exerciseId: string): void {
  try {
    localStorage.removeItem(`${DRAFT_PREFIX}${exerciseId}`)
  } catch (e) {
    console.warn('Failed to remove draft from localStorage', e)
  }
}

export function getLastExerciseId(): string | null {
  try {
    return localStorage.getItem(LAST_EXERCISE_KEY)
  } catch {
    return null
  }
}

export function setLastExerciseId(exerciseId: string): void {
  try {
    localStorage.setItem(LAST_EXERCISE_KEY, exerciseId)
  } catch {
    // ignore
  }
}

export function getLanguagePreference(): string {
  try {
    return localStorage.getItem(LANG_KEY) || 'en'
  } catch {
    return 'en'
  }
}

export function setLanguagePreference(lang: string): void {
  try {
    localStorage.setItem(LANG_KEY, lang)
  } catch {
    // ignore
  }
}
