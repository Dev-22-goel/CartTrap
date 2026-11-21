- Implemented `eval/metrics.py` and `tests/test_metrics.py` with Task 3 schema stubs for this checkout.
- Initial run failed on missing `eval.metrics`. `.venv\Scripts\python -m pytest -q tests/test_metrics.py` then reported `22 passed in 1.00s`.
- Commit pending with the orchestrator on `m4-codex` as `feat(eval): metrics + tests`, per the lane contract.

### A2 eval runner

- Added `eval/run_eval.py`, `eval/runner/{systems,storage}.py` and `tests/test_run_eval.py`. Each completed system/case pair is flushed and synced to its JSONL checkpoint. Reports retain error rows and reasons, and aggregate the successfully scored cases.
- Initial pytest output was `6 failed, 2 warnings in 0.92s` with the runner missing. Final verification with `.venv\Scripts\python -m pytest -q tests/test_run_eval.py -p no:cacheprovider -o asyncio_default_fixture_loop_scope=function` returned `8 passed in 1.39s`. The full suite returned `42 passed, 1 warning in 2.25s` (Starlette test-client deprecation).
- The five-case CLI smoke used offline Shop and shopper fixtures. The shared schema, config and shopper implementations are still absent here. The runner validates against `eval.metrics.Metrics`, checks shared `backend.schemas.Metrics` when available, and labels the fixed C7 fake in `meta.adapters`. Real integration and the S4/S5 freeze-hash comparison remain pending. Claude owns the commit on `m4-codex`.
