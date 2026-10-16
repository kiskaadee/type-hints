# Revex Web Client: Backend Friction, Assumptions & Open Questions

**Author:** Anne Droid, Senior Frontend Engineer & UX Specialist  
**Target:** Core Engine & Backend Engineering Teams  
**Date:** October 2026  
**Status:** Active Architectural Feedback  

---

## 1. Executive Summary

During the initial scaffolding and implementation of the Revex Web Client (`web/`), the frontend architecture was aligned with the **Anti-"Zombie UI"** design manifesto (DEC VT220 / Bell Labs aesthetic, strict ligature suppression, mobile-first macro ergonomics, and the 5-state validation lifecycle).

This document captures concrete friction points in the backend API contracts, assumptions implemented in the client runtime, and open questions requiring coordination with the backend team.

---

## 2. API Contract Friction & Proposed Backend Enhancements

### 2.1 Lack of Explicit `stage` Discriminator on `CheckErrorItem`

- **Current State:**  
  `CheckErrorItem` in `src/revex/server/schemas.py` provides:
  ```python
  class CheckErrorItem(BaseModel):
      start_line: int | None = None
      start_column: int | None = None
      end_line: int | None = None
      end_column: int | None = None
      message: str
      error_code: str
      severity: Literal["error", "warning"] = "error"
  ```
  The client has to inspect string prefixes (e.g., `err.error_code.startswith("AST")`) to determine whether a failure occurred in Stage 1 (AST Structural Validator) or Stage 2 (Pyright Static Type Checker).

- **UX Impact:**  
  The 5-state design requires distinguishing between:
  - **Error State**: AST structural defects (missing type annotations).
  - **Partial State**: AST passed cleanly, but Pyright type consistency failed (e.g. incompatible return type).

- **Proposed Enhancement:**  
  Add an explicit `stage` field to `CheckErrorItem`:
  ```python
  class CheckErrorItem(BaseModel):
      stage: Literal["ast", "pyright"]
      start_line: int | None = None
      start_column: int | None = None
      end_line: int | None = None
      end_column: int | None = None
      message: str
      error_code: str
      severity: Literal["error", "warning"] = "error"
  ```

---

### 2.2 Unpersisted User Progress & `saved_code` Field

- **Current State:**  
  `ExerciseDetailResponse` exposes `saved_code: str | None = None`, but the backend implementation currently always returns `None` because the server is purely stateless. Completed status and user streaks are not persisted on the server.

- **Frontend Mitigation:**  
  The web client implements client-side persistence using `localStorage`:
  - `revex_draft_${exerciseId}`: Automatically caches unsaved code changes.
  - `revex_last_exercise_id`: Restores the student's active workspace position.
  - In-memory completion tally updates during the browser session.

- **Proposed Enhancement:**  
  Introduce an optional session cookie or header (`X-Session-ID: <uuid>`), enabling the server to persist student progress and solution drafts to a SQLite/PostgreSQL store (as specified in the Web Architecture RFC).

---

### 2.3 Pyright Subprocess Overhead & Rate Limiting

- **Current State:**  
  Each `POST /api/v1/check` triggers synchronous disk writes and invokes `pyright --outputjson` via subprocess execution.

- **UX Impact:**  
  If a student rapidly presses `Cmd+Enter` or if a network backlog occurs, the server could experience thread pool exhaustion.

- **Proposed Enhancement:**  
  1. Add HTTP 429 rate limiting per client session.
  2. Evaluate a persistent Pyright Language Server Protocol (LSP) daemon pool or worker queue for production deployment.

---

## 3. Assumptions Made During Client Implementation

1. **Local-First Draft Resilience:**  
   Code in the editor is persisted to `localStorage` on every keystroke. If the backend returns an HTTP 500 or network connection drops, student work is never lost.
2. **Strict Font Ligature Suppression:**  
   Ligatures are strictly disabled (`font-variant-ligatures: none !important;` and `fontLigatures: false` in Monaco). Python type hint syntax (e.g., `->`, `|`, `==`) must remain visually distinct glyphs to prevent learner confusion.
3. **Mobile Macro Ergonomics:**  
   Because typing brackets, pipes, and colons on mobile keyboards introduces significant cognitive friction, a docked accessory bar provides one-tap token insertion with automatic cursor placement inside generic brackets (`[]`).
4. **Fallback Navigation:**  
   If no previous or next exercise ID is provided, the UI gracefully disables adjacent navigation controls while keeping the catalog selector available.

---

## 4. Open Questions for Core & Backend Teams

| # | Question | Current Assumption | Proposed Next Step |
|---|---|---|---|
| **1** | How should authentication be structured? | Unauthenticated guest session with local persistence. | Implement OIDC / GitHub OAuth code flow as defined in RFC Section 2. |
| **2** | Will multi-file exercises (e.g., separate `.pyi` stub files or helper modules) be supported? | Single `solution.py` file per exercise. | Design multi-tab Monaco buffer layout if multi-file manifests are introduced. |
| **3** | Is browser-side Pyodide / WebAssembly validation on the roadmap? | Server-side validation via FastAPI + Pyright. | Keep server-side validation for strict Pyright fidelity; consider client AST parsing for instant feedback. |
| **4** | What is the production deployment topology? | Vite SPA + FastAPI behind reverse proxy (Caddy / Nginx). | Containerize both with Docker Compose and test under production loads. |
