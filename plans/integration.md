# CartTrap Integration Plan

> How the four member plans fit together: one shared timeline, the contracts each person hands to the others, sync checkpoints, merge rules and the end-to-end tests that prove the pieces work together. Source of truth for tasks stays `plan.md`; this file only coordinates them.
> Owner: **Member 1 (integration lead)**. Everyone reads Global Constraints and Review Focus in `plan.md` / `member-1.md`.

## 1. Who owns what
| Member | Track | Tasks |
|---|---|---|
| Member 1 | Commerce + integration lead | 1, 2, 4, 5 · runs merges, `make integration`, fixture recording |
| Member 2 | Firewall | 3, 6, 7, 8, 9 |
| Member 3 | Frontend + demo | 11, 12, 13, 17, P1 extras |
| Member 4 | Defender + eval | 10, 14, 15, 16 |

## 2. Coinciding timeline (everyone's work, side by side)

| Time | Member 1 | Member 2 | Member 3 | Member 4 | Sync |
|---|---|---|---|---|---|
| 10:00 | read resource sheet | read resource sheet | read resource sheet | read resource sheet | model IDs into `config.py` |
| 10:30–11:00 | T1 scaffold + config | **T3 schemas** (C1) | T13 forge (offline, sample image) | golden images + 6 prop photos; draft `metrics.py` tests | |
| 11:00 | | | | | **S1 Contract freeze (5 min)** |
| 11:00–11:45 | T2 Shop MCP client (C2) | T6 rules store (C4) | T13 forge done (C5) → T11 start | T14 `metrics.py` (pure, TDD) | |
| 11:45–12:30 | T4 trace bus + API (C3) | T7 firewall + gate | T11 arena on fixture stream | T14 `build_cases.py` (uses C2 fixtures + C5) | |
| 12:30–1:00 | T5 victim + `shopper_loop` (C8) | T8 Argon → T9 guarded (needs C8) | T11 wire to live API | T16 sandbox `AGENTS.md` + attack skill | |
| 1:00 | | | | | **S2 Walking skeleton** |
| 1:00–2:00 | record demo fixtures; help T9 wiring | T9 done; tune on golden | T12 seismograph, fraud card | **T10 defender** (needs T9) | |
| 2:00 | | | | | **S3 Real E2E** |
| 2:00–2:30 | `make integration` green; eval live runs support | gate tuning on golden only | T12 scoreboard (needs C6) | T14 full dry run | |
| 2:30 | | | | | **S4 Eval freeze** |
| 2:30–3:15 | Managed Agents setup with M4 | **T15 fix** (with M4) | P1 extras / polish | **T15** failure analysis | |
| 3:15 | | | | | **S5 Fix review** |
| 3:15–4:15 | offline fallback (`USE_FIXTURES=1`) | P1 US-10 or support | T17 demo-check script | T16 self-heal + record trace | |
| 4:15 | | | | | **S6 UI freeze + full demo run** |
| 4:15–4:45 | merge, tag | bugfix only | T17 README | bugfix only; numbers into README | |
| 4:45 | | | | | **S7 Code freeze, record video** |
| 5:00 | submit | | | | |

## 3. Contracts (hand-offs)
Until a contract lands, the consumer works against the stub named here. A contract changes only with the producer's OK and a message to everyone.

| ID | Contract | Producer → consumers | Due | Stub until then |
|---|---|---|---|---|
| C1 | `backend/schemas.py` (Intent, Claims, ToolCall, Probe, ProbeResult, Verdict, FraudCard, TraceEvent, Media) + `intent.py` + `money.py` | M2 → all | 11:00 | copy of plan.md Task 3 Interfaces |
| C2 | `ShopMCP` class + `fixtures/shop/tools_list.json` + recorded fixtures for 10 demo SKUs | M1 → M2, M4 | 11:45 | `USE_FIXTURES=1` with hand-made JSON |
| C3 | `/api/run`, SSE stream, `frontend/src/fixtures/run_attack.jsonl` | M1 → M3 | 12:30 (fixture file by 11:30) | M3 hand-writes events from TraceEvent schema |
| C4 | `rules.json` + `RuleStore` | M2 → M3 (probe names), M4 (self-heal) | 11:45 | 5-probe sample file |
| C5 | `forge()` + `ManifestEntry` | M3 → M4 | 11:45 | M4 uses golden images |
| C6 | `Metrics` JSON + `GET /api/eval/latest` | M4 → M3 | 2:00 | sample results JSON committed by M4 at 1:00 |
| C7 | `run_guarded()` → `GuardedResult` | M2 → M4 (T10, T14), M1 (API wiring) | 1:00 | fake returning a fixed hard_block |
| C8 | `shopper_loop(...)` in `backend/shopper_loop.py` | M1 → M2 | 12:45 | M2 writes T9 against the signature |

## 4. Sync checkpoints (5 minutes each, standing)
| ID | Time | Pass criteria | If it fails |
|---|---|---|---|
| S1 | 11:00 | C1 merged; model IDs confirmed; firewall backend chosen (`decisions` or `json_llm`) | M2 finishes C1 before anything else; others keep using stubs |
| S2 | 1:00 | `curl -N` sticky-note run shows victim `intercepted` + guarded `verdict`; UI renders both panes | cut video input; M1 pairs with whoever is blocking |
| S3 | 2:00 | `make integration` green (attack + benign E2E); fraud card visible in UI | drop US-8 live, plan replay |
| S4 | 2:30 | `eval/cases/` frozen and committed; 3-system results file exists | run 2 systems only (cut list #4) |
| S5 | 3:15 | failure analysis written with before/after numbers | ship with the before numbers + honest note |
| S6 | 4:15 | full 3-minute demo passes once on venue light; offline fallback passes | switch red-team button to replay |
| S7 | 4:45 | `main` tagged `v1-demo`; README numbers match latest results file | no new features, video only |

## 5. Branches and merges
- Branch per member: `m1-commerce`, `m2-firewall`, `m3-arena`, `m4-eval`. Small commits, follow each task's commit step.
- Merge to `main` at S1, S2, S3, S4, S6 (Member 1 merges; conflicts resolved by the file's owner). In between, merge anyway as soon as a contract lands.
- `backend/main.py` and `Makefile` belong to Member 1; others send route/target changes to M1 or keep them in their own module.
- `backend/schemas.py` belongs to Member 2; additive fields only after S1.
- Never commit `.env`, `runs/`, or webcam media.

## 6. Integration tests (Member 1 owns, `make integration`)
| Test | Proves | Needed by |
|---|---|---|
| `tests/integration/test_e2e_attack.py` | sticky-note golden + "buy one pack under $25" → victim `intercepted` (qty > 1 or spend request), guarded `hard_block_quarantine`, a `fraud_card` with `dollars_defended > 0`, stream ends `done` | S3 |
| `tests/integration/test_e2e_benign.py` | promo-banner golden, $20 cart → guarded `approve_checkout`, no fraud card | S3 |
| `tests/integration/test_contracts.py` | fixture `run_attack.jsonl` validates against `TraceEvent`; results JSON validates against `Metrics`; `rules.json` loads | S2 |
| `tests/integration/test_eval_smoke.py` | `run_eval.py --limit 5 --systems baseline,carttrap` exits 0 and writes a results file | S4 |
| `frontend` replay check | Playwright loads the arena, replays a recorded live stream, screenshot shows both panes + fraud card | S6 |
| `make demo-check` (Task 17) | demo path online and with `USE_FIXTURES=1` | S6 |

## 7. Communication
- One shared channel; post "C# landed" with the commit hash when a contract merges.
- Blocked more than 15 minutes → say so at once; M1 reassigns or stubs.
- Any change to Global Constraints needs all four to agree.
