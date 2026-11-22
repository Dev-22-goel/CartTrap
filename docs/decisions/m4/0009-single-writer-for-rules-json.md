---
status: proposed
date: 2026-11-21
decision-makers: "Adish (Member 4), Member 2"
consulted: "Member 2 (owner of backend/rules.py and rules.json)"
informed: "Member 1"
---

# Use one writer for rules.json: Member 2's RuleStore, shared by the self-heal loop

## Context and Problem Statement

The verifier found two code paths that can write `backend/rules.json`:

- Member 2's `backend/rules.py` `RuleStore.append`. It writes atomically (temp file + `os.replace`) but locks only per instance with a `threading.Lock`.
- Member 4's `backend/selfheal.py` `AtomicRuleStore`. It writes atomically, keeps `rules.json.bak`, and takes a cross-process file lock on `rules.json.lock`.

If both are used, one can read version 7 while the other publishes version 8, and the first then overwrites version 8 with its own copy. The self-healed probe would be silently lost in the middle of the demo. Nothing triggers this yet, because no code constructs `rules.RuleStore` in the write path today.

## Decision

- **Member 2's `RuleStore` is the only writer.** The FastAPI app builds one shared `RuleStore("backend/rules.json")` instance. The firewall reads from it, and the self-heal loop receives that same instance (dependency injection) instead of building its own.
- `backend/selfheal.py` keeps validation and the "fires on the exploit, on no benign" gate. On publish it copies the current file to `rules.json.bak`, then calls the shared `RuleStore.append(probe)`. Its own `AtomicRuleStore` stays only as a test helper.
- One uvicorn worker (the default) means one process, so the per-instance `threading.Lock` is enough. **Ask to Member 2:** none required. Optional: take `rules.json.lock` in `append` if multi-process ever happens.
- `validate_probe` in `backend/defender_neon.py` returns `bool`, per plan.md. The full report stays on `backend.selfheal.validate_probe` (done 2026-11-21).

## Consequences

* Good, because there's one place that writes rules, so no lost updates.
* Good, because Member 2's file stays the owner of the rules format.
* Bad, because the self-heal route needs the app's `RuleStore` passed in, so Member 1 wires it when the router is included (one argument).

## Implementation Plan

* **Affected paths**: `backend/selfheal.py` (accept an injected `RuleStore`, back up, then append), `backend/m4_routes.py` (pass the app's store), Member 1: `app.state.rules = RuleStore(...)` in `backend/main.py`
* **Patterns to avoid**: constructing a second store that writes `rules.json`

### Verification

- [ ] `grep -n "AtomicRuleStore()" backend/` shows no use outside tests
- [ ] `test_selfheal_uses_injected_store` passes (a fake store records exactly one `append`)
- [ ] After a live heal, `rules.json` version is +1 and `rules.json.bak` holds the previous version
