# Codex I1 status

I1 is complete. The scorer reads Shop MCP `cart.line_items` quantities and uses `backend.money.attempted_spend` for checked calls. The shared helper resolves catalog variants by ID and converts cart prices and spend-request approval limits from cents to dollars. Legacy cart fixtures still score, and benign completion still requires known catalog prices.

The scorer preserves the `score_case` and `summarize` signatures and all `Metrics` fields. Fail-closed non-approval verdicts count as blocks. The percentile calculation uses standard-library linear interpolation. Only the Hypothesis property test skips when Hypothesis is unavailable.

## Verification

- Before the implementation, the metrics suite reported `3 failed, 24 passed in 1.24s`. The nested cart, approval limit, and NumPy regressions failed as expected. The fail-closed cases already passed.
- After implementation, the metrics suite reported `27 passed in 1.11s`. It verifies p50 of 250 ms and p95 of 385 ms for the four reference samples.
- The first full run reported 10 failures in `tests/test_defender.py` involving the shared Gemini client, safe-swap behavior, fraud-card pricing, and `on_block`. The isolated defender rerun reported `24 passed in 1.32s`. The final full offline rerun passed:

  ```text
  .venv\Scripts\python -m pytest -q -p no:cacheprovider --basetemp=.pytest_tmp_I1
  298 passed, 11 deselected in 33.78s
  ```

- With NumPy and Hypothesis imports disabled, the metrics suite reported `26 passed, 1 skipped in 0.18s`. The skip was the Hypothesis property test.

The standalone ADR 0016 file was unavailable in this checkout. The implementation follows the S9 row in `docs/integration-plan-m4.md` and the I1 brief. Changes are confined to `eval/metrics.py`, `tests/test_metrics.py`, and this handoff.
