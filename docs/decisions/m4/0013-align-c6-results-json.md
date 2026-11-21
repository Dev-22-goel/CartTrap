---
status: proposed
date: 2026-11-21
decision-makers: "Adish (Member 4)"
consulted: "Member 3 (scoreboard)"
---

# Align the C6 results JSON with the frontend and serve a stable latest.json

## Context and Problem Statement
The frontend reads `failures[] = {case_id, vector?, system?, note?}`, but we write `{id, system, reason}`. `/api/eval/latest` also picks the newest file by mtime, so a holdout or sample run can shadow the frozen run.

## Decision
- `failures[]` becomes `{case_id, id, vector, system, note, reason}` (additive).
- `meta` gains `shop_mode`, `backend` and `n_fail_closed`.
- `run_eval.py` writes `eval/results/latest.json` atomically for the official run, and the route prefers that file.

## Consequences
* Good, because the scoreboard always shows the frozen numbers and never a side run.

## Implementation Plan
* **Affected paths**: `eval/run_eval.py`, `eval/runner/**`, `backend/m4_routes.py`

### Verification
- [ ] `test_failures_have_case_id_and_note` and `test_latest_prefers_latest_json` pass
