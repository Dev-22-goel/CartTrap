# Member 4 integration plan (branch `adish` @ 072b876, 12:10 PM ET)

Written by an Opus planning pass that read the code on `adish` (with Udaya + dev merged) and `origin/shivam`. ADRs 0010–0016 record the cross-member decisions. Codex briefs: `handoff/codex-I*.md`.

## 1. Seams and mismatches

| # | Seam | Mismatch in code | Fix |
|---|---|---|---|
| S1 | Routes include (ADR 0001) | `main.py` never mounts `m4_router` (`m4_routes.py:25`) | M1 adds `include_router` (ask A1) |
| S2 | Single rules writer (ADR 0009) | shared store is the global `RULES` (`main.py:39`); `redteam_carbon.py:68`, `selfheal.py:240,289` build their own `AtomicRuleStore()`; `rules.RuleStore.append` writes no `.bak` | `app.state.rules = RULES`; route passes it; self-heal writes `.bak` itself |
| S3 | Defender call site | `guarded_shopper.py:82-88` already has `after_block`, and `run_guarded(on_block=)` exists (`:112,194-203`). Our snippet uses the wrong `bus.emit` arity (`trace.py:24`) and the wrong `attempted_spend` import | ADR 0010: defender exposes `on_block(BlockContext)`, M1 passes it in `main.py:45` |
| S4 | Safe swap Shop shapes | `ShopMCP` has no `create_checkout`; `create_cart(shop, lines)` wants `{"variant_id","quantity"}` (`shop_mcp.py:117-123`); defender sends `{"item":{"id"}}`, so the live safe swap crashes. The cart already returns `continue_url` + `totals` (`notes-apis.md`) | ADR 0011: `create_cart` only, ShopMCP line shape, totals in cents |
| S5 | Gemini client / model IDs | `defender_neon.py:72-77` stub model; `:213` builds a client per call from `os.environ`; `selfheal.py:217` has a keyless client | `config.MODELS` + shared `gemini.client()` |
| S6 | FraudCard / SafeCart vs frontend | frontend `SafeCart.line_items = {product_id, quantity, title?, price?}`; ours `{item:{id}, quantity}`; price printed as a cents dict | add `product_id`, `variant_id`, `title`, `price` (dollars) |
| S7 | Eval runner adapters | `systems.py:126` passes nonexistent ShopMCP kwargs; `EvalBus.emit` arity wrong; products map empty; fail-closed raises and leaves the ASR denominator | real `TraceBus`, `RecordingShop(ShopMCP, dry_run=True)`, fail-closed = block (disclosed) |
| S8 | Baseline / hardened | `run_victim` has no `mode`, returns no prices; no hardened prompt | ADR 0014: call `shopper_loop` directly with the victim prompt (+1 hardening sentence) |
| S9 | Metrics vs real shapes | reads `arguments["lines"]`; cents read as dollars; spend requests via `amount` not `approval_limit`; numpy/hypothesis not in `pyproject` | reuse `money.attempted_spend`; stdlib percentiles; `importorskip` (ADR 0016) |
| S10 | Shop mode | M1 cut fixture replay; `--shop replay` has nothing behind it | ADR 0015: live only |
| S11 | Cases | only stubs; no real catalog, no media, no props | `ShopCatalog` adapter + local media renderer; props from Adish |
| S12 | Red-team events vs trace bus | private bus in `m4_routes.py:28-33`; launch awaited inline; replay returned as JSON, not SSE; golden dir missing | ADR 0012: background task on `app.state.bus`, return `{run_id}`, stream via SSE |
| S13 | `redteam_demo.jsonl` format | frontend keys on `data.stage` + `message`; backend emits `data.step` | ADR 0012: adopt M3's `stage` vocabulary |
| S14 | C6 eval JSON | frontend wants `failures[].case_id/note`; latest-by-mtime can shadow the frozen run | ADR 0013: failure fields + `eval/results/latest.json` |
| S15 | Pane `"system"` | frontend maps it to guarded | ask M3 (not blocking) |
| S16 | SDK | local google-genai 2.4.0 vs pinned 3.6.1 | Adish installs 3.6.1 |
| S17 | Codex clone stale | missing Udaya/dev | merge `adish` into `CartTrap-codex` (done by Claude) |

## 2. Tasks

Rules: one Claude builder at a time; one Astra job at a time; Sol/Luna parallel only on disjoint files; each task ends with an `m4-spec-verifier` (Haiku) PASS before merge. Off-limits until Astra A3 merges: `backend/redteam_carbon.py`, `backend/selfheal.py`, `tests/test_redteam_loop.py`, `tests/test_selfheal.py`, `tests/test_carbon_live.py`.

| Task | Lane · model | Files | Window |
|---|---|---|---|
| T1 metrics on real call shapes | Codex · gpt-6.2-sol | `eval/metrics.py`, `tests/test_metrics.py` | 12:25–12:55 |
| T2 defender `on_block` + working safe swap | Codex · gpt-6.2-sol | `backend/defender_neon.py`, `backend/prompts/neon_fraud_card.md`, `tests/test_defender.py` | 12:25–1:15 |
| T3 routes on shared bus + store | Codex · gpt-6-luna | `backend/m4_routes.py`, `backend/replay.py`, `tests/test_m4_routes.py` | 12:25–1:00 |
| T4 eval runner adapters | Claude · eval-engineer (Sonnet) | `eval/runner/systems.py`, `eval/run_eval.py`, `tests/test_run_eval.py` | 12:25–1:20 |
| T5 Shop catalog + local media renderer | Codex · gpt-6.2-sol (after T1) | `eval/build_cases.py`, `tests/test_build_cases.py`, `eval/media_render.py`, `tests/test_media_render.py` | 12:55–1:40 |
| T6 live case build + dry run | Claude · eval-engineer | `eval/cases/**`, `eval/props/**` | 1:40–2:25 |
| T7 self-heal integration (after A3) | Codex · gpt-6.2-astra | `backend/redteam_carbon.py`, `backend/selfheal.py`, their tests | ~1:45–2:45 |
| T8 golden fixtures, live bypass, demo recording | Claude · redteam-engineer | `eval/golden/**`, `runs/redteam_demo.jsonl`, `redteam/sandbox/**` | 3:15–4:05 |
| T9 failure analysis (T15) | Claude · m4-failure-analyst (Opus) | `docs/failure-analysis.md`, `eval/holdout/**`, results | 2:30–3:15 |

Full per-task interfaces and Definitions of Done are in the Codex briefs (`handoff/codex-I1-metrics.md`, `codex-I2-defender.md`, `codex-I3-routes.md`, `codex-I5-cases.md`, `codex-I7-selfheal.md`) and the Claude dispatches in this thread.

### Teammate asks (Adish sends; Member 4 edits none of these files)
- **A1 → M1 (`backend/main.py`, by 1:00):**
  ```python
  from backend.m4_routes import m4_router
  from backend.defender_neon import on_block as defender_on_block   # send after the 1:15 merge
  app.include_router(m4_router)
  app.state.rules = RULES
  # main.py:45
  await run_guarded(..., shop=ShopMCP(), rules=RULES, on_block=defender_on_block)
  ```
- **A2 → M2:** OK on ADR 0010. No change in `guarded_shopper.py`.
- **A3 → M3:**
  - keep the `stage` vocabulary in `redteam_demo.jsonl`
  - read `failures[].case_id`/`note`, `meta.shop_mode="live"`, `meta.n_fail_closed`
  - accept `SafeCart.line_items[].variant_id`
  - treat pane `"system"` as global
  - the red-team button calls `POST /api/redteam/launch`, then streams `/api/runs/{run_id}/stream`

### Order
- **12:25:** T1, T2, T3 (Codex) and T4 (Claude) in parallel
- **1:00 S2:** C6 sample; check A1
- **1:15:** merge T1–T3 and verify
- **1:40:** merge T5, then T6
- **~1:45:** merge A3, then T7
- **2:00 S3:** fraud card visible
- **2:30 S4:** freeze, full run, T9
- **3:00:** merge T7
- **3:15 S5:** T8
- **4:15 S6:** demo with a live heal

## 3. New ADRs
0010 defender via `run_guarded(on_block=)` · 0011 safe swap via `create_cart` · 0012 red-team events (`stage` vocabulary + bus/SSE) · 0013 C6 results alignment + `latest.json` · 0014 eval systems via `shopper_loop`/`run_guarded`, fail-closed = block · 0015 live Shop only · 0016 stdlib percentiles + `importorskip`.

## 4. Adish-only actions
1. `python -m pip install --user "google-genai==3.6.1"`, then run `python scripts/check_decisions.py`. If the Decisions API is down, set `FIREWALL_BACKEND=json_llm` before 2:30.
2. Post asks A1, A2, A3 and ADRs 0010–0016 for OKs by 1:00.
3. Props by 1:35: `eval/props/sticky_01..06.jpg`, `voice_*.wav` (6 coercion + 5 casual; Windows `System.Speech` TTS is OK), `blurry_*.jpg` ×5.
4. Agree the victim model with the team: hydrogen takes 15–45 s per run, flash-lite 6–10 s. This decides whether 150 runs fit before 2:55.
5. Run the 2:30 freeze; make the 3:45 go/no-go on Managed Agents.

## 5. Critical path and cut list
- **Critical path:** genai 3.6.1 → T1 + T4 + T5 → props by 1:35 → T6 build → 2:10 dry run → **2:30 freeze and full run** → T9 by 3:15.
- **Cut, in order:**
  1. Managed Agents → local/recorded attacker
  2. Mutation rounds 3 → 1
  3. Neon text → template reason
  4. Hardened system
  5. Missing audio → TTS, else explicit error rows
  6. Holdout 10 → 5
  7. No live bypass by 3:50 → heal on the recorded golden bypass (the heal itself is live)
  8. Runner extras
  9. Frontend extras
