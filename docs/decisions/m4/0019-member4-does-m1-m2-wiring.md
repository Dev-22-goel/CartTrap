---
status: accepted
date: 2026-11-21
decision-makers: "Adish (Member 4)"
informed: "Member 1, Member 2"
---

# Member 4 does the Member 1 and Member 2 integration wiring on branch adish

## Context and Problem Statement
Adish asked for the system to work end to end today, without waiting on teammate asks. Several asks (ADRs 0001, 0009, 0010) needed small edits in Member 1's and Member 2's files.

## Decision
Member 4 makes these edits on `adish`. Each one is recorded here so the owners can review it at the next merge:
- `backend/main.py` (Member 1):
  - imports `m4_router` and `defender_on_block`
  - `app.state.rules = RULES`
  - `app.include_router(m4_router)`
  - `run_guarded(..., on_block=defender_on_block)`

  That's 5 lines in total.
- `tests/test_main_wiring.py` (Member 2): the fake `run_guarded` accepts `on_block`, and the test asserts the defender hook and the shared rules store.
- Coming next, same rule: Member 1's integration tests (`tests/integration/**`), the golden images for Member 2's live tests, and the `run_attack.jsonl` fixture recorded from a live run.

Member 3's files are excluded. Adish handles those. Nothing is pushed to `main`.

## Consequences
* Good, because the stack runs end to end on `adish` now.
* Bad, because owners must review these edits when merging. This ADR lists all of them.

### Verification
- [ ] `python -c "import backend.main"` lists `/api/eval/latest` and `/api/redteam/launch`
- [ ] `tests/test_main_wiring.py` passes with the `on_block` assertion
