---
status: proposed
date: 2026-11-21
decision-makers: "Adish (Member 4)"
consulted: "Member 1"
---

# Official eval runs use live Shop only, and --shop replay is dropped

## Context and Problem Statement
Member 1 cut fixture replay (`integration.md` §2), so `--shop replay` has nothing behind it. Architecture §0.6 ("replay the cache") also conflicts with ADR 0008.

## Decision
`run_eval.py` runs live only. Tests inject a fake executor instead. For the eval, this supersedes architecture §0.6.

## Consequences
* Bad, because a Shop outage at 2:30 hurts the run. The per-case timeout and error rows keep the results honest.

### Verification
- [ ] `run_eval.py --shop replay` is rejected and `meta.shop_mode` is `live`
