---
status: proposed
date: 2026-11-21
decision-makers: "Adish (Member 4)"
consulted: "Member 1 (backend/main.py), Member 2 (backend/guarded_shopper.py)"
---

# Wire the defender through run_guarded(on_block=), replacing ADR 0002's snippet

## Context and Problem Statement
`backend/guarded_shopper.py` already accepts `run_guarded(..., on_block=)` and calls it with a `BlockContext` (`guarded_shopper.py:82-88,112,194-203`). That makes ADR 0002's paste-in snippet unnecessary. The snippet was also wrong in three places: the `TraceBus.emit` arity, the `attempted_spend` import path, and a recomputed total.

## Decision
`backend/defender_neon.py` exposes `async on_block(b: BlockContext)`. It runs the safe swap, builds the Fraud Card, and emits `fraud_card` on `b.bus`. It never raises and has a 10 s cap. Member 1 passes `on_block=defender_on_block` at the `run_guarded` call in `backend/main.py`. Nobody edits `guarded_shopper.py`. The eval passes `on_block=None`. This supersedes ADR 0002.

## Consequences
* Good, because Member 2's file isn't edited, and the hook is already tested (`tests/test_guarded.py:186,200`).
* Bad, because Member 1 has to add one argument after the defender merges (~1:15).

## Implementation Plan
* **Affected paths**: `backend/defender_neon.py`, `tests/test_defender.py`; one argument in `backend/main.py` (Member 1)

### Verification
- [ ] `test_on_block_emits_fraud_card_on_real_tracebus` passes
- [ ] A live sticky-note run shows a `fraud_card` event in the SSE stream
