# Revex Web Playground

Interactive type-hint laboratory web client built with **React 19**, **TypeScript**, **Tailwind CSS v4**, and **Monaco Editor**.

## 1. Aesthetic & Architecture (Anti-"Zombie UI")

- **Scientific Monasticism / DEC VT220 Terminal Aesthetic:** Deep graphite chassis (`#0d1117`), dark panels (`#161926`), phosphor amber (`#ffb000`), mint (`#10b981`), and vermillion (`#ef4444`).
- **Tactile CRT Detail:** Sunken inset shadow and subtle scanlines overlay on the interactive DOM terminal.
- **Strict Ligature Suppression:** `font-variant-ligatures: none !important;` and `fontLigatures: false` enabled across code and UI chrome to keep Python type tokens (`->`, `|`, `==`) optically unambiguous.
- **Mobile-First Macro Strip:** Docked bottom accessory bar for rapid input of Python type syntax (`:`, `->`, `|`, `[ ]`, `int`, `str`, `list[`, `dict[`, `None`, `Tab`) with automatic inner cursor positioning.
- **The 5 States Lifecycle:** Handles `empty`, `loading` (non-blocking top phosphor line), `error` (AST structural failures), `partial` (AST passed, Pyright failed), and `success` (mint glow + celebration).
- **Local-First Draft Persistence:** Autosaves edits to `localStorage` (`revex_draft_${exerciseId}`) with zero code loss across refreshes or disconnections.

---

## 2. Getting Started

### Development Workflow

1. **Start the Revex FastAPI backend server** (from repository root):
   ```bash
   uv run uvicorn revex.server.app:app --host 127.0.0.1 --port 8000 --reload
   ```

2. **Start the Vite development server** (from `web/` directory):
   ```bash
   cd web
   npm install
   npm run dev
   ```
   The Vite dev server runs at `http://localhost:5173` and automatically proxies `/api` requests to `http://127.0.0.1:8000`.

### Production Build

```bash
cd web
npm run build
```

Build artifacts will be written to `web/dist/`.

---

## 3. Keyboard Shortcuts

- **`Cmd+Enter` / `Ctrl+Enter`**: Run Validation Check (AST + Pyright).
- **`Enter` (during Success state)**: Advance to next module.
- **`Cmd+Option+R`**: Reset editor to canonical starter template.
- **`Ctrl+M`**: Toggle Tab-Moves-Focus accessibility mode (WCAG 2.1.2 compliance).
