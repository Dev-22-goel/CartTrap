# Codex I3 status: routes on shared bus and store

Implemented the I3 route seam in `backend/m4_routes.py` and `backend/replay.py`, with coverage in `tests/test_m4_routes.py`.

- `/api/redteam/launch` now starts the app's shared `TraceBus`, schedules the red-team launcher as a background task, keeps a task reference, adapts Carbon events to `TraceBus.emit(run_id, pane, kind, data)`, and passes the app's rules store (falling back lazily to `backend.main.RULES`).
- Recorded demo traces replay into the bus under a fresh run ID, retain scaled `t_ms` gaps using `REPLAY_SPEED`, and end with `done`.
- `/api/eval/latest` prefers `latest.json`, then the newest non-sample JSON, then `sample.json`, and returns 404 when none exist.
- The tests verify the launcher response and bus events, replay completion, app rules store, and latest result preference.

Verification:

```text
.venv\Scripts\python -m pytest tests/test_m4_routes.py -q -p no:cacheprovider --basetemp=.pytest_tmp_I3
.........                                                                [100%]
9 passed in 1.34s
```

```text
.venv\Scripts\python -m pytest -q -p no:cacheprovider --basetemp=.pytest_tmp_I3
288 passed, 11 deselected, 10 failed in 15.40s
```

All 10 full-suite failures are in `tests/test_defender.py` and cover the independent defender implementation: shared Gemini explanation fallback, safe cart shape/product lookup, and absent `on_block`. No route tests failed. No network calls were made.

`docs/decisions/m4/0012-redteam-events.md` and `docs/decisions/m4/0013-eval-results.md` were referenced by the I3 brief but were not present in this checkout; I followed their requirements as summarized in `docs/integration-plan-m4.md` and the I3 brief.
