---
status: proposed
date: 2026-11-21
decision-makers: "Adish (Member 4)"
consulted: "Member 1 (owner of backend/main.py)"
informed: "Member 2, Member 3"
---

# Put Member 4's API routes in their own router instead of editing backend/main.py

## Context and Problem Statement

`plan.md` Task 14 says to add `GET /api/eval/latest` "in `backend/main.py`", and Task 16 says to add `POST /api/redteam/launch` there too. But `integration.md` §5 makes `backend/main.py` Member 1's file: "others send route/target changes to M1 or keep them in their own module". If two people edit `main.py` on different branches, merges at S2–S6 can conflict.

## Decision

Member 4 creates `backend/m4_routes.py`, which defines a FastAPI `APIRouter` (`m4_router`) with both routes. Member 1 adds one line to `backend/main.py`, once, as soon as the file exists:

```python
from backend.m4_routes import m4_router
app.include_router(m4_router)
```

The route paths, methods and response shapes don't change. Contract C6 (`GET /api/eval/latest` returns the `Metrics` JSON) is unchanged for Member 3.

Non-goals: no other changes to `main.py`. No auth, no new middleware.

## Consequences

* Good, because Member 4 never touches `backend/main.py`, so merges stay conflict-free.
* Good, because Member 4 can test the routes in isolation with `TestClient`.
* Bad, because Member 1 has to add one line before S2 (1:00 PM), or the routes don't show up in the running app.

## Implementation Plan

* **Affected paths**: `backend/m4_routes.py` (new, Member 4), `tests/test_m4_routes.py` (new, Member 4), `backend/main.py` (+2 lines, Member 1)
* **Dependencies**: none new
* **Patterns to follow**: FastAPI `APIRouter`; `GET /api/eval/latest` returns the newest `eval/results/*.json` or 404; `POST /api/redteam/launch` calls `launch_redteam`, or replays `runs/redteam_demo.jsonl` if live launch is off
* **Patterns to avoid**: editing `backend/main.py` from any Member 4 branch

### Verification

- [ ] `pytest -q tests/test_m4_routes.py` passes
- [ ] `git log --format=%an -- backend/main.py` shows no Member 4 commits
- [ ] With the server running, `curl localhost:8000/api/eval/latest` returns the sample results JSON by 1:00 PM

## Alternatives Considered

* Member 4 edits `main.py` directly: rejected, because it breaks the ownership rule in integration.md §5.
* Member 1 writes the routes from Member 4's spec: rejected, because it adds work to the integration lead on the busiest morning.
