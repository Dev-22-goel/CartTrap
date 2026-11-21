# EV handoff

**Blocked at event delivery.** Image, video and audio localization, artifact serving, and the defender hook are implemented. The real TraceBus rejects the new event before it reaches SSE. Member 2 or an explicitly authorized EV edit must add `"evidence"` to `TraceEvent.kind` in `backend/schemas.py`. That file is outside the EV lane, and approval was requested. The integration test is active and reproduces the issue.

The frontend contract, including crop coordinates and half-open waveform segment indexes, is in [ADR 0025](../docs/decisions/m4/0025-live-evidence.md). Per-file localization accepts a null result for a clean attachment in a mixed batch. All verification used local files and offline model doubles.

## Verification output

```text
.venv\Scripts\python -m pytest -q -p no:cacheprovider --basetemp=.pytest_tmp_EV
FAILED tests/test_evidence.py::test_on_block_streams_evidence_while_swap_pending
1 failed, 379 passed, 13 deselected in 9.44s
```

The failing test received the template fraud card and then timed out waiting for evidence while the safe swap was held open. The captured defender log reported `evidence event unavailable: ValidationError`. The other eight EV tests passed. A separate smoke check used the installed ffmpeg with synthetic color bars. Its output was `ffmpeg frame at 1.2 s: JPEG, 160x90`.

Live Gemini localization accuracy and the frontend rendering were outside this offline backend check. Claude owns the commit.
