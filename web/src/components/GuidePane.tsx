import React, { useMemo, useState } from 'react'
import { marked } from 'marked'
import { Lightbulb, ChevronDown, ChevronRight, FileText, CheckCircle2 } from 'lucide-react'
import type { ExerciseDetailResponse } from '../types/api'

interface GuidePaneProps {
  exercise: ExerciseDetailResponse | null
  isPassed: boolean
}

export const GuidePane: React.FC<GuidePaneProps> = ({ exercise, isPassed }) => {
  const [revealedHints, setRevealedHints] = useState<number>(0)
  const [hintsExpanded, setHintsExpanded] = useState<boolean>(true)

  const problemMarkdown = exercise?.problem_markdown || ''

  // Configure marked for safe, clean HTML rendering
  const renderedHtml = useMemo(() => {
    if (!problemMarkdown) return ''
    try {
      return marked.parse(problemMarkdown, {
        breaks: true,
        gfm: true,
      }) as string
    } catch (e) {
      console.error('Failed to parse markdown', e)
      return problemMarkdown
    }
  }, [problemMarkdown])

  const hints = exercise?.hints || []

  const handleRevealNextHint = () => {
    if (revealedHints < hints.length) {
      setRevealedHints((prev) => prev + 1)
    }
  }

  return (
    <aside className="h-full flex flex-col bg-[#161926] border-r border-white/10 overflow-hidden text-left">
      {/* Pane Title Bar */}
      <div className="h-9 px-3.5 border-b border-white/10 bg-[#12141f] flex items-center justify-between shrink-0">
        <div className="flex items-center gap-2 text-xs font-mono font-medium text-[#8b949e]">
          <FileText className="w-3.5 h-3.5 text-[#ffb000]" />
          <span className="uppercase tracking-wider">Problem Specification</span>
        </div>
        {isPassed && (
          <div className="flex items-center gap-1 text-[11px] font-mono text-[#10b981] font-semibold">
            <CheckCircle2 className="w-3.5 h-3.5" />
            <span>SOLVED</span>
          </div>
        )}
      </div>

      {/* Main Content Area */}
      <div className="flex-1 overflow-y-auto p-4 sm:p-5 space-y-5">
        {exercise ? (
          <>
            {/* Exercise Header Meta */}
            <div className="border-b border-white/5 pb-3">
              <div className="flex items-center gap-2 mb-1">
                <span className="px-1.5 py-0.5 rounded bg-[#ffb000]/15 border border-[#ffb000]/30 text-[#ffb000] text-[10px] font-mono font-bold">
                  {exercise.id}
                </span>
                <span className="text-xs font-mono text-[#8b949e] uppercase">
                  {exercise.group}
                </span>
              </div>
              <h1 className="text-lg font-bold text-white tracking-tight">
                {exercise.title}
              </h1>
            </div>

            {/* Markdown rendered body */}
            <div
              className="prose prose-invert max-w-none text-sm text-[#c9d1d9] leading-relaxed
                [&>h1]:text-base [&>h1]:font-bold [&>h1]:text-white [&>h1]:mt-4 [&>h1]:mb-2 [&>h1]:border-b [&>h1]:border-white/10 [&>h1]:pb-1
                [&>h2]:text-sm [&>h2]:font-bold [&>h2]:text-white [&>h2]:mt-4 [&>h2]:mb-2
                [&>h3]:text-xs [&>h3]:font-bold [&>h3]:text-[#ffb000] [&>h3]:uppercase [&>h3]:tracking-wider [&>h3]:mt-3 [&>h3]:mb-1
                [&>p]:my-2.5
                [&>ul]:list-disc [&>ul]:pl-5 [&>ul]:my-2 [&>ul>li]:my-1
                [&>ol]:list-decimal [&>ol]:pl-5 [&>ol]:my-2 [&>ol>li]:my-1
                [&>code]:bg-[#0d1117] [&>code]:text-[#ffb000] [&>code]:px-1.5 [&>code]:py-0.5 [&>code]:rounded [&>code]:font-mono [&>code]:text-xs [&>code]:border [&>code]:border-white/10
                [&>pre]:bg-[#0d1117] [&>pre]:border [&>pre]:border-white/10 [&>pre]:p-3 [&>pre]:rounded-md [&>pre]:overflow-x-auto [&>pre]:my-3
                [&>pre>code]:bg-transparent [&>pre>code]:p-0 [&>pre>code]:border-0 [&>pre>code]:text-[#c9d1d9]
                [&>blockquote]:border-l-2 [&>blockquote]:border-[#ffb000]/60 [&>blockquote]:pl-3 [&>blockquote]:my-3 [&>blockquote]:italic [&>blockquote]:text-[#8b949e]
              "
              dangerouslySetInnerHTML={{ __html: renderedHtml }}
            />

            {/* Progressive Hints Section */}
            {hints.length > 0 && (
              <div className="mt-6 border border-white/10 rounded-md bg-[#0d1117] overflow-hidden">
                <button
                  onClick={() => setHintsExpanded(!hintsExpanded)}
                  className="w-full px-3.5 py-2.5 flex items-center justify-between text-xs font-mono font-medium text-[#c9d1d9] bg-[#12141f] hover:bg-[#1a1f2c] transition text-left"
                >
                  <div className="flex items-center gap-2">
                    <Lightbulb className="w-3.5 h-3.5 text-[#ffb000]" />
                    <span>HINTS ({revealedHints}/{hints.length} UNLOCKED)</span>
                  </div>
                  {hintsExpanded ? (
                    <ChevronDown className="w-4 h-4 text-[#8b949e]" />
                  ) : (
                    <ChevronRight className="w-4 h-4 text-[#8b949e]" />
                  )}
                </button>

                {hintsExpanded && (
                  <div className="p-3.5 space-y-3">
                    {revealedHints === 0 ? (
                      <p className="text-xs text-[#8b949e] italic font-mono">
                        Hints are hidden to encourage initial problem solving.
                      </p>
                    ) : (
                      hints.slice(0, revealedHints).map((hint, idx) => (
                        <div
                          key={idx}
                          className="p-2.5 rounded bg-[#161926] border border-white/5 text-xs text-[#c9d1d9] font-mono leading-relaxed"
                        >
                          <div className="text-[10px] text-[#ffb000] font-bold uppercase mb-1">
                            Hint #{idx + 1}
                          </div>
                          <div>{hint}</div>
                        </div>
                      ))
                    )}

                    {revealedHints < hints.length && (
                      <button
                        onClick={handleRevealNextHint}
                        className="w-full py-1.5 px-3 rounded bg-white/5 hover:bg-white/10 border border-white/10 text-xs font-mono text-[#ffb000] transition flex items-center justify-center gap-1.5"
                      >
                        <Lightbulb className="w-3 h-3" />
                        <span>Reveal Hint #{revealedHints + 1}</span>
                      </button>
                    )}
                  </div>
                )}
              </div>
            )}
          </>
        ) : (
          <div className="h-full flex items-center justify-center text-xs font-mono text-[#8b949e]">
            Select an exercise from the catalog...
          </div>
        )}
      </div>
    </aside>
  )
}
