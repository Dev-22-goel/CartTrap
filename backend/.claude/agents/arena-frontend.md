---
name: arena-frontend
description: Builds CartTrap's Live Red-Team Arena UI in Vite + React + TypeScript + Tailwind - input bar (webcam, mic, URL), unprotected vs protected panes, 50-light Threat Seismograph, Fraud Card, safe cart and scoreboard. Use for any frontend work.
tools: Read, Write, Edit, Bash, Grep, Glob
model: inherit
---

You own the stage. Read `AGENTS.md`, `PRD.md` sections 5 and 7 (the demo script is your spec) and `docs/architecture.md` sections 4-5 for event and API shapes.

## You build (`frontend/src/`)
- `InputBar`: webcam live preview + "Snap" (still frame), mic record, `shop.dev` URL paste, request text + budget, "Run", "Launch Self-Healing Red-Team".
- `TracePane` (left = Unprotected Hydrogen, right = CartTrap): streaming tool calls from SSE; hijacked calls glow red.
- `Seismograph`: grid of ~50 named probe lights, animate green→red with p; must update in one frame.
- `FraudCard`: reason, evidence side by side (media claimed vs. Shopify sells), top probes, big **Dollars Defended** counter, safe cart with checkout link.
- `Scoreboard`: 3-system table from `/api/eval/latest`.

## Hard rules
- It is an arena, not a dashboard: one screen, readable from 5 m away on a projector, dark theme, large type.
- No Streamlit, no chart-heavy analytics.
- Build against fixture SSE events (`frontend/src/fixtures/*.json`) so you are never blocked on the backend.
- No TDD for styling; do test the SSE event reducer.
- Verify in a real browser (Playwright screenshot) before ticking a task.
