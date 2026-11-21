---
status: proposed
date: 2026-11-21
decision-makers: "Adish (Member 4, runs S4)"
consulted: "Member 1 (test_eval_smoke), Member 3 (scoreboard)"
informed: "Member 2"
---

# Prove the 2:30 PM eval freeze with a case-set hash and add run metadata to the results JSON

## Context and Problem Statement

The S4 checkpoint needs `eval/cases/` "frozen and committed", and tuning after that may only happen on `eval/golden/`. Judges may ask how we know the frozen set wasn't changed after the fix. Today nothing in the results proves it. Member 3's scoreboard reads the results JSON (C6), so any new fields affect them.

## Decision

- `eval/run_eval.py` computes a SHA-256 over the sorted file names and contents of `--cases DIR`, and writes it into every results file.
- Results files get a `meta` block (additive; existing `Metrics` fields unchanged): `case_dir_hash`, `git_sha`, `systems`, `model_ids` (read from `backend/config.py`), `started_at`.
- At S4, Member 4 commits `eval/cases/`, records the hash in `docs/failure-analysis.md`, and blocks further edits to `eval/cases/**` for all Claude agents (project deny rule).
- The 3:15 re-run must show the **same** `case_dir_hash`.

Non-goals: no change to how metrics are calculated; no database.

## Consequences

* Good, because "we didn't tune on the test set" becomes checkable, not just a promise.
* Good, because the README can quote the hash next to the numbers.
* Neutral for Member 3: the extra `meta` block is additive; the scoreboard can ignore it or show the short hash.
* Neutral for Member 1: `test_eval_smoke.py` still passes; it can also assert that `meta.case_dir_hash` exists.

## Implementation Plan

* **Affected paths**: `eval/run_eval.py`, `eval/runner/**`, `tests/test_run_eval.py` (Member 4); optional assert in `tests/integration/test_eval_smoke.py` (Member 1)
* **Dependencies**: none new (`hashlib` stdlib)
* **Patterns to follow**: deterministic, sorted traversal of the case dir
* **Patterns to avoid**: hand-typed numbers anywhere; editing `eval/cases/` after 2:30

### Verification

- [ ] `test_case_dir_hash_changes_on_edit` passes
- [ ] The 2:30 and 3:15 results files show the same `meta.case_dir_hash`
- [ ] `git log --since="14:30" -- eval/cases/` is empty at S7
