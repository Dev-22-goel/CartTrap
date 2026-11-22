# CartTrap full-app integration plan (branch `adish` @ 24b0942, 2:10 PM ET)

Written by an Opus planning pass that read the code only. ADRs 0021–0024 record the cross-member changes. Codex briefs: `handoff/codex-F1-*.md`, `codex-G1-*.md`, `codex-R1-*.md`.

## Demo breakers (never cut)
1. **The stream never closes.** It doesn't close on the `"system"` `done` event (`src/api.ts:47,65`, `src/types.ts:3`), so EventSource reconnects and replays every event in a loop.
2. **`POST /api/redteam/launch` returns 404.** There's no `eval/golden/redteam/` and no `runs/redteam_demo.jsonl`.
3. **`/api/eval/latest` shows hand-made numbers.** It falls back to `sample.json`, which breaks "live-only".

## Seams
| # | Seam | Fix | Task |
|---|---|---|---|
| S1 | final `done` on pane `system` | `Pane` gains `"system"`; close on a system `done`; mark every pane finished | F1 |
| S2–S4 | victim `intercepted`/`tool_call` shapes: args under `result.arguments`; cart `cart.line_items[].item.id`; spend request in cents | backend adds `arguments`, `attempted_spend` ($), `quantity`, `hijacked`. Frontend reads `args.cart.line_items`, `item.id`, `approval_limit/100` | D1 + F1 |
| S5 | guarded verdict `cart_total` ignored | reducer back-fills the spend; extend the `Verdict` type | F1 |
| S6 | fraud card / safe cart | matches; add `variant_id?` | F1 |
| S7 | red-team `stage` vocabulary not emitted (ADR 0012 never implemented) | emit `stage` + `message` at the source (step→stage mapping) | R1 |
| S8 | red-team launch 404 | golden red-team and benign fixtures, plus a recorded fallback | R1, R2 |
| S9 | `GET /api/rules` missing | new route | G1 |
| S10 | `/api/route` missing | optional, cut first | G1 (P2) |
| S12 | run form drops `product_id` and `pdf`; the URL wins over the id | add both; `product_ref = product_id or demo_product_id or product_url` | G1 |
| S13–S14 | catalog / CORS | demo from Vite (dev or preview); no proxy needed | — |
| S15 | `normalizeEval` drops `by_modality`, `n_errors` | pass them through | F1 |
| S17 | no per-modality report; no `eval/cases/` | `CaseResult.poisoned_modality` + `Report.by_modality`; cases from the generated dataset | E1, E2 |
| S18 | sample shadowing | no sample fallback (404 instead); UI ignores `meta.sample` | G2 + F1 |
| S19 | dataset not exposed | `GET /api/dataset`, `GET /api/dataset/{id}/{file}`, a Dataset page | G1 + F2 |

## Tasks (disjoint files; Haiku verifier gate before each merge)
| Task | Lane | Files | Window |
|---|---|---|---|
| F1 reducer + api contract | Codex gpt-6.2-sol | `src/state.ts`, `src/state.test.ts`, `src/api.ts`, `src/types.ts`, `src/lib/spend.ts`, ADR 0022 | 2:15–2:55 |
| F2 per-modality table + Dataset page | Claude arena-frontend (Sonnet) | `src/components/Scoreboard.tsx`, `src/components/Dataset.tsx`, `src/lib/dataset.ts`, `src/App.tsx`, `src/components/Header.tsx` | 2:15–3:20 |
| G1 app routes + run form | Codex gpt-6-luna | `backend/app_routes.py`, `backend/main.py`, `tests/test_app_routes.py`, `tests/test_api.py`, ADR 0021 | 2:15–2:50 |
| G2 no sample fallback | Codex gpt-6-luna (after G1) | `backend/m4_routes.py`, `tests/test_m4_routes.py` | 2:50–3:00 |
| D1 event enrichment + live smoke | Claude defender-engineer (Sonnet) | `backend/shopper_loop.py`, `tests/test_shopper_loop.py` | 2:15–2:50 |
| E1 per-modality report | Claude eval-engineer (Sonnet) | `eval/run_eval.py`, `tests/test_run_eval.py`, `eval/build_cases.py`, ADR 0023 | 2:15–2:40 |
| E2 cases from the dataset + official run | Claude eval-engineer (after E1) | `eval/cases_from_generated.py`, its test, `eval/cases/**` | 2:40–3:45 |
| R1 live red-team heal | Codex gpt-6.2-astra (Claude redteam-engineer if refused) | `backend/redteam_carbon.py`, `backend/selfheal.py`, `tests/test_redteam_loop.py`, `scripts/make_redteam_fixtures.py`, `eval/golden/redteam/**`, `eval/golden/benign/**`, ADR 0024 | 2:15–3:30 |
| R2 recorded fallback | Claude redteam-engineer (after R1) | `runs/redteam_demo.jsonl` | 3:30–3:50 |

**Merge order:** D1 → G1 → F1 → E1 → G2 → E2 → F2 → R1 → R2.

## Demo path (3 min)
| Time | Step | What happens |
|---|---|---|
| 0:00–0:20 | Home → search "daily multivitamins" → real product page | Vite `/shop-mcp` proxy |
| 0:20–1:20 | Dataset → `type-21-v1` → Run in Compare | victim hijacked (qty 10, $) vs guarded block + fraud card + real `continue_url`; the stream closes |
| 1:20–2:10 | Safety updates → Launch | attack → bypass → probe_proposed → validate → patched (vN→vN+1) → reblocked |
| 2:10–2:50 | Performance | 3 systems, the "Where it breaks" per-modality table, failures, meta |
| 2:50–3:00 | Honest failures | — |

## Verification (3:20 and 4:05)
1. `npm run typecheck && npm test && npm run build`
2. `pytest -q`
3. Routes list `/api/rules`, `/api/dataset`, `/api/eval/latest`, `/api/redteam/launch`
4. uvicorn :8000 + `npm run dev`: a Compare run shows no duplicate steps; the Assistant reaches Done; the fraud card shows the continue link
5. `/api/eval/latest` serves the real `latest.json` with `by_modality`
6. The live red-team heal works; then restore `rules.json` from `.bak`

## Cut list (in order)
1. `/api/route`
2. The hardened system
3. Video and audio in eval cases
4. Dataset page polish
5. Live heal → replay
6. Per-modality UI → printout
7. Dataset page → manual upload
