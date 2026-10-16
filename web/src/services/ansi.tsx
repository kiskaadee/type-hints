import type { CSSProperties, ReactElement } from 'react'
import { parseAnsi } from './ansiParser'

export function RenderAnsi({ text }: { text: string }): ReactElement {
  const spans = parseAnsi(text)

  return (
    <span>
      {spans.map((span, idx) => {
        const style: CSSProperties = {
          color: span.color,
          fontWeight: span.bold ? 700 : undefined,
          opacity: span.dim ? 0.65 : undefined,
          textDecoration: span.underline ? 'underline' : undefined,
        }

        return (
          <span key={idx} style={style}>
            {span.text}
          </span>
        )
      })}
    </span>
  )
}
