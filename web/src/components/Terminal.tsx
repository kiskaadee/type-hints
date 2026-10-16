import React, { useState, useRef, useEffect, useImperativeHandle, forwardRef } from 'react'
import { Terminal as TermIcon, Trash2, CheckCircle2, XCircle, Clock, Tv } from 'lucide-react'
import { RenderAnsi } from '../services/ansi'
import type { UIState } from '../types/api'

export interface TerminalHandle {
  appendLog: (text: string) => void
  clear: () => void
  focus: () => void
}

interface TerminalProps {
  logs: string[]
  uiState: UIState
  executionTimeMs?: number
  onRunCheck: () => void
  onHint: () => void
  onReset: () => void
  onNext: () => void
  onPrev: () => void
  onClear: () => void
}

export const Terminal = forwardRef<TerminalHandle, TerminalProps>(
  (
    { logs, uiState, executionTimeMs, onRunCheck, onHint, onReset, onNext, onPrev, onClear },
    ref
  ) => {
    const [commandInput, setCommandInput] = useState('')
    const [history, setHistory] = useState<string[]>([])
    const [historyIdx, setHistoryIdx] = useState<number>(-1)
    const [scanlinesEnabled, setScanlinesEnabled] = useState(false)
    const [copiedNotice, setCopiedNotice] = useState<string | null>(null)
    const terminalEndRef = useRef<HTMLDivElement>(null)
    const inputRef = useRef<HTMLInputElement>(null)

    // Tmux-like copy on text selection
    const handleMouseUp = () => {
      const selection = window.getSelection()?.toString().trim()
      if (selection && selection.length > 0) {
        navigator.clipboard.writeText(selection).then(() => {
          setCopiedNotice(`COPIED (${selection.length})`)
          setTimeout(() => setCopiedNotice(null), 1500)
        }).catch(() => {})
      }
    }

    // Auto-scroll when logs change
    useEffect(() => {
      terminalEndRef.current?.scrollIntoView({ behavior: 'smooth' })
    }, [logs])

    useImperativeHandle(ref, () => ({
      appendLog: (_text: string) => {
        // Parent manages logs array
      },
      clear: () => {
        onClear()
      },
      focus: () => {
        inputRef.current?.focus()
      },
    }))

    const handleCommandSubmit = (e: React.FormEvent) => {
      e.preventDefault()
      const rawCmd = commandInput.trim()
      if (!rawCmd) return

      // Add to history
      setHistory((prev) => [...prev, rawCmd])
      setHistoryIdx(-1)
      setCommandInput('')

      const parts = rawCmd.split(/\s+/)
      const root = parts[0].toLowerCase()
      const sub = parts[1]?.toLowerCase()

      if (root === 'clear') {
        onClear()
        return
      }

      if (root === 'help') {
        // Emit help message
        logs.push(
          `\x1b[33mREVEX COMMAND MANUAL:\x1b[0m\n` +
            `  \x1b[32mrevex check\x1b[0m   Validate code against AST rules & Pyright\n` +
            `  \x1b[32mrevex hint\x1b[0m    Reveal progressive exercise hint\n` +
            `  \x1b[32mrevex reset\x1b[0m   Restore template starter code\n` +
            `  \x1b[32mrevex next\x1b[0m    Advance to next exercise\n` +
            `  \x1b[32mrevex prev\x1b[0m    Navigate to previous exercise\n` +
            `  \x1b[32mclear\x1b[0m         Clear the terminal output screen\n` +
            `  \x1b[32mhelp\x1b[0m          Show this interactive help prompt`
        )
        return
      }

      if (root === 'revex') {
        switch (sub) {
          case 'check':
            onRunCheck()
            break
          case 'hint':
            onHint()
            break
          case 'reset':
            onReset()
            break
          case 'next':
            onNext()
            break
          case 'prev':
            onPrev()
            break
          default:
            logs.push(`\x1b[31mUnknown revex subcommand:\x1b[0m '${sub}'. Type \x1b[33mhelp\x1b[0m for usage.`)
        }
        return
      }

      // Fallback
      logs.push(
        `\x1b[31mbash: command not found:\x1b[0m ${rawCmd}. Available: \x1b[33mrevex check\x1b[0m, \x1b[33mrevex hint\x1b[0m, \x1b[33mclear\x1b[0m, \x1b[33mhelp\x1b[0m`
      )
    }

    const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
      if (e.key === 'ArrowUp') {
        e.preventDefault()
        if (history.length === 0) return
        const nextIdx = historyIdx === -1 ? history.length - 1 : Math.max(0, historyIdx - 1)
        setHistoryIdx(nextIdx)
        setCommandInput(history[nextIdx] || '')
      } else if (e.key === 'ArrowDown') {
        e.preventDefault()
        if (historyIdx === -1) return
        const nextIdx = historyIdx + 1
        if (nextIdx >= history.length) {
          setHistoryIdx(-1)
          setCommandInput('')
        } else {
          setHistoryIdx(nextIdx)
          setCommandInput(history[nextIdx] || '')
        }
      }
    }

    // Determine 2-stage status from UI state
    const astPassed = uiState === 'success' || uiState === 'partial'
    const astFailed = uiState === 'error'
    const pyrightPassed = uiState === 'success'
    const pyrightFailed = uiState === 'error' || uiState === 'partial'

    return (
      <div className="h-full flex flex-col bg-[#0d1117] relative select-text border-l border-white/10 overflow-hidden font-mono">
        {/* Terminal Header Bar */}
        <div className="h-9 px-3.5 border-b border-white/10 bg-[#12141f] flex items-center justify-between shrink-0 select-none">
          <div className="flex items-center gap-2 text-xs text-[#8b949e]">
            <TermIcon className="w-3.5 h-3.5 text-[#ffb000]" />
            <span className="font-bold tracking-wider text-[#c9d1d9]">TERMINAL</span>
            <span className="text-[10px] text-white/40 hidden sm:inline">[guest@revex:~]</span>
          </div>

          {/* Two-Stage Checklist Pills */}
          <div className="flex items-center gap-2 text-[10px]">
            {/* AST status */}
            <div
              className={`flex items-center gap-1 px-1.5 py-0.5 rounded border transition ${
                astPassed
                  ? 'bg-[#10b981]/10 text-[#10b981] border-[#10b981]/30'
                  : astFailed
                  ? 'bg-[#ef4444]/10 text-[#ef4444] border-[#ef4444]/30'
                  : 'bg-white/5 text-[#8b949e] border-white/10'
              }`}
              title="Stage 1: AST Structural Type Hint Analysis"
            >
              {astPassed ? (
                <CheckCircle2 className="w-3 h-3" />
              ) : astFailed ? (
                <XCircle className="w-3 h-3" />
              ) : (
                <span className="w-1.5 h-1.5 rounded-full bg-[#8b949e]" />
              )}
              <span>AST</span>
            </div>

            {/* Pyright status */}
            <div
              className={`flex items-center gap-1 px-1.5 py-0.5 rounded border transition ${
                pyrightPassed
                  ? 'bg-[#10b981]/10 text-[#10b981] border-[#10b981]/30'
                  : pyrightFailed
                  ? 'bg-[#ef4444]/10 text-[#ef4444] border-[#ef4444]/30'
                  : 'bg-white/5 text-[#8b949e] border-white/10'
              }`}
              title="Stage 2: Pyright Strict Type Checker"
            >
              {pyrightPassed ? (
                <CheckCircle2 className="w-3 h-3" />
              ) : pyrightFailed ? (
                <XCircle className="w-3 h-3" />
              ) : (
                <span className="w-1.5 h-1.5 rounded-full bg-[#8b949e]" />
              )}
              <span>Pyright</span>
            </div>

            {executionTimeMs !== undefined && executionTimeMs > 0 && (
              <div className="hidden sm:flex items-center gap-1 text-[#8b949e] text-[10px]">
                <Clock className="w-3 h-3" />
                <span>{executionTimeMs.toFixed(0)}ms</span>
              </div>
            )}

            {copiedNotice && (
              <span className="px-1.5 py-0.5 rounded text-[9px] font-bold bg-[#10b981]/20 text-[#10b981] border border-[#10b981]/40 animate-pulse">
                {copiedNotice}
              </span>
            )}

            <button
              onClick={() => setScanlinesEnabled((prev) => !prev)}
              className={`p-1 rounded transition ${
                scanlinesEnabled
                  ? 'text-[#ffb000] bg-[#ffb000]/10 hover:bg-[#ffb000]/20'
                  : 'text-[#8b949e] hover:text-white hover:bg-white/5'
              }`}
              title={scanlinesEnabled ? 'CRT Scanlines: ON (Click to disable)' : 'CRT Scanlines: OFF (Click to enable)'}
              aria-label="Toggle CRT Scanlines"
            >
              <Tv className="w-3.5 h-3.5" />
            </button>

            <button
              onClick={onClear}
              className="p-1 rounded text-[#8b949e] hover:text-white hover:bg-white/5 transition"
              title="Clear terminal buffer"
              aria-label="Clear terminal output"
            >
              <Trash2 className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>

        {/* CRT Sunken Log Window with Optional Scanlines */}
        <div
          className={`flex-1 p-3.5 overflow-y-auto crt-sunken text-xs leading-relaxed space-y-2 relative ${
            scanlinesEnabled ? 'crt-scanlines' : ''
          }`}
          onMouseUp={handleMouseUp}
          onClick={() => inputRef.current?.focus()}
        >
          {logs.map((log, index) => (
            <div key={index} className="whitespace-pre-wrap break-words text-[#c9d1d9]">
              <RenderAnsi text={log} />
            </div>
          ))}

          {/* Interactive Prompt Line */}
          <form onSubmit={handleCommandSubmit} className="flex items-center gap-2 pt-2">
            <span className="text-[#10b981] font-bold shrink-0 select-none">guest@revex:~$</span>
            <input
              ref={inputRef}
              type="text"
              value={commandInput}
              onChange={(e) => setCommandInput(e.target.value)}
              onKeyDown={handleKeyDown}
              className="flex-1 bg-transparent text-[#ffb000] focus:outline-hidden font-mono text-xs caret-[#ffb000]"
              spellCheck={false}
              autoComplete="off"
            />
          </form>

          <div ref={terminalEndRef} />
        </div>
      </div>
    )
  }
)

Terminal.displayName = 'Terminal'
