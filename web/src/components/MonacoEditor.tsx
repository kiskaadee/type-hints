import { useEffect, useRef, useImperativeHandle, forwardRef } from 'react'
import Editor from '@monaco-editor/react'
import type { Monaco, OnMount } from '@monaco-editor/react'
import type { editor } from 'monaco-editor'
import type { CheckErrorItem } from '../types/api'

export interface MonacoEditorHandle {
  insertText: (text: string, cursorOffsetFromEnd?: number) => void
  focus: () => void
  formatCode: () => void
}

interface MonacoEditorProps {
  code: string
  onChange: (value: string) => void
  errors: CheckErrorItem[]
  tabFocusMode: boolean
  onRunCheck: () => void
  onReset: () => void
}

export const MonacoEditor = forwardRef<MonacoEditorHandle, MonacoEditorProps>(
  ({ code, onChange, errors, tabFocusMode, onRunCheck, onReset }, ref) => {
    const editorRef = useRef<editor.IStandaloneCodeEditor | null>(null)
    const monacoRef = useRef<Monaco | null>(null)

    // Expose methods to parent components (such as MobileMacroBar)
    useImperativeHandle(ref, () => ({
      insertText: (text: string, cursorOffsetFromEnd: number = 0) => {
        const ed = editorRef.current
        if (!ed) return
        const selection = ed.getSelection()
        if (!selection) return

        const op: editor.ISingleEditOperation = {
          range: selection,
          text,
          forceMoveMarkers: true,
        }
        ed.executeEdits('macro-bar', [op])
        ed.focus()

        if (cursorOffsetFromEnd > 0) {
          const pos = ed.getPosition()
          if (pos) {
            ed.setPosition({
              lineNumber: pos.lineNumber,
              column: Math.max(1, pos.column - cursorOffsetFromEnd),
            })
          }
        }
      },
      focus: () => {
        editorRef.current?.focus()
      },
      formatCode: () => {
        editorRef.current?.getAction('editor.action.formatDocument')?.run()
      },
    }))

    // Define and apply custom dark theme
    const handleBeforeMount = (monaco: Monaco) => {
      monaco.editor.defineTheme('revex-dark', {
        base: 'vs-dark',
        inherit: true,
        rules: [
          { token: '', foreground: 'c9d1d9', background: '161926' },
          { token: 'keyword', foreground: 'ffb000', fontStyle: 'bold' },
          { token: 'keyword.type', foreground: '79c0ff' },
          { token: 'type', foreground: '79c0ff' },
          { token: 'string', foreground: '7ee787' },
          { token: 'number', foreground: '79c0ff' },
          { token: 'comment', foreground: '6e7681', fontStyle: 'italic' },
          { token: 'identifier', foreground: 'e6edf3' },
          { token: 'delimiter', foreground: '8b949e' },
          { token: 'operator', foreground: 'ff7b72' },
        ],
        colors: {
          'editor.background': '#161926',
          'editor.foreground': '#c9d1d9',
          'editorCursor.foreground': '#ffb000',
          'editor.lineHighlightBackground': '#1f2438',
          'editorLineNumber.foreground': '#484f58',
          'editorLineNumber.activeForeground': '#ffb000',
          'editor.selectionBackground': '#264f78',
          'editor.inactiveSelectionBackground': '#264f7855',
          'editorIndentGuide.background': '#21262d',
          'editorIndentGuide.activeBackground': '#30363d',
          'editorError.foreground': '#ef4444',
          'editorWarning.foreground': '#ffb000',
        },
      })
    }

    const handleEditorDidMount: OnMount = (editorInstance, monacoInstance) => {
      editorRef.current = editorInstance
      monacoRef.current = monacoInstance

      // Configure editor options
      editorInstance.updateOptions({
        fontFamily: "'JetBrains Mono', monospace",
        fontLigatures: false, // STRICT ANTI-ZOMBIE MANIFESTO: ligatures explicitly disabled
        fontSize: 14,
        lineHeight: 22,
        tabSize: 4,
        insertSpaces: true,
        renderWhitespace: 'selection',
        minimap: { enabled: false },
        scrollBeyondLastLine: false,
        automaticLayout: true,
        contextmenu: true,
        cursorBlinking: 'smooth',
        cursorSmoothCaretAnimation: 'on',
        bracketPairColorization: { enabled: true },
        tabFocusMode,
      })

      // Add keyboard shortcuts
      // Cmd+Enter or Ctrl+Enter -> Run Check
      editorInstance.addCommand(
        monacoInstance.KeyMod.CtrlCmd | monacoInstance.KeyCode.Enter,
        () => {
          onRunCheck()
        }
      )

      // Cmd+Alt+R -> Reset template
      editorInstance.addCommand(
        monacoInstance.KeyMod.CtrlCmd | monacoInstance.KeyMod.Alt | monacoInstance.KeyCode.KeyR,
        () => {
          onReset()
        }
      )
    }

    // Toggle Monaco Tab Focus Mode (WCAG accessibility)
    useEffect(() => {
      if (editorRef.current) {
        editorRef.current.updateOptions({
          tabFocusMode,
        })
      }
    }, [tabFocusMode])

    // Update Model Markers when errors change
    useEffect(() => {
      const ed = editorRef.current
      const monaco = monacoRef.current
      if (!ed || !monaco) return

      const model = ed.getModel()
      if (!model) return

      const markers: editor.IMarkerData[] = errors.map((err) => {
        const startLine = Math.max(1, err.start_line ?? 1)
        const startCol = Math.max(1, err.start_column ?? 1)
        const endLine = Math.max(startLine, err.end_line ?? startLine)
        let endCol = err.end_column ?? startCol + 1
        if (endLine === startLine && endCol <= startCol) {
          endCol = startCol + 3 // Ensure squiggle is visible
        }

        return {
          startLineNumber: startLine,
          startColumn: startCol,
          endLineNumber: endLine,
          endColumn: endCol,
          message: `[${err.error_code}] ${err.message}`,
          severity:
            err.severity === 'warning'
              ? monaco.MarkerSeverity.Warning
              : monaco.MarkerSeverity.Error,
        }
      })

      monaco.editor.setModelMarkers(model, 'revex-validator', markers)
    }, [errors])

    return (
      <div className="h-full w-full relative bg-[#161926] overflow-hidden flex flex-col">
        {/* Editor Sub-Header bar */}
        <div className="h-9 px-3.5 border-b border-white/10 bg-[#12141f] flex items-center justify-between shrink-0 text-xs font-mono text-[#8b949e]">
          <div className="flex items-center gap-2">
            <span className="text-[#ffb000] font-bold">SOLUTION.PY</span>
            <span className="text-white/20">|</span>
            <span className="text-[11px]">Python 3.13</span>
            <span className="text-white/20 hidden sm:inline">|</span>
            <span className="text-[10px] text-white/40 hidden sm:inline">
              Ligatures Disabled
            </span>
          </div>

          <div className="flex items-center gap-3 text-[11px]">
            {errors.length > 0 ? (
              <span className="text-[#ef4444] font-semibold flex items-center gap-1">
                <span className="w-2 h-2 rounded-full bg-[#ef4444] animate-pulse" />
                {errors.length} {errors.length === 1 ? 'error' : 'errors'}
              </span>
            ) : (
              <span className="text-[#10b981] font-medium hidden sm:inline">No syntax markers</span>
            )}
          </div>
        </div>

        {/* Editor Container */}
        <div className="flex-1 w-full relative">
          <Editor
            height="100%"
            defaultLanguage="python"
            theme="revex-dark"
            value={code}
            onChange={(val) => onChange(val || '')}
            beforeMount={handleBeforeMount}
            onMount={handleEditorDidMount}
            options={{
              wordWrap: 'off',
              padding: { top: 12, bottom: 24 },
            }}
          />
        </div>
      </div>
    )
  }
)

MonacoEditor.displayName = 'MonacoEditor'
