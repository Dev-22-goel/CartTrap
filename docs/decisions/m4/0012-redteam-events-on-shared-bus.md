---
status: proposed
date: 2026-11-21
decision-makers: "Adish (Member 4)"
consulted: "Member 3 (frontend), Member 1 (trace bus)"
---

# Red-team runs stream through the shared TraceBus, using Member 3's stage vocabulary

## Context and Problem Statement
The frontend fixture keys each red-team step on `data.stage`, which is one of launch, attack, blocked, mutate, bypass, diagnose, probe_proposed, validate, patched or reblocked, plus a `data.message` (`origin/shivam:frontend/src/state.ts:210`). Our backend emits `data.step` with no message, publishes on a private bus, and returns the events inline.

## Decision
`POST /api/redteam/launch` starts the loop as a background task on `app.state.bus` and returns `{run_id}`. The UI streams `/api/runs/{run_id}/stream`. Every red-team event carries `data.stage` (Member 3's vocabulary) and `data.message`, and keeps `step` for compatibility. `runs/redteam_demo.jsonl` uses the same format. Replay pushes it onto the bus with its original timing.

## Consequences
* Good, because live runs and replay share one stream format and one reducer.
* Bad, because the frontend button has to call launch and then open the stream (ask to Member 3).

## Implementation Plan
* **Affected paths**: `backend/m4_routes.py`, `backend/replay.py`, `backend/redteam_carbon.py`, `backend/selfheal.py`, `runs/redteam_demo.jsonl`

### Verification
- [ ] `test_launch_returns_run_id_and_streams_via_bus` and `test_events_have_stage_and_message` pass
