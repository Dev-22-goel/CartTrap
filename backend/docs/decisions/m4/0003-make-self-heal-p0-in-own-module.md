---
status: proposed
date: 2026-11-21
decision-makers: "Adish (Member 4)"
consulted: "Member 2 (owner of RuleStore and rules.json)"
informed: "Member 1, Member 3"
---

# Make self-heal a committed (P0) deliverable, built in its own module on a safe RuleStore.append

## Context and Problem Statement

In `plan.md`, Task 16 (Carbon red-team + self-heal) is P1, so it can be cut. Member 4 has decided to ship self-heal for sure, because "the firewall writes and validates its own new rule" is the strongest demo moment. Self-heal writes to `rules.json` through Member 2's `RuleStore` (contract C4) while the firewall reads that same file, so a half-written file could break every run. The self-heal code was also planned inside `defender_neon.py`, which Task 10 is editing at the same time.

## Decision

1. **Priority:** self-heal (`propose_probe` → `validate_probe` → `RuleStore.append` → re-run the attack and confirm it's blocked) is P0. Only the *live Managed Agents launch* stays cuttable at 3:45 PM. The fallback is local `forge()` + a recorded `runs/redteam_demo.jsonl`, and self-heal still runs for real either way.
2. **Module:** self-heal lives in a new `backend/selfheal.py` (Member 4). `backend/defender_neon.py` re-exports `propose_probe` and `validate_probe`, so plan.md's names still work.
3. **Ask to Member 2 (C4):** `RuleStore.append(probe)` should write atomically (temp file + `os.replace`), bump `version` by 1, keep `rules.json.bak`, and ignore a probe whose name already exists. If Member 2 has no time, Member 4's `selfheal.py` wraps the call with these guarantees, and Member 2 only reviews.
4. **Validation gate (unchanged from plan.md):** a probe is appended only if it fires on the exploit and on none of the 5 benign fixtures.

Non-goals: no change to gate thresholds or verdict logic; no database.

## Consequences

* Good, because the demo's self-heal moment no longer depends on Managed Agents being up.
* Good, because a crash mid-write can't corrupt `rules.json` during the demo.
* Bad, because Member 4's afternoon is fuller (3:15–4:15 PM is now must-ship).
* Neutral: Member 3's S6 fallback note "switch red-team button to replay" now means "replay the attacker"; the self-heal step still runs live.

## Implementation Plan

* **Affected paths**: `backend/selfheal.py`, `backend/redteam_carbon.py`, `tests/test_selfheal.py`, `tests/test_redteam_loop.py`, `runs/redteam_demo.jsonl` (Member 4); `backend/defender_neon.py` (+1 re-export line, Member 4); `RuleStore.append` (Member 2, or wrapped by Member 4)
* **Dependencies**: C4 `RuleStore` (Member 2, 11:45), C7 `run_guarded` (Member 2, 1:00), C5 `forge()` (Member 3, 11:45)
* **Patterns to follow**: atomic file write; one atomic yes/no probe per heal; max 3 red-team rounds; sandbox Shop access read-only (`search_catalog`, `get_product`)
* **Patterns to avoid**: writing `rules.json` without validation; spend tools in the sandbox

### Verification

- [ ] `pytest -q tests/test_selfheal.py tests/test_redteam_loop.py` passes (includes `test_append_is_atomic_on_crash`, `test_loop_reblocks_after_heal`, `test_launch_caps_rounds`)
- [ ] After a live heal, `rules.json` has `version` +1, and `rules.json.bak` holds the previous version
- [ ] `runs/redteam_demo.jsonl` replays one full round in the UI at S6
