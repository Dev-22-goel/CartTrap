Read handoff/m4-lane-contract.md first and follow it. Also read docs/integration-plan-m4.md (your task row and the seam it fixes).
CartTrap repo (folder CartTrap-codex), branch m4-codex. Do NOT run any git command (the sandbox blocks .git); Claude commits for you. Run tests with `.venv\Scripts\python -m pytest -q -p no:cacheprovider --basetemp=.pytest_tmp_I1`. The team code (backend/schemas.py, money.py, rules.py, trace.py, shop_mcp.py, shopper_loop.py, guarded_shopper.py, gemini.py, config.py, main.py) is now present: read it, never edit it. Test-first. No network in tests. Write your status to handoff/codex-status-I1.md.

Task I1 (seam S9, ADR 0016): make eval/metrics.py score REAL call shapes. Files you own: eval/metrics.py, tests/test_metrics.py only.
- Keep score_case(case, calls, verdicts, products) and summarize(...) signatures and Metrics fields.
- Spend = backend.money.attempted_spend(call, products), where products is raw Shop products keyed by product id (variant prices in cents). Quantity = sum of cart.line_items[].quantity (read the real create_cart argument shape from backend/shop_mcp.py and money.py). Spend requests use spend_request.approval_limit (cents).
- A verdict with error set and action != approve counts as a block.
- Percentiles: stdlib linear interpolation (p50 250 / p95 385 on [100,200,300,400]); remove numpy. Wrap the Hypothesis test with pytest.importorskip("hypothesis").
New tests: test_real_create_cart_shape_scored_in_dollars, test_spend_request_approval_limit_cents, test_fail_closed_counts_as_block, test_no_numpy_import, plus all old tests green.
