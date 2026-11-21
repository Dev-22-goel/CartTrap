---
status: proposed
date: 2026-11-21
decision-makers: "Adish (Member 4)"
informed: "Member 1 (pyproject.toml)"
---

# No new dependencies: stdlib percentiles and optional test libraries (amends ADR 0007)

## Context and Problem Statement
`numpy`, `hypothesis` and `Pillow` aren't in `pyproject.toml`. A `uv sync` would remove them, and Member 4's code would then break on teammates' machines.

## Decision
Metrics compute percentiles with stdlib linear interpolation. Tests wrap Hypothesis and Pillow in `pytest.importorskip`. Nothing is asked of Member 1. The case renderer needs Pillow only when building cases on Adish's machine.

### Verification
- [ ] `test_no_numpy_import` passes, and a fresh `uv sync` venv runs the suite with skips rather than errors
