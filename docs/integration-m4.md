# CartTrap Integration Plan: Member 4 changes

> For Members 1–3. This lists only what Member 4 (Adish) changes that touches **your** files, contracts or checkpoints. Everything else in `plans/integration.md` stays as it is. Each change has an ADR in `docs/decisions/m4/` with the full reasoning and a verification checklist.
> Status: **proposed**. Please reply in the team channel with OK or objections before S1 (11:00).

## 1. What each teammate needs to know

### Member 1 (integration lead)
| Change | What you do | When | ADR |
|---|---|---|---|
| Member 4's routes move to `backend/m4_routes.py` | Add 2 lines to `backend/main.py`: `from backend.m4_routes import m4_router` and `app.include_router(m4_router)` | Once, before S2 (1:00 PM) | [0001](decisions/m4/0001-put-m4-routes-in-own-router.md) |
| Results JSON gains an additive `meta` block (`case_dir_hash`, `git_sha`, …) | Nothing required. Optional: assert `meta.case_dir_hash` in `test_eval_smoke.py` | S4 | [0004](decisions/m4/0004-prove-eval-freeze-with-case-hash.md) |
| Shopify rules: `create_cart` / `create_checkout` need `shop` (the offer's `seller.domain`); `create_checkout` takes line items, not a cart ID | Make `ShopMCP.create_cart(shop, lines)` and `ShopMCP.create_checkout(shop, lines)` match the real tools | Task 2, by C2 (11:45) | [0008](decisions/m4/0008-follow-shopify-challenge-rules.md) |
| Member 4 needs `hypothesis`, `pytest-asyncio`, `numpy`, `vcrpy` in the test requirements | Add 4 lines during Task 1 | 10:30–11:00 | [0007](decisions/m4/0007-add-m4-test-dependencies.md) |
| Member 4 uses Codex in a separate folder | Nothing. You still merge one `adish` branch | — | [0005](decisions/m4/0005-run-codex-in-separate-folder.md) |

### Member 2 (firewall)
| Change | What you do | When | ADR |
|---|---|---|---|
| Defender call site in `guarded_shopper.py` | You add the ~10-line call (`safe_swap` → `build_fraud_card` → emit `fraud_card`) on non-approve. Member 4 sends the exact snippet at S2. If you're swamped at S3, Member 4 adds it with your OK | S2 → before S3 | [0002](decisions/m4/0002-defender-call-site-in-guarded-shopper.md) |
| `RuleStore.append` (C4) needs to be safe for self-heal | Atomic write (temp + `os.replace`), `version` +1, keep `rules.json.bak`, ignore duplicate probe names. Or let Member 4 wrap it and just review | C4 at 11:45 | [0003](decisions/m4/0003-make-self-heal-p0-in-own-module.md) |
| T15 fix (unchanged from plan) | Member 4 sends a written probe/threshold change; you apply it to `rules.json` | 2:50–3:05 PM | (recorded as a new ADR at T15) |

### Member 3 (frontend + demo)
| Change | What you do | When | ADR |
|---|---|---|---|
| Results JSON gains a `meta` block | Nothing required. Optional: show the short `case_dir_hash` on the scoreboard as "frozen set" proof | 2:00 | [0004](decisions/m4/0004-prove-eval-freeze-with-case-hash.md) |
| Self-heal is now P0 | The "red-team" demo segment always includes a live heal. At S6 "switch red-team button to replay" now replays only the attacker, and the heal still runs | S6 | [0003](decisions/m4/0003-make-self-heal-p0-in-own-module.md) |
| Shopify rules: no re-hosted merchant images; judges must be able to buy | `forge()` writes composites to git-ignored `redteam/out/`. The Fraud Card's "Buy the safe one" button opens `safe_swap`'s `continue_url` exactly as returned | 11:45 / S3 | [0008](decisions/m4/0008-follow-shopify-challenge-rules.md) |
| `forge()` (C5) | Unchanged. Member 4 imports `redteam/forge/` and never edits it | 11:45 | — |

## 2. Contract table: only the rows that change
| ID | Contract | Change |
|---|---|---|
| C4 | `RuleStore` | Adds atomic-write + versioning guarantees on `append` (ADR 0003) |
| C6 | `Metrics` JSON + `GET /api/eval/latest` | Same shape plus an additive `meta` block; route served from `backend/m4_routes.py` (ADRs 0001, 0004) |
| C9 (new) | Defender interface | `build_fraud_card`, `safe_swap`, `dollars_defended` in `backend/defender_neon.py`, Member 4 → Member 2, by S2 (ADR 0002) |

## 3. Member 4 file ownership (updated)
Member 4 lane (Claude): `backend/defender_neon.py`, `backend/prompts/neon_fraud_card.md`, `tests/test_defender.py`, `eval/build_cases.py`, `eval/cases/**`, `eval/holdout/**`, `eval/golden/**`, `redteam/sandbox/**`, `docs/failure-analysis.md`, `docs/decisions/m4/**`

Member 4 lane (Codex, merged into `adish`): `eval/metrics.py`, `tests/test_metrics.py`, `eval/run_eval.py`, `eval/runner/**`, `tests/test_run_eval.py`, `backend/m4_routes.py`, `backend/replay.py`, `tests/test_m4_routes.py`, `eval/results/sample.json`, `backend/selfheal.py`, `backend/redteam_carbon.py`, `tests/test_selfheal.py`, `tests/test_redteam_loop.py`

Not touched by Member 4: `backend/main.py` (M1), `backend/guarded_shopper.py` except as ADR 0002 allows (M2), `backend/schemas.py` (M2), `rules.json` (M2), `redteam/forge/**` (M3).

## 4. Checkpoint changes
| Checkpoint | Change |
|---|---|
| S2 (1:00) | Member 4 posts the C9 snippet for Member 2 and the C6 sample. Member 1 confirms the `include_router` line is in |
| S4 (2:30) | Member 4 posts the frozen `case_dir_hash` in the channel |
| S5 (3:15) | Re-run must show the same hash |
| S6 (4:15) | Demo includes a live self-heal (attacker may be replayed) |
