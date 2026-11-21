# Member 4 lane contract (Claude Code ↔ Codex)

Read this before every Member 4 job, whether you are Claude Code or Codex. It overrides the ownership table in `AGENTS.md` for Member 4 work only (ADR m4/0006). Project rules in `AGENTS.md` "Non-negotiables" and `plan.md` "Global Constraints" still apply in full.

## 1. Who owns which file

| File / path | Owner lane | Builder | After merge, owned by |
|---|---|---|---|
| `eval/metrics.py`, `tests/test_metrics.py` | Codex | gpt-6.2-sol | eval-engineer |
| `eval/run_eval.py`, `eval/runner/**`, `tests/test_run_eval.py` | Codex | gpt-6.2-astra | eval-engineer |
| `backend/m4_routes.py`, `backend/replay.py`, `tests/test_m4_routes.py`, `eval/results/sample.json` | Codex | gpt-6-luna | defender-engineer (routes), eval-engineer (sample) |
| `backend/selfheal.py`, `backend/redteam_carbon.py`, `tests/test_selfheal.py`, `tests/test_redteam_loop.py` | Codex | gpt-6.2-astra | defender-engineer |
| `handoff/codex-status.md` | Codex | any | Codex only, always |
| `eval/build_cases.py`, `eval/cases/**`, `eval/holdout/**`, `eval/results/<runs>.json` | Claude | eval-engineer | — |
| `eval/golden/**`, `docs/failure-analysis.md` | Claude | m4-failure-analyst (T15) | — |
| `backend/defender_neon.py`, `backend/prompts/neon_fraud_card.md`, `tests/test_defender.py` | Claude | defender-engineer | — |
| `redteam/sandbox/**`, `runs/redteam_demo.jsonl` | Claude | redteam-engineer | — |
| `.superpowers/sdd/progress.md`, `handoff/*.md` except `codex-status.md` | Claude | m4-handoff-scribe | — |
| `docs/decisions/m4/**`, `docs/member-4-plan.md`, `docs/integration-m4.md` | You (Adish) | Claude main session | — |

**Never touched by either Member 4 lane:** `backend/main.py`, `Makefile`, requirements (Member 1) · `backend/schemas.py`, `backend/guarded_shopper.py`, `rules.json`, firewall files (Member 2) · `redteam/forge/**`, `frontend/**` (Member 3) · `AGENTS.md`, `plan.md`, `PRD.md`, `docs/architecture.md`, `plans/**` (team).

A file changes lane **only** when Adish merges the Codex branch into `adish` and the `m4-spec-verifier` passes.

## 2. Rules

1. Edit only files your lane owns right now. If you need a change elsewhere, write it into your status (Codex: `handoff/codex-status.md`) and stop.
2. Codex runs in `..\CartTrap-codex` on branch `m4-codex`, with `-s workspace-write`. Claude runs in `CartTrap` on `adish`. Neither pushes to `main`.
3. **After 2:30 PM, nobody edits `eval/cases/**`.** After the holdout is built, nobody edits `eval/holdout/**`.
4. Skills for Codex: read them by path, e.g. `.claude/skills/firewall-rules/SKILL.md`, `.claude/skills/attack-forge/SKILL.md`, `.claude/skills/shop-mcp/SKILL.md`, `.claude/skills/run-eval/SKILL.md`.
5. When an ADR in `docs/decisions/m4/` governs your files, it's your spec: meet its Verification checklist.
6. Test-first (superpowers TDD). Paste real pytest output in your final report.
7. Dependencies are `hypothesis`, `pytest-asyncio`, `numpy`, `vcrpy` (ADR m4/0007). If one is missing, say so; don't edit requirements files.
8. No `complete_checkout`, `complete_spend_request` or `create_spend_request`. Shop access only via `ShopMCP`. No DB, no Streamlit. Model IDs only from `backend/config.py`. Secrets only from `.env`, which you never read or print.

## 3. Merge points (Adish runs them)
11:40 Sol C1 · 12:20 Luna L1 · 1:15 Astra A2 · 3:15 Astra A1. Each one goes: Opus plan turn reviews the diff → `git merge m4-codex` → `m4-spec-verifier` → PASS → ownership moves per §1.

## 4. Shared case vocabulary (set by eval/build_cases.py, 2026-11-21)
- Attack `vector`: `sticky_note`, `pack_lie`, `pdf_spend`, `voice_coercion`, `split_payload` (6 each). Case ids `atk_<vector>_NN`.
- Benign `vector`: `promo_banner`, `blurry_photo`, `casual_voice`, `plain`; 4 cases per `category`. Case ids `ben_<category>_NN`.
- Sticky-note media: `eval/props/sticky_01..06.jpg`. Categories are placeholders until live sampling.
Runner and metrics code must key on these names; change them only via the eval-engineer.
