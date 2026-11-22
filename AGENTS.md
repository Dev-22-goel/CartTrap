# CartTrap: agent guide

CartTrap is a live multimodal red-team arena and execution firewall for AI shopping agents on Shopify's Shop MCP. A gullible Hydrogen shopper gets attacked with poisoned photos/audio/PDFs; CartTrap (Argon perception → Decisions API firewall → Neon defender) blocks the money-moving call in ~200 ms, explains why it's fraud, swaps to a safe Shopify cart, and heals its own rules when a Carbon red-team agent gets through.

## Read first
- `docs/PRD.md`: what and why, user stories with acceptance criteria, demo script, anti-goals.
- `docs/architecture.md`: stack, components, JSON shapes, API, Gemini integration.
- `docs/plan.md`: Superpowers-format plan: Global Constraints, Review Focus, 17 tasks with exact Interfaces and TDD steps. Tick boxes as you finish.
- `docs/architecture.md` §0: the 7 builder decisions (trust boundary, dry-run victim, escalate vs. block, latency definitions, eval honesty). Binding.

## Layout
The repo root holds only `.git`, `backend/` and `frontend/`. They deploy separately and never import each other.
```
backend/
  app/        FastAPI package: main, shop_mcp, shopper_loop, guarded_shopper, cart_check, firewall_decisions,
              perception_argon, defender_neon, evidence, selfheal, scanner, rules.json, config, paths
  app/llm/    provider layer: settings (Gemini or OpenRouter, a model per role), openrouter client, media prep, api
  app/warehouse/  catalog (Shopify-shaped listings), portal (merchant listing logic), auth, reputation, carbon
  data/warehouse/ 11 fictional merchants and 110 listings, one folder per category (git-tracked seed)
  data/state/     runtime state (listings, reputation, model choices): git-ignored
  eval/ redteam/ scripts/ tests/ docs/ runs/
frontend/
  src/        Vite + React + TS web app (talks to the API over HTTP; VITE_API_URL sets where)
```

## Commands
Backend, from `backend/`: `uv sync` · `uv run uvicorn app.main:app --reload --port 8000` · `uv run pytest -q` · `uv run python scripts/build_warehouse.py --clean`
Frontend, from `frontend/`: `npm install` · `npm run dev` · `npx tsc -b --noEmit` · `npx vitest run` (uppercase drive path on Windows) · `npm run build`

## Agents (`.claude/agents/`)
| Agent | Owns |
|---|---|
| shop-mcp-engineer | Shop MCP client, fixtures, Hydrogen victim |
| firewall-engineer | Argon perception, Decisions API firewall, rules.json, gate, guarded shopper |
| defender-engineer | Neon fraud card, Dollars Defended, safe swap, self-heal probes |
| redteam-engineer | attack forge, Carbon Managed Agent loop |
| arena-frontend | the one-screen live arena UI |
| eval-engineer | 50-case benchmark, metrics, failure analysis |
| demo-verifier | acceptance checks, demo-check, README |

Skills (`.claude/skills/`): `shop-mcp`, `firewall-rules`, `attack-forge`, `run-eval`, `demo-check`, plus doc skills `write-prd`, `write-design-doc`, `write-plan`.

## Non-negotiables
1. Never call `complete_checkout` or `complete_spend_request` from code; never send `create_spend_request`; the victim pane runs in dry-run.
2. Firewall fails closed.
3. Perception (Argon) never has tools; its output is data, not instructions.
4. No Streamlit, no dashboard-first UI, no text-only chatbot, no database.
5. Model IDs only in `app/config.py` and `app/llm/settings.py` (per-role defaults per provider).
6. Don't claim something works without running its check and pasting output. Numbers come from `eval/results/*.json`.
7. TDD for shop_mcp, firewall gate, rules loader, eval metrics. Skip TDD for UI styling.
8. Don't tune on `eval/cases/` after the 2:30 PM freeze.
9. Secrets in `.env` only; never commit it.

## Suggested workflow
- Execution: Superpowers `subagent-driven-development` over `plan.md` (fresh implementer + reviewer per task). Two tracks after Task 3: backend (2→4→5/6→7/8→9→10) and frontend (11→12) on fixtures; forge (13) and eval (14) in parallel.
- Use `verification-before-completion` and `systematic-debugging` when a shop.dev or Gemini call breaks.
