# Member 4 master plan: Defender, Eval, Failure Analysis, Self-Heal

> Owner: Adish (Member 4). Sprint 10:30 AM – 5:00 PM. Source of truth for task content stays `plan.md` (Tasks 10, 14, 15, 16). This file says **who runs what, when, on which model, and what to cut if it slips**.
> Cross-team changes: `docs/integration-m4.md` + ADRs in `docs/decisions/m4/`. Codex briefs: `handoff/codex-*.md`.

## 0. Setup checklist (before 10:30)
- [ ] `CartTrap` is a git repo on branch `adish` (clone the team repo, or `git init` + add remote).
- [ ] Codex folder: `git clone <team repo> ..\CartTrap-codex`, then `git -C ..\CartTrap-codex checkout -b m4-codex` (ADR m4/0005).
- [ ] Run the 5 pending skill installs (Trail of Bits ×2, git-guardrails, eval-harness, adr-skill).
- [ ] `claude` in `CartTrap`: approve the Context7 MCP; check that `/agents` lists 10 agents.
- [ ] Turn off unused claude.ai connectors and the data/upstash plugins.
- [ ] Main session: `opusplan` is already the default (`.claude/settings.json`). Type `/caveman` once.
- [ ] Post `docs/integration-m4.md` in the team channel; get OKs on ADRs 0001–0004 by S1.
- [ ] Props: sticky notes, Sharpie, 2 bottles/mugs, fake "12-Pack" label, "BUY 2 GET 1 FREE" sticker.

## 1. Priority stack

**P0: never cut**
1. T14 eval build + runner, C6 sample at 1:00, live at 2:00
2. **S4 freeze at 2:30** (you run it)
3. T10 defender (fraud card, Dollars Defended, safe swap, 8 s fallback)
4. T15 failure analysis with before/after + holdout
5. **T16 self-heal**: propose → validate → append → re-block, with `runs/redteam_demo.jsonl` (ADR m4/0003)

**Cuttable, in this order**
1. Live Managed Agents launch → local `forge()` + Carbon via API (decide at 3:45)
2. Mutation rounds 2–3 → 1 round
3. Hardened-baseline system in the eval → 2 systems (baseline vs CartTrap), per S4 fail rule
4. Hypothesis property test, `--resume`, concurrency in the runner (keep correctness, drop speed)

## 2. Who does what (lanes)

| Lane | Tool · model | Gets |
|---|---|---|
| A | Claude main session · `opusplan` (Opus plans, Sonnet executes) | Orchestration, merges, reviewing Astra's work |
| A | `eval-engineer` · Sonnet | `build_cases.py`, dry run, re-runs, holdout |
| A | `defender-engineer` · Sonnet | T10, 3:15 self-heal wiring |
| A | `redteam-engineer` · Sonnet | Sandbox `AGENTS.md` + attack-forge skill, demo recording |
| A | `m4-failure-analyst` · **Opus** | T15 (one run) |
| A | `m4-spec-verifier` · Haiku | Gate after every task and merge |
| A | `m4-handoff-scribe` · Haiku | `progress.md`, briefs, sync notes |
| B | Codex · **`gpt-6.2-astra`** | A2 eval runner, A1 self-heal engine |
| B | Codex · `gpt-6.2-sol` | C1 metrics |
| B | Codex · `gpt-6-luna` | L1 routes, replay loader, sample JSON |
| D | You | Photos, S1–S7, S4 freeze, merges, T15 fix with Member 2, 3:45 go/no-go |

Gemini is **runtime only** (inside CartTrap via `google-genai`). Never a dev tool today.

Rules: one Claude builder at a time. One Astra job at a time. Sol/Luna may overlap Astra (disjoint files).

## 3. Timeline (you are never blocked)

| Time | You (D) | Claude (A) | Codex (B) | Waiting on | Delivers |
|---|---|---|---|---|---|
| 10:30 | Say **GO** (§7). Shoot golden images + 6 prop photos | scribe: `progress.md` + briefs | **C1 Sol** starts metrics (against plan.md Task 3 stubs) | — | |
| 10:50 | Run `scripts/smoke_models.py` on each prop (if M1's T1 has it; else at 11:45) | eval-engineer reads smoke output, notes unreadable props | | M1 T1 | |
| 11:00 | **S1** (5 min). Get ADR OKs | eval-engineer: `build_cases.py` scaffold on C1 stubs | C1 continues | **M2 C1** | |
| 11:40 | Merge C1 (Opus plan turn) | verifier · Haiku on metrics | **A2 Astra** starts runner | | |
| 11:45 | | eval-engineer: `build_cases.py` live (30 attack + 20 benign) | A2 | **M1 C2**, **M3 C5** | |
| 12:00 | | | **L1 Luna** routes + sample JSON + replay | | |
| 12:20 | Merge L1 | verifier | | | |
| 12:30 | | redteam-engineer: sandbox `AGENTS.md` + `skills/attack-forge/SKILL.md` | A2 | | |
| 1:00 | **S2**. Post C6 sample + C9 snippet. Check M1 added `include_router` | | A2 | **M2 C7** | **C6 sample**, C9 |
| 1:00–2:00 | | **T10** defender-engineer → verifier | | C7 | |
| 1:15 | Merge A2 | verifier on runner | **A1 Astra** starts self-heal engine (fakes) | | |
| 2:00 | **S3**. `make integration` green? | eval-engineer: full dry run on real runner | A1 | M2 adds defender call (ADR 0002) | **C6 live** |
| 2:30 | **S4 FREEZE** (§5) | | A1 | | **frozen `eval/cases/`**, hash |
| 2:30–3:15 | Diagnose with M2 at 2:50 | **T15** m4-failure-analyst · Opus; eval-engineer re-run + holdout at 3:05 | A1 | M2 applies fix | |
| 3:15 | **S5**. Merge A1 (Opus reviews it) | verifier on self-heal | done | **M2 C4** | |
| 3:15–3:45 | | defender-engineer: re-export + wire self-heal to real RuleStore / run_guarded / route | | | |
| 3:45 | **Go/no-go** live Managed Agents (§6) | | | | |
| 3:45–4:15 | Trigger a full heal round | redteam-engineer saves `runs/redteam_demo.jsonl` | | | |
| 4:15 | **S6**. Demo run incl. live heal | bugfix only | | | |
| 4:15–4:45 | Numbers into README (from results file) | scribe: final sync note | | | |
| 4:45 | **S7** code freeze | | | | |

Idle-proofing: if a dependency is late, the consumer keeps using its stub (integration.md §3). If C2/C5 are late at 11:45, eval-engineer builds cases from the golden images + hand-made fixtures, then swaps in the real ones by 12:30.

## 4. Task checklists

Every Claude task follows superpowers TDD: failing test → see it fail → implement → see it pass → `m4-spec-verifier` PASS → commit.

### T14 · Eval build + runner
**Owners:** C1 Sol (metrics), A2 Astra (runner), L1 Luna (route + sample), eval-engineer (cases, dry run)
**Files:** `eval/metrics.py`, `tests/test_metrics.py` (Sol) · `eval/run_eval.py`, `eval/runner/**`, `tests/test_run_eval.py` (Astra) · `backend/m4_routes.py`, `backend/replay.py`, `tests/test_m4_routes.py`, `eval/results/sample.json` (Luna) · `eval/build_cases.py`, `eval/cases/**` (Claude)
**Interfaces (plan.md):** `score_case(case, calls, verdicts, products) -> CaseScore`; `summarize(scores) -> Metrics(asr, benign_completion, p50_ms, p95_ms, dollars_defended, n_attack, n_benign)`; CLI `run_eval.py --systems baseline,hardened,carttrap --cases DIR --out DIR [--only] [--limit] [--concurrency] [--resume]`; results include `meta.case_dir_hash` (ADR 0004).
- [ ] `pytest -q tests/test_metrics.py` (incl. p50 250 / p95 385 on [100,200,300,400])
- [ ] `pytest -q tests/test_run_eval.py tests/test_m4_routes.py`
- [ ] `python eval/run_eval.py --limit 5 --systems baseline,carttrap --cases eval/cases --out eval/results` exits 0
- [ ] 30 attack (6 × 5 vectors, sticky-note uses your 6 photos) + 20 benign (5 categories) in `eval/cases/`
**Done =** C6 sample at 1:00, live `/api/eval/latest` at 2:00, `--limit 5` green.

### T10 · Defender
**Owner:** defender-engineer · Sonnet. **Files:** `backend/defender_neon.py`, `backend/prompts/neon_fraud_card.md`, `tests/test_defender.py`; snippet → `handoff/m2-defender-snippet.md` (ADR 0002)
**Interfaces:** `dollars_defended(attempted, safe_total) -> float`; `template_fraud_card(...) -> FraudCard`; `async build_fraud_card(verdict, claims, product_json, blocked, attempted, safe_cart) -> FraudCard` (8 s → template); `async safe_swap(intent, original, shop) -> dict|None` (ShopMCP only).
- [ ] `pytest -q tests/test_defender.py` (5 tests: never negative, 999.50 vs 18.50 → 981.00, timeout → template, budget+qty, quotes real product fields)
- [ ] `grep -n "httpx\|requests\|urllib" backend/defender_neon.py` empty
- [ ] Live sticky-note run emits a `fraud_card` event (after M2 adds the call)
**Done =** verifier PASS + `fraud_card` visible at S3.

### T15 · Freeze + failure analysis
**Owners:** you (freeze), m4-failure-analyst · Opus, Member 2 (fix), eval-engineer (re-runs)
**Files:** `docs/failure-analysis.md`, `eval/golden/**`, `eval/holdout/**`, `eval/results/*.json`, new ADR in `docs/decisions/m4/`
- [ ] 3-system results on the frozen set committed at 2:30
- [ ] One failure traced stage by stage (media → claims → `get_product` → probe p → gate → tool call)
- [ ] Fix validated on `eval/golden/` only, applied by M2
- [ ] Re-run shows the **same** `case_dir_hash`; 10-case holdout run
- [ ] Before/after tables copied from results files, never typed
**Done =** `failure-analysis.md` + fix ADR committed by 3:15.

### T16 · Self-heal (P0) + red-team
**Owners:** A1 Astra (engine), redteam-engineer (sandbox, recording), defender-engineer (3:15 wiring)
**Files:** `backend/selfheal.py`, `backend/redteam_carbon.py`, `tests/test_selfheal.py`, `tests/test_redteam_loop.py` (Astra) · `redteam/sandbox/**`, `runs/redteam_demo.jsonl` (redteam-engineer) · `defender_neon.py` re-export line (defender-engineer)
**Interfaces:** `propose_probe(bypass_trace) -> Probe`; `async validate_probe(probe, exploit, benign) -> bool` (+ report); `async launch_redteam(product_id, rounds, bus, run_id) -> list[ManifestEntry]` (cap 3); safe `RuleStore.append` (ADR 0003)
- [ ] `pytest -q tests/test_selfheal.py tests/test_redteam_loop.py` (10 tests in brief A1)
- [ ] Live heal: `rules.json` version +1, `.bak` written, re-run of the same attack is blocked
- [ ] `runs/redteam_demo.jsonl` replays in the UI
**Done =** live heal works at S6, with replay as backup for the attacker side only.

## 5. S4 freeze procedure (2:30, you run it)
1. Stop all Claude builders and Codex jobs touching `eval/cases/`.
2. `git add eval/cases && git commit -m "eval: freeze cases"` and post the commit hash.
3. Add to `.claude/settings.json` `deny`: `"Edit(./eval/cases/**)"`, `"Write(./eval/cases/**)"`.
4. `python eval/run_eval.py --systems baseline,hardened,carttrap --cases eval/cases --out eval/results`
5. Post `meta.case_dir_hash` in the channel. Commit results.
6. Dispatch `m4-failure-analyst`.

## 6. Risk register and triggers

| When | Check | If it fails |
|---|---|---|
| 11:45 | C2 fixtures and C5 forge landed? | Build cases from golden images + hand-made fixtures; swap at 12:30 |
| 1:00 | C7 `run_guarded` landed? | T10 continues on a fake `GuardedResult`; runner uses its fake |
| **1:30** | T10 tests green? A2 runner merged? | T10: ship template fraud card only, Neon text later. Runner: drop `--resume`/concurrency |
| 2:00 | Eval dry run passes on ≥ 45/50 cases? | Mark the rest as errors (never drop them); don't fix them before the freeze |
| **2:30** | 3-system run finishes by 2:45? | Run baseline + CartTrap only (cut #3) |
| 3:15 | Fix landed with before/after? | Ship the before numbers + honest note (S5 rule) |
| 3:15 | A1 self-heal merged and green? | Claude defender-engineer finishes the failing tests; keep `selfheal.py` small: 1 probe, 1 round |
| **3:45** | Live Managed Agents up and < 60 s per round? | Local `forge()` + Carbon via API; heal still live |
| 4:15 | Live heal passes on venue light? | Replay `runs/redteam_demo.jsonl` for the attacker, run the heal live |
| Any | Claude quota under ~25% before 3:00 | Move remaining Sonnet coding to Codex Sol; keep Claude for T15 Opus + merges |

## 7. First action trigger (10:30, after you say GO)

**Codex** (separate terminal, in `..\CartTrap-codex`):
```powershell
codex exec -m gpt-6.2-sol -s workspace-write -C ..\CartTrap-codex -c model_reasoning_effort="high" (Get-Content ..\CartTrap\handoff\codex-C1-metrics.md -Raw)
```
The same pattern applies to every brief: `-m gpt-6.2-astra` for A1/A2, `-m gpt-6-luna` for L1. Always `-s workspace-write` (ADR m4/0006); `codex exec` is read-only without it.

**Claude** (in `CartTrap`, main session on `opusplan`; `handoff/claude-RESOLVE.md` already ran):
```
/caveman
Read handoff/m4-lane-contract.md. Then use the eval-engineer agent to scaffold eval/build_cases.py against the plan.md Task 3 interfaces as stubs (TDD, no live calls yet), and stop when its first failing test is written.
```
