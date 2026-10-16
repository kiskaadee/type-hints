import { useState, useEffect, useRef, useCallback } from 'react'
import { Header } from './components/Header'
import { GuidePane } from './components/GuidePane'
import { MonacoEditor } from './components/MonacoEditor'
import type { MonacoEditorHandle } from './components/MonacoEditor'
import { Terminal } from './components/Terminal'
import type { TerminalHandle } from './components/Terminal'
import { MobileMacroBar } from './components/MobileMacroBar'
import { CatalogModal } from './components/CatalogModal'
import { LoadingBar } from './components/LoadingBar'
import { SuccessCelebration } from './components/SuccessCelebration'
import { fetchCatalog, fetchExercise, checkCode } from './services/api'
import {
  getDraft,
  saveDraft,
  removeDraft,
  getLastExerciseId,
  setLastExerciseId,
  getLanguagePreference,
  setLanguagePreference,
} from './services/storage'
import type {
  ActiveMobileTab,
  CheckErrorItem,
  ExerciseCatalogResponse,
  ExerciseDetailResponse,
  UIState,
} from './types/api'

export function App() {
  // Navigation & Catalog state
  const [catalog, setCatalog] = useState<ExerciseCatalogResponse | null>(null)
  const [currentExercise, setCurrentExercise] = useState<ExerciseDetailResponse | null>(null)
  const [isCatalogOpen, setIsCatalogOpen] = useState(false)
  const [lang, setLang] = useState<string>(() => getLanguagePreference())

  // Editor & Code state
  const [code, setCode] = useState<string>('')
  const [errors, setErrors] = useState<CheckErrorItem[]>([])
  const [tabFocusMode, setTabFocusMode] = useState<boolean>(false)

  // Terminal & Execution state
  const [uiState, setUiState] = useState<UIState>('empty')
  const [logs, setLogs] = useState<string[]>([])
  const [executionTimeMs, setExecutionTimeMs] = useState<number | undefined>(undefined)
  const [streak, setStreak] = useState<number>(0)
  const [showCelebration, setShowCelebration] = useState(false)

  // Mobile layout state
  const [activeMobileTab, setActiveMobileTab] = useState<ActiveMobileTab>('code')

  // Refs
  const editorRef = useRef<MonacoEditorHandle>(null)
  const terminalRef = useRef<TerminalHandle>(null)

  // Initialize terminal welcome log
  const pushWelcomeLog = useCallback((exerciseId: string, title: string) => {
    setLogs([
      `\x1b[33m════════════════════════════════════════════════════════════════════\x1b[0m\n` +
        `\x1b[1m\x1b[32m  REVEX INTERACTIVE TYPE-HINT LABORATORY // v0.1.0\x1b[0m\n` +
        `  Python 3.13 Standard Library + PEP 695 Static Verification\n` +
        `\x1b[33m════════════════════════════════════════════════════════════════════\x1b[0m\n` +
        `Loaded module: \x1b[33m${exerciseId}\x1b[0m - \x1b[37m${title}\x1b[0m\n` +
        `Ready for static inspection. Run \x1b[32mrevex check\x1b[0m or press \x1b[33m⌘+Enter\x1b[0m.`,
    ])
  }, [])

  // Load an exercise by ID
  const loadExercise = useCallback(
    async (id: string, currentLang: string = lang) => {
      setUiState('loading')
      setErrors([])
      try {
        const detail = await fetchExercise(id, currentLang)
        setCurrentExercise(detail)
        setLastExerciseId(id)

        // Restore saved draft from localStorage or fallback to starter_code
        const savedDraft = getDraft(id)
        const initialCode = savedDraft !== null ? savedDraft : detail.starter_code
        setCode(initialCode)

        setUiState('empty')
        pushWelcomeLog(detail.id, detail.title)
      } catch (err) {
        console.error('Failed to load exercise:', err)
        setUiState('error')
        setLogs((prev) => [
          ...prev,
          `\x1b[31mError loading exercise ${id}:\x1b[0m ${err instanceof Error ? err.message : String(err)}`,
        ])
      }
    },
    [lang, pushWelcomeLog]
  )

  // Initial mount: load catalog and default exercise
  useEffect(() => {
    let isMounted = true
    async function init() {
      try {
        const cat = await fetchCatalog(lang)
        if (!isMounted) return
        setCatalog(cat)
        setStreak(cat.current_streak)

        const lastId = getLastExerciseId()
        const initialId =
          lastId && cat.exercises.some((e) => e.id === lastId)
            ? lastId
            : cat.exercises[0]?.id || '0101'

        await loadExercise(initialId, lang)
      } catch (err) {
        console.error('Failed to load catalog:', err)
        if (isMounted) {
          setUiState('error')
          setLogs([
            `\x1b[31m[CONNECTION ERROR]\x1b[0m Could not connect to revex-server at http://localhost:8000/api/v1`,
            `Ensure \x1b[33mrevex-server\x1b[0m is running: \x1b[32muv run revex server\x1b[0m`,
          ])
        }
      }
    }

    init()
    return () => {
      isMounted = false
    }
  }, [lang, loadExercise])

  // Handle code edits: update state and cache in localStorage
  const handleCodeChange = (newCode: string) => {
    setCode(newCode)
    if (currentExercise) {
      saveDraft(currentExercise.id, newCode)
    }
  }

  // Handle Validation Check (Cmd+Enter or Run CTA)
  const handleRunCheck = async () => {
    if (!currentExercise || uiState === 'loading') return

    setUiState('loading')
    setLogs((prev) => [
      ...prev,
      `\x1b[38;5;244mguest@revex:~$\x1b[0m revex check workspace/${currentExercise.id}.py\n` +
        `\x1b[33m[..] Analyzing AST structure & type annotations...\x1b[0m\n` +
        `\x1b[33m[..] Invoking Pyright strict static type checker...\x1b[0m`,
    ])

    // On mobile, switch to terminal tab so learner sees results
    if (window.innerWidth < 1024) {
      setActiveMobileTab('terminal')
    }

    try {
      const response = await checkCode(currentExercise.id, code, lang)
      setExecutionTimeMs(response.execution_time_ms)
      setErrors(response.errors)

      // Append terminal output
      setLogs((prev) => [...prev, response.terminal_output])

      if (response.passed) {
        setUiState('success')
        setShowCelebration(true)
        setStreak((prev) => prev + 1)
        // Mark completed in local catalog state
        setCatalog((prev) => {
          if (!prev) return null
          return {
            ...prev,
            total_solved: prev.total_solved + 1,
            exercises: prev.exercises.map((e) =>
              e.id === currentExercise.id ? { ...e, status: 'completed' } : e
            ),
          }
        })
      } else {
        // Evaluate if partial state (AST passed, but Pyright failed)
        const hasAstError = response.errors.some((e) => e.error_code.startsWith('AST'))
        if (!hasAstError && response.errors.length > 0) {
          setUiState('partial')
        } else {
          setUiState('error')
        }
      }
    } catch (err) {
      console.error('Validation request failed:', err)
      setUiState('error')
      setLogs((prev) => [
        ...prev,
        `\x1b[31m[ERROR]\x1b[0m Request failed: ${err instanceof Error ? err.message : String(err)}`,
        `Your code has been safely preserved locally in localStorage.`,
      ])
    }
  }

  // Reset exercise to canonical starter code
  const handleReset = () => {
    if (!currentExercise) return
    const confirmed = window.confirm(
      'Reset this exercise to the original starter template? Any unsaved edits will be discarded.'
    )
    if (!confirmed) return

    removeDraft(currentExercise.id)
    setCode(currentExercise.starter_code)
    setErrors([])
    setUiState('empty')
    setLogs((prev) => [
      ...prev,
      `\x1b[33m[RESTORE]\x1b[0m Code restored to starter template for ${currentExercise.id}.`,
    ])
  }

  // Progressive Hint handler
  const handleHint = () => {
    if (!currentExercise || currentExercise.hints.length === 0) {
      setLogs((prev) => [...prev, `\x1b[33m[HINT]\x1b[0m No hints available for this module.`])
      return
    }
    const randomHint =
      currentExercise.hints[Math.floor(Math.random() * currentExercise.hints.length)]
    setLogs((prev) => [
      ...prev,
      `\x1b[33m[HINT]\x1b[0m ${randomHint}`,
    ])
  }

  // Navigation: Next / Prev exercise
  const handleNext = () => {
    if (currentExercise?.next_exercise_id) {
      loadExercise(currentExercise.next_exercise_id)
      setShowCelebration(false)
      if (window.innerWidth < 1024) {
        setActiveMobileTab('code')
      }
    }
  }

  const handlePrev = () => {
    if (currentExercise?.prev_exercise_id) {
      loadExercise(currentExercise.prev_exercise_id)
      setShowCelebration(false)
      if (window.innerWidth < 1024) {
        setActiveMobileTab('code')
      }
    }
  }

  // Language Toggle
  const handleToggleLang = () => {
    const nextLang = lang === 'en' ? 'es' : 'en'
    setLang(nextLang)
    setLanguagePreference(nextLang)
    if (currentExercise) {
      loadExercise(currentExercise.id, nextLang)
    }
  }

  // Macro bar insertion
  const handleMacroInsert = (text: string, cursorOffset?: number) => {
    editorRef.current?.insertText(text, cursorOffset)
  }

  // Global Keyboard Shortcuts
  useEffect(() => {
    const handleGlobalKeyDown = (e: KeyboardEvent) => {
      // Ctrl+M: Toggle Tab Moves Focus mode
      if (e.ctrlKey && e.key.toLowerCase() === 'm') {
        e.preventDefault()
        setTabFocusMode((prev) => !prev)
        return
      }

      // Cmd+Option+R: Reset exercise
      if ((e.metaKey || e.ctrlKey) && e.altKey && e.key.toLowerCase() === 'r') {
        e.preventDefault()
        handleReset()
        return
      }

      // Enter when celebration active -> Next exercise
      if (showCelebration && e.key === 'Enter') {
        e.preventDefault()
        handleNext()
        return
      }
    }

    window.addEventListener('keydown', handleGlobalKeyDown)
    return () => window.removeEventListener('keydown', handleGlobalKeyDown)
  })

  return (
    <div className="h-screen w-screen flex flex-col bg-[#0d1117] text-[#c9d1d9] overflow-hidden select-none">
      {/* Top Phosphor Pulsing Loading Line */}
      <LoadingBar isLoading={uiState === 'loading'} />

      {/* Main Navigation Header */}
      <Header
        currentExercise={currentExercise}
        uiState={uiState}
        streak={streak}
        totalSolved={catalog?.total_solved || 0}
        totalExercises={catalog?.total_exercises || 0}
        lang={lang}
        tabFocusMode={tabFocusMode}
        activeMobileTab={activeMobileTab}
        onSelectMobileTab={setActiveMobileTab}
        onToggleTabFocusMode={() => setTabFocusMode((p) => !p)}
        onToggleLang={handleToggleLang}
        onOpenCatalog={() => setIsCatalogOpen(true)}
        onPrev={handlePrev}
        onNext={handleNext}
        onRunCheck={handleRunCheck}
        onReset={handleReset}
      />

      {/* Split Workspace View */}
      <main className="flex-1 w-full min-h-0 flex overflow-hidden relative">
        {/* Desktop Split View: 3 columns */}
        {/* Left Column: Problem Specification Guide (Hidden on mobile unless 'spec' tab) */}
        <section
          aria-label="Problem Specification"
          className={`h-full border-r border-white/10 lg:w-[28%] xl:w-[25%] lg:flex flex-col shrink-0 ${
            activeMobileTab === 'spec' ? 'flex w-full' : 'hidden'
          }`}
        >
          <GuidePane
            exercise={currentExercise}
            isPassed={uiState === 'success' || currentExercise?.completed === true}
          />
        </section>

        {/* Center Column: Monaco Editor (Hidden on mobile unless 'code' tab) */}
        <section
          aria-label="Code Editor"
          className={`h-full lg:flex-1 lg:flex flex-col min-w-0 ${
            activeMobileTab === 'code' ? 'flex w-full' : 'hidden'
          }`}
        >
          <MonacoEditor
            ref={editorRef}
            code={code}
            onChange={handleCodeChange}
            errors={errors}
            tabFocusMode={tabFocusMode}
            onRunCheck={handleRunCheck}
            onReset={handleReset}
          />
        </section>

        {/* Right Column: Sunken CRT Terminal (Hidden on mobile unless 'terminal' tab) */}
        <section
          aria-label="Interactive Terminal Output"
          className={`h-full lg:w-[32%] xl:w-[30%] lg:flex flex-col shrink-0 ${
            activeMobileTab === 'terminal' ? 'flex w-full' : 'hidden'
          }`}
        >
          <Terminal
            ref={terminalRef}
            logs={logs}
            uiState={uiState}
            executionTimeMs={executionTimeMs}
            onRunCheck={handleRunCheck}
            onHint={handleHint}
            onReset={handleReset}
            onNext={handleNext}
            onPrev={handlePrev}
            onClear={() => setLogs([])}
          />
        </section>
      </main>

      {/* Mobile Accessory Strip: Docked Macro Bar */}
      <div className="lg:hidden shrink-0">
        <MobileMacroBar onInsert={handleMacroInsert} />
      </div>

      {/* Sequence Catalog Modal */}
      <CatalogModal
        isOpen={isCatalogOpen}
        exercises={catalog?.exercises || []}
        currentExerciseId={currentExercise?.id || null}
        onSelect={(id) => loadExercise(id)}
        onClose={() => setIsCatalogOpen(false)}
      />

      {/* Confetti & Success Toast */}
      <SuccessCelebration
        show={showCelebration}
        nextExerciseId={currentExercise?.next_exercise_id || null}
        onAdvance={handleNext}
        onDismiss={() => setShowCelebration(false)}
      />
    </div>
  )
}

export default App
