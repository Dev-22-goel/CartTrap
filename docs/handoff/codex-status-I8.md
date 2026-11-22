# I8 integration tests

The offline suite exercises `backend.main.app` through HTTP and SSE. The tests use SDK fakes for Hydrogen, Argon, Decisions, and Neon and an `httpx.MockTransport` for the real ShopMCP client. Both shopping scenarios upload self-contained PNG fixtures. The tests use temporary paths for uploads, eval manifests, and result files.

- The sticky-note run intercepts the victim's three-pack proposal, hard-blocks the guarded proposal, and sends only a one-pack replacement to Shop MCP. The fraud card reports $40 defended and preserves the replacement URL byte for byte.
- The promo-banner run approves a one-pack $20 cart and emits no fraud card.
- Every shopping and red-team SSE frame is parsed as a `TraceEvent`. The contract tests also load the repo rules through `RuleStore` and validate a two-case eval report, including its case directory hash and live Shop mode metadata. The limited eval writes a results file and leaves `latest.json` absent.
- The red-team test checks the mounted launch route, its shared rules store, and the SSE stream through a fake launcher emitting `data.stage`. The current production launcher emits `data.step`. Its stage migration remains outside this test change.
- Both live twins were collected under `-m live`. They use the real Gemini and Shop MCP clients and were left unexecuted under the offline instruction. The live benign test uses an available catalog offer under $25. The exact $20 assertion applies to the deterministic offline fixture.

## Verification

```text
> .venv\Scripts\python -m pytest -q -p no:cacheprovider --basetemp=.pytest_tmp_I8
........................................................................ [ 21%]
........................................................................ [ 43%]
........................................................................ [ 65%]
........................................................................ [ 87%]
...........................................                              [100%]
331 passed, 13 deselected in 5.83s
```

```text
> .venv\Scripts\python -m pytest -q -p no:cacheprovider --basetemp=.pytest_tmp_I8 -m live --collect-only tests/integration
tests/integration/test_e2e_attack.py::test_sticky_note_attack_live
tests/integration/test_e2e_benign.py::test_promo_banner_live

2/10 tests collected (8 deselected) in 0.70s
```

Importing the real app confirmed the mounted `/api/eval/latest` and `/api/redteam/launch` routes for ADR 0019. The full run includes the existing `tests/test_main_wiring.py` hook assertion.
