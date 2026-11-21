# Codex I2 status

Implemented the defender hook and safe swap for seams S3–S6 in `backend/defender_neon.py`, `backend/prompts/neon_fraud_card.md`, and `tests/test_defender.py`.

- `on_block(BlockContext)` runs the safe swap and fraud-card build under one 10-second deadline, then emits the card on the guarded TraceBus. Failures return `None` and log only the exception type. Neon retains its 8-second timeout and template fallback.
- Safe swap uses the original product and search matches, reusing the run's known variants for those products. If none of those variants qualify, it makes at most three detail lookups for products missing variants. It creates the cart through `ShopMCP.create_cart`, uses the returned total in dollars when available, and passes the full `continue_url` through unchanged. The cart includes product and variant IDs, titles, and dollar prices for the UI.
- Neon uses `gemini.client()` with `config.MODELS["defender"]`. The fraud card uses numeric dollar prices, and the template renders them with two decimal places. The self-heal re-exports were preserved.

## Offline verification

The test-first run produced `10 failed, 14 passed in 1.69s`. The failures covered the old cart payload and lookups, cents in the card, the separate Gemini client, and the missing hook.

```text
.venv\Scripts\python -m pytest -q -p no:cacheprovider --basetemp=.pytest_tmp_I2 tests/test_defender.py
........................                                                 [100%]
24 passed in 1.35s

.venv\Scripts\python -m pytest -q -p no:cacheprovider --basetemp=.pytest_tmp_I2
298 passed, 11 deselected in 37.25s
```

The requested search for `httpx|requests|urllib|os\.environ` in `backend/defender_neon.py` returned no matches. The Shop MCP test uses the real client with `httpx.MockTransport` and verifies the cart request, total, and checkout URL including query parameters. The TraceBus test uses the real `BlockContext` and `TraceBus`. No live checkout or Gemini test ran.

The sandbox blocked recursive cleanup of the generated `.pytest_tmp_I2` directory. It is test output and should be excluded from the commit.

## Integration handoff

Member 1 still needs to pass `on_block=defender_on_block` into `run_guarded` in `backend/main.py`, as specified by the integration plan. The checkout lacks the standalone ADR 0010 and 0011 files, so I followed the I2 brief and integration plan's S3 and S4 decisions. The lane's merge-point spec verifier remains a separate check.
