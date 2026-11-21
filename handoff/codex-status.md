- Implemented `eval/metrics.py` and `tests/test_metrics.py` with Task 3 schema stubs for this checkout.
- Initial run failed on missing `eval.metrics`. `.venv\Scripts\python -m pytest -q tests/test_metrics.py` then reported `22 passed in 1.00s`.
- Commit pending with the orchestrator on `m4-codex` as `feat(eval): metrics + tests`, per the lane contract.

### A2 eval runner

- Added `eval/run_eval.py`, `eval/runner/{systems,storage}.py` and `tests/test_run_eval.py`. Each completed system/case pair is flushed and synced to its JSONL checkpoint. Reports retain error rows and reasons, and aggregate the successfully scored cases.
- Initial pytest output was `6 failed, 2 warnings in 0.92s` with the runner missing. Final verification with `.venv\Scripts\python -m pytest -q tests/test_run_eval.py -p no:cacheprovider -o asyncio_default_fixture_loop_scope=function` returned `8 passed in 1.39s`. The full suite returned `42 passed, 1 warning in 2.25s` (Starlette test-client deprecation).
- The five-case CLI smoke used offline Shop and shopper fixtures. The shared schema, config and shopper implementations are still absent here. The runner validates against `eval.metrics.Metrics`, checks shared `backend.schemas.Metrics` when available, and labels the fixed C7 fake in `meta.adapters`. Real integration and the S4/S5 freeze-hash comparison remain pending. Claude owns the commit on `m4-codex`.

### A1 self-healing firewall

1. Proposal uses the guarded approval, claims, and probe results to identify a likely missed stage. Neon returns a structured candidate under a ten-second deadline.
2. The defender assigns the threshold and provenance. Local checks reject compound questions, name collisions, and normalized question similarity above 0.90.
3. Validation scores the recorded miss and at least five benign controls with four concurrent workers and reports each probability, latency, and outcome.
4. Publication requires the miss to reach threshold and every control to stay below it. Missing scores and scoring errors prevent publication.
5. The C4-compatible writer locks across processes, preserves the previous file bytes in `rules.json.bak`, and publishes a single version increment with `os.replace`. Retries reuse the stored version.
6. The launcher audits up to three fixed decision snapshots. It reads the last manifest line and checks the same proposed call against the published rules before reporting a reblock.
7. Events use the shared trace envelope, with the step in `data.step`. The replay test round-trips JSONL in order. The current route uses an in-memory bus, so UI persistence still needs integration.
8. The runner accepts fixed recordings and sends verdicts to the trace bus. Managed/local Carbon generation, attacker feedback, artifact transfer, and live C7 execution are outside this implementation.
9. Shared schemas, config, firewall dependencies, golden recordings, and the Gemini SDK were unavailable here. Tests used fakes and temporary rule files. The live heal and UI demo remain unverified.
10. Initial focused run stopped with two missing-module errors. Final focused output was `22 passed in 1.06s` and full-suite output was `79 passed, 1 warning in 2.41s`. Claude owns the commit on `m4-codex`.

### A1 follow-up on recorded firewall decisions
- The launcher still evaluates fixed snapshots, up to three per run.
- A validated rule emits `probe_published` with its version before the verification verdict.
- Verification reruns the same proposed call and reports `reblocked` only when the new probe fires and the firewall stops the call.
- A completed verification can report false. An unavailable verdict still ends the run with an error.
- `record_round` appends replay envelopes in order and saves only approved status fields. Raw model text and tool arguments stay out of the recording.
- Local and managed attack generation, probe-guided mutation, artifact rendering and their integration tests were omitted.
- Test-first loop output was `4 failed, 5 passed in 1.01s`. Final loop and self-heal output was `25 passed in 0.94s`.
- Full suite output was `7 failed, 304 passed, 11 deselected in 10.00s`. The failing table tests need eval/genprops/product_types.json and variants.json, outside this lane.
- Live checks remain for Neon proposal, validation against golden controls, rule publication, and UI replay. This checkout had no eval/golden directory or demo recording at inspection.
