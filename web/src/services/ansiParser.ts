export interface AnsiSpan {
  text: string
  bold?: boolean
  dim?: boolean
  underline?: boolean
  color?: string
}

const COLOR_MAP: Record<number, string> = {
  30: '#484f58', // black / dark gray
  31: '#ef4444', // red (vermillion)
  32: '#10b981', // green (mint)
  33: '#ffb000', // yellow (amber)
  34: '#58a6ff', // blue
  35: '#bc8cff', // magenta
  36: '#39c5cf', // cyan
  37: '#f0f6fc', // white
  90: '#8b949e', // bright black / gray
  91: '#f85149', // bright red
  92: '#34d399', // bright green
  93: '#fde047', // bright yellow
  94: '#79c0ff', // bright blue
  95: '#d2a8ff', // bright magenta
  96: '#56d4dd', // bright cyan
  97: '#ffffff', // bright white
}

export function parseAnsi(input: string): AnsiSpan[] {
  if (!input) return []

  const spans: AnsiSpan[] = []
  // Regex to match ANSI escape codes like \x1b[32m or \u001b[1;31m
  // eslint-disable-next-line no-control-regex
  const ansiRegex = /\x1b\[([0-9;]*)m/g

  let lastIndex = 0
  let currentBold = false
  let currentDim = false
  let currentUnderline = false
  let currentColor: string | undefined = undefined

  let match: RegExpExecArray | null

  while ((match = ansiRegex.exec(input)) !== null) {
    const textBefore = input.slice(lastIndex, match.index)
    if (textBefore.length > 0) {
      spans.push({
        text: textBefore,
        bold: currentBold,
        dim: currentDim,
        underline: currentUnderline,
        color: currentColor,
      })
    }

    const params = match[1] ? match[1].split(';').map((s) => parseInt(s, 10)) : [0]

    for (const code of params) {
      if (isNaN(code) || code === 0) {
        currentBold = false
        currentDim = false
        currentUnderline = false
        currentColor = undefined
      } else if (code === 1) {
        currentBold = true
      } else if (code === 2) {
        currentDim = true
      } else if (code === 4) {
        currentUnderline = true
      } else if (code === 22) {
        currentBold = false
        currentDim = false
      } else if (code === 24) {
        currentUnderline = false
      } else if (code === 39) {
        currentColor = undefined
      } else if (COLOR_MAP[code]) {
        currentColor = COLOR_MAP[code]
      }
    }

    lastIndex = ansiRegex.lastIndex
  }

  const remainingText = input.slice(lastIndex)
  if (remainingText.length > 0) {
    spans.push({
      text: remainingText,
      bold: currentBold,
      dim: currentDim,
      underline: currentUnderline,
      color: currentColor,
    })
  }

  return spans
}
