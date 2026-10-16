import React, { useEffect } from 'react'
import confetti from 'canvas-confetti'
import { Sparkles, ArrowRight } from 'lucide-react'

interface SuccessCelebrationProps {
  show: boolean
  nextExerciseId: string | null
  onAdvance: () => void
  onDismiss: () => void
}

export const SuccessCelebration: React.FC<SuccessCelebrationProps> = ({
  show,
  nextExerciseId,
  onAdvance,
  onDismiss,
}) => {
  useEffect(() => {
    if (show) {
      // Fire confetti burst
      try {
        confetti({
          particleCount: 50,
          spread: 60,
          origin: { y: 0.7 },
          colors: ['#10b981', '#ffb000', '#58a6ff', '#ffffff'],
        })
      } catch (e) {
        console.warn('Confetti effect failed', e)
      }
    }
  }, [show])

  if (!show) return null

  return (
    <div className="fixed bottom-16 right-4 sm:right-8 z-40 animate-in slide-in-from-bottom-4 duration-200">
      <div className="p-3 sm:p-4 rounded-lg bg-[#161926] border border-[#10b981]/50 shadow-2xl mint-glow flex items-center gap-3">
        <div className="p-2 rounded-full bg-[#10b981]/15 text-[#10b981]">
          <Sparkles className="w-5 h-5" />
        </div>
        <div>
          <div className="text-xs font-mono font-bold text-[#10b981] uppercase tracking-wider">
            All Checks Passed!
          </div>
          <div className="text-[11px] text-[#c9d1d9] font-mono">
            AST verified & Pyright strict validated.
          </div>
        </div>

        {nextExerciseId && (
          <button
            onClick={() => {
              onDismiss()
              onAdvance()
            }}
            className="ml-2 px-3 py-1.5 rounded bg-[#10b981] hover:bg-[#059669] text-black font-mono font-bold text-xs flex items-center gap-1.5 transition active:scale-95 shadow-md"
          >
            <span>Next</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </button>
        )}
      </div>
    </div>
  )
}
