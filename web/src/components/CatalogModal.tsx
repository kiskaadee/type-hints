import React, { useState, useMemo } from 'react'
import { X, Search, CheckCircle2, CircleDot, Circle, BookOpen } from 'lucide-react'
import type { ExerciseListItem } from '../types/api'

interface CatalogModalProps {
  isOpen: boolean
  exercises: ExerciseListItem[]
  currentExerciseId: string | null
  onSelect: (exerciseId: string) => void
  onClose: () => void
}

export const CatalogModal: React.FC<CatalogModalProps> = ({
  isOpen,
  exercises,
  currentExerciseId,
  onSelect,
  onClose,
}) => {
  const [query, setQuery] = useState('')

  // Group exercises by group_title or group
  const filteredExercises = useMemo(() => {
    if (!query.trim()) return exercises
    const q = query.toLowerCase()
    return exercises.filter(
      (ex) =>
        ex.id.toLowerCase().includes(q) ||
        ex.title.toLowerCase().includes(q) ||
        ex.group.toLowerCase().includes(q) ||
        ex.group_title.toLowerCase().includes(q)
    )
  }, [exercises, query])

  const grouped = useMemo(() => {
    const map = new Map<string, ExerciseListItem[]>()
    for (const ex of filteredExercises) {
      const gTitle = ex.group_title || ex.group
      if (!map.has(gTitle)) {
        map.set(gTitle, [])
      }
      map.get(gTitle)!.push(ex)
    }
    return Array.from(map.entries())
  }, [filteredExercises])

  if (!isOpen) return null

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="catalog-title"
      className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-6 bg-black/75 backdrop-blur-xs animate-in fade-in duration-150"
      onClick={onClose}
    >
      <div
        className="w-full max-w-2xl max-h-[85vh] bg-[#161926] border border-white/15 rounded-lg shadow-2xl flex flex-col overflow-hidden text-left"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="p-4 border-b border-white/10 flex items-center justify-between gap-3 bg-[#12141f]">
          <div className="flex items-center gap-2">
            <BookOpen className="w-5 h-5 text-[#ffb000]" />
            <h2 id="catalog-title" className="text-sm font-bold uppercase tracking-wider text-white">
              Course Sequence Catalog
            </h2>
            <span className="text-xs font-mono text-[#8b949e]">
              ({exercises.length} modules)
            </span>
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded text-[#8b949e] hover:text-white hover:bg-white/5 transition"
            aria-label="Close dialog"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Filter input */}
        <div className="p-3 border-b border-white/10 bg-[#0d1117] flex items-center gap-2">
          <Search className="w-4 h-4 text-[#8b949e] shrink-0" />
          <input
            type="text"
            placeholder="Search exercises by title, group or code (e.g. 0501, Generics, PEP 695)..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            autoFocus
            className="w-full bg-transparent text-sm text-white placeholder-[#8b949e] focus:outline-hidden font-mono"
          />
          {query && (
            <button
              onClick={() => setQuery('')}
              className="text-xs font-mono text-[#8b949e] hover:text-white"
            >
              Clear
            </button>
          )}
        </div>

        {/* Catalog List */}
        <div className="p-4 overflow-y-auto space-y-6 flex-1 divide-y divide-white/5">
          {grouped.length === 0 ? (
            <div className="py-12 text-center text-[#8b949e] font-mono text-xs">
              No exercises match &quot;{query}&quot;
            </div>
          ) : (
            grouped.map(([groupTitle, items]) => (
              <div key={groupTitle} className="pt-4 first:pt-0">
                <div className="text-xs font-mono uppercase tracking-wider text-[#8b949e] mb-2 flex items-center justify-between">
                  <span>{groupTitle}</span>
                  <span className="text-[10px] text-white/40">{items.length} items</span>
                </div>
                <div className="grid grid-cols-1 gap-1.5">
                  {items.map((ex) => {
                    const isCurrent = ex.id === currentExerciseId
                    const isCompleted = ex.status === 'completed'
                    const isInProgress = ex.status === 'in_progress'

                    return (
                      <button
                        key={ex.id}
                        onClick={() => {
                          onSelect(ex.id)
                          onClose()
                        }}
                        className={`w-full p-2.5 rounded flex items-center justify-between gap-3 text-left transition border group ${
                          isCurrent
                            ? 'bg-[#ffb000]/10 border-[#ffb000]/50 text-white'
                            : 'bg-[#0d1117]/60 hover:bg-[#0d1117] border-white/5 hover:border-white/20 text-[#c9d1d9]'
                        }`}
                      >
                        <div className="flex items-center gap-3 min-w-0">
                          {/* Status Icon */}
                          <div className="shrink-0">
                            {isCompleted ? (
                              <CheckCircle2 className="w-4 h-4 text-[#10b981]" />
                            ) : isInProgress ? (
                              <CircleDot className="w-4 h-4 text-[#ffb000]" />
                            ) : (
                              <Circle className="w-4 h-4 text-white/20 group-hover:text-white/40" />
                            )}
                          </div>

                          {/* Exercise ID & Title */}
                          <div className="min-w-0">
                            <div className="flex items-center gap-2">
                              <span
                                className={`text-xs font-mono font-bold ${
                                  isCurrent ? 'text-[#ffb000]' : 'text-[#8b949e]'
                                }`}
                              >
                                {ex.id}
                              </span>
                              <span className="text-sm font-medium truncate">{ex.title}</span>
                            </div>
                          </div>
                        </div>

                        {/* Difficulty Badge */}
                        <div className="shrink-0 flex items-center gap-2">
                          <span className="text-[10px] uppercase font-mono px-1.5 py-0.5 rounded bg-white/5 border border-white/10 text-[#8b949e]">
                            {ex.difficulty}
                          </span>
                          {isCurrent && (
                            <span className="text-[10px] font-mono font-bold text-[#ffb000] px-1.5 py-0.5 rounded bg-[#ffb000]/20">
                              CURRENT
                            </span>
                          )}
                        </div>
                      </button>
                    )
                  })}
                </div>
              </div>
            ))
          )}
        </div>

        {/* Footer info */}
        <div className="p-3 bg-[#12141f] border-t border-white/10 text-xs font-mono text-[#8b949e] flex items-center justify-between">
          <span>Esc to close</span>
          <span className="text-[11px] text-white/50">Strict AST + Pyright Verification</span>
        </div>
      </div>
    </div>
  )
}
