---
status: proposed
date: 2026-11-21
decision-makers: "Adish (Member 4)"
consulted: "Member 1 (owns Task 1 scaffold, requirements and Makefile)"
informed: "Member 2, Member 3"
---

# Add Member 4's test and eval dependencies to the shared requirements

## Context and Problem Statement

Member 4's tests and eval runner use libraries the Task 1 scaffold may not include: `hypothesis` (property test for Dollars Defended), `pytest-asyncio` (async defender, self-heal and runner tests), `numpy` (percentiles), and `vcrpy` (record/replay of Shop responses). Task 1 (requirements file, `Makefile`) belongs to Member 1. If the dependencies are missing, the Codex jobs at 10:30 and 11:40 fail on import, and `make test` fails for everyone.

## Decision

Member 1 adds these to the dev/test requirements during Task 1 (10:30–11:00):

```
hypothesis
pytest-asyncio
numpy
vcrpy
```

If Task 1 isn't merged by 10:45, Member 4 keeps a temporary `requirements-m4.txt` (install with `pip install -r requirements-m4.txt`) and deletes it once Member 1's file has the lines. Member 4 never edits Member 1's requirements file or `Makefile` directly.

Non-goals: no runtime dependency changes; no new services.

## Consequences

* Good, because `make test` stays green for the whole team once Member 4's tests land.
* Bad, because it's one more small ask of Member 1 in the first 30 minutes.

## Implementation Plan

* **Affected paths**: Member 1's requirements file (4 lines); temporary `requirements-m4.txt` (Member 4) if needed
* **Patterns to avoid**: pinning versions that conflict with the scaffold; editing the `Makefile`

### Verification

- [ ] `python -c "import hypothesis, pytest_asyncio, numpy, vcr"` succeeds in the team venv
- [ ] `requirements-m4.txt` is deleted by S2
