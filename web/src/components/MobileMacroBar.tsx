import React from 'react'

interface MacroItem {
  label: string
  insertText: string
  cursorOffsetFromEnd?: number // moves cursor left by N characters after insertion
  description: string
}

const MACRO_ITEMS: MacroItem[] = [
  { label: ':', insertText: ': ', cursorOffsetFromEnd: 0, description: 'Type colon' },
  { label: '->', insertText: ' -> ', cursorOffsetFromEnd: 0, description: 'Return arrow' },
  { label: '|', insertText: ' | ', cursorOffsetFromEnd: 0, description: 'Union operator' },
  { label: '[ ]', insertText: '[]', cursorOffsetFromEnd: 1, description: 'Generic brackets' },
  { label: 'int', insertText: 'int', cursorOffsetFromEnd: 0, description: 'Integer type' },
  { label: 'str', insertText: 'str', cursorOffsetFromEnd: 0, description: 'String type' },
  { label: 'bool', insertText: 'bool', cursorOffsetFromEnd: 0, description: 'Boolean type' },
  { label: 'list[', insertText: 'list[]', cursorOffsetFromEnd: 1, description: 'List generic' },
  { label: 'dict[', insertText: 'dict[]', cursorOffsetFromEnd: 1, description: 'Dict generic' },
  { label: 'None', insertText: 'None', cursorOffsetFromEnd: 0, description: 'None return' },
  { label: '⇥ Tab', insertText: '    ', cursorOffsetFromEnd: 0, description: 'Indent 4 spaces' },
]

interface MobileMacroBarProps {
  onInsert: (text: string, cursorOffsetFromEnd?: number) => void
}

export const MobileMacroBar: React.FC<MobileMacroBarProps> = ({ onInsert }) => {
  return (
    <nav
      aria-label="Type Hint Macro Bar"
      className="h-12 bg-[#12141f] border-t border-white/10 px-2 flex items-center gap-1.5 overflow-x-auto no-scrollbar shrink-0 z-30 select-none shadow-lg"
    >
      <div className="flex items-center gap-1.5 min-w-max mx-auto py-1">
        {MACRO_ITEMS.map((item) => (
          <button
            key={item.label}
            onClick={() => onInsert(item.insertText, item.cursorOffsetFromEnd)}
            title={item.description}
            aria-label={item.description}
            className="h-9 min-w-[44px] px-2.5 rounded bg-[#161926] hover:bg-[#1f2438] active:bg-[#ffb000]/20 active:text-[#ffb000] border border-white/10 active:border-[#ffb000]/40 text-[#c9d1d9] text-xs font-mono font-semibold transition flex items-center justify-center shrink-0 shadow-xs touch-manipulation"
          >
            {item.label}
          </button>
        ))}
      </div>
    </nav>
  )
}
