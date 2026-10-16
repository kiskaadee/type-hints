import React from 'react'
import {
  Flame,
  ChevronLeft,
  ChevronRight,
  ListFilter,
  Play,
  RotateCcw,
  Sparkles,
  Keyboard,
  Globe,
  Loader2,
} from 'lucide-react'
import type { ActiveMobileTab, ExerciseDetailResponse, UIState } from '../types/api'

interface HeaderProps {
  currentExercise: ExerciseDetailResponse | null
  uiState: UIState
  streak: number
  totalSolved: number
  totalExercises: number
  lang: string
  tabFocusMode: boolean
  activeMobileTab: ActiveMobileTab
  onSelectMobileTab: (tab: ActiveMobileTab) => void
  onToggleTabFocusMode: () => void
  onToggleLang: () => void
  onOpenCatalog: () => void
  onPrev: () => void
  onNext: () => void
  onRunCheck: () => void
  onReset: () => void
}

export const Header: React.FC<HeaderProps> = ({
  currentExercise,
  uiState,
  streak,
  totalSolved,
  totalExercises,
  lang,
  tabFocusMode,
  activeMobileTab,
  onSelectMobileTab,
  onToggleTabFocusMode,
  onToggleLang,
  onOpenCatalog,
  onPrev,
  onNext,
  onRunCheck,
  onReset,
}) => {
  const isPassing = uiState === 'success'
  const isLoading = uiState === 'loading'

  return (
    <header className="h-14 border-b border-white/10 bg-[#161926] px-3 sm:px-4 flex items-center justify-between gap-2 shrink-0 select-none z-20">
      {/* Brand & Exercise Sequence Picker */}
      <div className="flex items-center gap-2 sm:gap-3 min-w-0">
        <div className="flex items-center gap-1.5 text-xs font-mono font-bold tracking-wider text-[#ffb000] px-2 py-1 rounded bg-[#ffb000]/10 border border-[#ffb000]/25 shrink-0">
          <span className="amber-glow">REVEX</span>
          <span className="text-[#8b949e] hidden sm:inline">// 3.13</span>
        </div>

        {/* Exercise Switcher Trigger */}
        <button
          onClick={onOpenCatalog}
          className="flex items-center gap-2 px-2.5 py-1 rounded bg-[#0d1117] hover:bg-[#1a1f2c] border border-white/10 hover:border-[#ffb000]/40 transition text-left group min-w-0"
          title="Open Exercise Sequence Catalog (Space/Click)"
          aria-label="Open Course Catalog"
        >
          <ListFilter className="w-3.5 h-3.5 text-[#ffb000] shrink-0 group-hover:scale-110 transition-transform" />
          <div className="min-w-0 flex items-center gap-1.5 text-xs">
            <span className="font-mono text-[#ffb000] font-semibold shrink-0">
              {currentExercise ? currentExercise.id : '----'}
            </span>
            <span className="text-white/40 hidden md:inline">•</span>
            <span className="font-medium text-[#c9d1d9] truncate max-w-[120px] sm:max-w-[200px] lg:max-w-[300px]">
              {currentExercise ? currentExercise.title : 'Loading exercise...'}
            </span>
          </div>
        </button>

        {/* Prev / Next Exercise quick navigation */}
        <div className="hidden sm:flex items-center gap-0.5 border border-white/10 rounded bg-[#0d1117] p-0.5">
          <button
            onClick={onPrev}
            disabled={!currentExercise?.prev_exercise_id || isLoading}
            className="p-1 rounded text-[#8b949e] hover:text-white hover:bg-white/5 disabled:opacity-30 disabled:hover:bg-transparent transition"
            title="Previous Exercise"
            aria-label="Previous Exercise"
          >
            <ChevronLeft className="w-4 h-4" />
          </button>
          <button
            onClick={onNext}
            disabled={!currentExercise?.next_exercise_id || isLoading}
            className="p-1 rounded text-[#8b949e] hover:text-white hover:bg-white/5 disabled:opacity-30 disabled:hover:bg-transparent transition"
            title="Next Exercise"
            aria-label="Next Exercise"
          >
            <ChevronRight className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Center Mobile Tab Switcher (Visible only below lg) */}
      <div className="flex lg:hidden items-center bg-[#0d1117] p-0.5 rounded border border-white/10 text-xs font-mono">
        <button
          onClick={() => onSelectMobileTab('spec')}
          className={`px-2.5 py-1 rounded transition ${
            activeMobileTab === 'spec'
              ? 'bg-[#161926] text-[#ffb000] font-bold border border-[#ffb000]/30'
              : 'text-[#8b949e] hover:text-white'
          }`}
        >
          [Spec]
        </button>
        <button
          onClick={() => onSelectMobileTab('code')}
          className={`px-2.5 py-1 rounded transition ${
            activeMobileTab === 'code'
              ? 'bg-[#161926] text-[#79c0ff] font-bold border border-[#79c0ff]/30'
              : 'text-[#8b949e] hover:text-white'
          }`}
        >
          [Code]
        </button>
        <button
          onClick={() => onSelectMobileTab('terminal')}
          className={`px-2.5 py-1 rounded transition relative ${
            activeMobileTab === 'terminal'
              ? 'bg-[#161926] text-[#10b981] font-bold border border-[#10b981]/30'
              : 'text-[#8b949e] hover:text-white'
          }`}
        >
          [Term]
          {uiState === 'error' && (
            <span className="absolute top-1 right-1 w-1.5 h-1.5 rounded-full bg-[#ef4444] animate-ping" />
          )}
        </button>
      </div>

      {/* Right Controls: Streak, Accessibility, Lang, Run CTA */}
      <div className="flex items-center gap-2 sm:gap-3 shrink-0">
        {/* Streak Counter */}
        <div
          className={`flex items-center gap-1.5 px-2 py-1 rounded text-xs font-mono font-medium transition ${
            streak > 0
              ? 'bg-[#ffb000]/10 text-[#ffb000] border border-[#ffb000]/25'
              : 'bg-white/5 text-[#8b949e] border border-white/10'
          }`}
          title={`Active Streak: ${streak} | Solved: ${totalSolved}/${totalExercises}`}
        >
          <Flame
            className={`w-3.5 h-3.5 ${
              streak > 0 ? 'text-[#ffb000] fill-[#ffb000]/30 animate-pulse' : 'text-[#8b949e]'
            }`}
          />
          <span className="tabular-nums font-bold">{streak}</span>
          <span className="hidden xl:inline text-white/40">
            ({totalSolved}/{totalExercises})
          </span>
        </div>

        {/* Tab-Moves-Focus Toggle (Ctrl+M - WCAG Accessibility) */}
        <button
          onClick={onToggleTabFocusMode}
          className={`hidden md:flex items-center gap-1 px-2 py-1 rounded text-xs font-mono transition border ${
            tabFocusMode
              ? 'bg-[#ffb000]/15 text-[#ffb000] border-[#ffb000]/40'
              : 'bg-[#0d1117] text-[#8b949e] border-white/10 hover:text-white'
          }`}
          title="Toggle Monaco Tab Moves Focus (Ctrl+M - Accessibility)"
          aria-label="Toggle Tab trap in code editor"
        >
          <Keyboard className="w-3.5 h-3.5" />
          <span className="text-[10px] uppercase">{tabFocusMode ? 'Tab Focus' : 'Tab Indent'}</span>
        </button>

        {/* Language Switcher */}
        <button
          onClick={onToggleLang}
          className="flex items-center gap-1 px-2 py-1 rounded text-xs font-mono text-[#8b949e] hover:text-white bg-[#0d1117] hover:bg-[#1a1f2c] border border-white/10 transition"
          title={`Switch Language (Current: ${lang.toUpperCase()})`}
          aria-label="Switch Language"
        >
          <Globe className="w-3.5 h-3.5 text-[#ffb000]" />
          <span className="font-bold uppercase text-[11px]">{lang}</span>
        </button>

        {/* Reset Template Button */}
        <button
          onClick={onReset}
          disabled={isLoading}
          className="p-1.5 rounded text-[#8b949e] hover:text-white hover:bg-white/5 border border-white/10 hover:border-white/20 transition disabled:opacity-40"
          title="Reset Code to Template (Cmd+Option+R)"
          aria-label="Reset exercise code"
        >
          <RotateCcw className="w-3.5 h-3.5" />
        </button>

        {/* Main CTA: Run Check or Advance */}
        {isPassing && currentExercise?.next_exercise_id ? (
          <button
            onClick={onNext}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded bg-[#10b981] hover:bg-[#059669] text-black font-semibold text-xs tracking-wide shadow-lg shadow-[#10b981]/25 hover:shadow-[#10b981]/40 transition-all font-mono active:scale-95"
            title="Advance to next exercise (Enter)"
          >
            <Sparkles className="w-3.5 h-3.5" />
            <span>Next Exercise ➔</span>
          </button>
        ) : (
          <button
            onClick={onRunCheck}
            disabled={isLoading}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded text-xs font-semibold tracking-wide font-mono transition-all active:scale-95 border ${
              isLoading
                ? 'bg-[#1e2330] text-[#8b949e] border-white/10 cursor-wait'
                : 'bg-[#ffb000] hover:bg-[#e59e00] text-black border-[#ffb000] shadow-md shadow-[#ffb000]/20 hover:shadow-[#ffb000]/30'
            }`}
            title="Run AST & Pyright Validation (Cmd+Enter)"
          >
            {isLoading ? (
              <>
                <Loader2 className="w-3.5 h-3.5 animate-spin text-[#ffb000]" />
                <span className="hidden sm:inline">Checking...</span>
              </>
            ) : (
              <>
                <Play className="w-3.5 h-3.5 fill-current" />
                <span className="hidden sm:inline">Run Check</span>
                <span className="sm:hidden">Run</span>
                <kbd className="hidden lg:inline-block ml-1 text-[10px] opacity-75 font-normal px-1 rounded bg-black/20">
                  ⌘↵
                </kbd>
              </>
            )}
          </button>
        )}
      </div>
    </header>
  )
}
