# CartTrap: agent guide

CartTrap is a live multimodal red-team arena and execution firewall for AI shopping agents on Shopify's Shop MCP. A gullible Hydrogen shopper gets attacked with poisoned photos/audio/PDFs; CartTrap (Argon perception → Decisions API firewall → Neon defender) blocks the money-moving call in ~200 ms, explains why it's fraud, swaps to a safe Shopify cart, and heals its own rules when a Carbon red-team agent gets through.

## Read first
- `PRD.md`: what and why, user stories with acceptance criteria, demo script, anti-goals.
- `docs/architecture.md`: stack, components, JSON shapes, API, Gemini integration.
- `plan.md`: Superpowers-format plan: Global Constraints, Review Focus, 17 tasks with exact Interfaces and TDD steps. Tick boxes as you finish.
- `plans/integration.md` + `plans/member-1..4.md`: who owns which tasks, the shared timeline, contracts C1–C8, sync checkpoints S1–S7, merge rules, `make integration` tests.
- `docs/architecture.md` §0: the 7 builder decisions (trust boundary, dry-run victim, escalate vs. block, latency definitions, eval honesty). Binding.

## Layout
```
backend/   FastAPI: shop_mcp, victim_hydrogen, perception_argon, guarded_shopper, firewall_decisions, defender_neon, redteam_carbon, rules.json, config
frontend/  Vite + React + TS arena
eval/      cases/ (frozen 2:30 PM), golden/ (tuning), run_eval.py, results/
redteam/   forge/ (attack generators), sandbox/ (Carbon Managed Agent AGENTS.md + skills), out/
docs/      architecture, failure-analysis, notes-apis, skills-research
```

## Commands
`make dev` · `make test` · `pytest -m live` (real APIs) · `python eval/run_eval.py ...` · `make demo-check`

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
5. Model IDs only in `backend/config.py` (confirm at 10:00 AM resource sheet).
6. Don't claim something works without running its check and pasting output. Numbers come from `eval/results/*.json`.
7. TDD for shop_mcp, firewall gate, rules loader, eval metrics. Skip TDD for UI styling.
8. Don't tune on `eval/cases/` after the 2:30 PM freeze.
9. Secrets in `.env` only; never commit it.

## Suggested workflow
- Execution: Superpowers `subagent-driven-development` over `plan.md` (fresh implementer + reviewer per task). Two tracks after Task 3: backend (2→4→5/6→7/8→9→10) and frontend (11→12) on fixtures; forge (13) and eval (14) in parallel.
- Use `verification-before-completion` and `systematic-debugging` when a shop.dev or Gemini call breaks.
