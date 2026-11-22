Read handoff/m4-lane-contract.md first and follow it. It says which files you own and the rules you must follow.

CartTrap repo, branch m4-codex. Read AGENTS.md, plan.md Global Constraints + Task 14, integration.md contracts C6/C7, backend/schemas.py, eval/metrics.py.
Build eval/run_eval.py (+ helpers in eval/runner/), TDD:
CLI: run_eval.py --systems baseline,hardened,carttrap --cases DIR --out DIR [--only ids] [--limit N] [--concurrency 4] [--resume]
- Run cases concurrently with a bounded semaphore; per-case timeout 60 s; a timed-out or crashing case is recorded as an error, never dropped, never crashes the run.
- --resume skips cases already in a partial results file (append-only JSONL checkpoint, so a crash at case 40 loses nothing).
- Deterministic: sorted case order in the output, fixed seed, Shop responses replayed from fixtures (vcrpy-style record/replay keyed by request).
- Score each case with metrics.score_case, summarize per system, and write eval/results/<UTC timestamp>.json validated against the Metrics schema: per-system metrics, per-case scores, failures list with reasons, run metadata (git SHA, case-dir hash, model IDs from config.py).
- Case-dir hash lets S4 prove the frozen set didn't change.
- run_guarded (C7) may not exist yet: Protocol + fake.
Constraints: no complete_* or create_spend_request, ShopMCP only, no DB, no network in tests.
Tests: test_runner_records_timeout_as_error, test_resume_skips_done_cases, test_output_validates_against_metrics, test_case_dir_hash_changes_on_edit, test_limit_and_only_filters, test_cli_smoke (--limit 5 --systems baseline,carttrap exits 0).
Only edit: eval/run_eval.py, eval/runner/**, tests/test_run_eval.py, handoff/codex-status.md. Commit on m4-codex; never push to main.
