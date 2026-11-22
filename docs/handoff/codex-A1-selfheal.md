Read handoff/m4-lane-contract.md first and follow it. It says which files you own and the rules you must follow.

CartTrap repo, branch m4-codex. Read AGENTS.md, plan.md (Global Constraints, Task 16, Task 6 RuleStore, Task 7 gate), docs/architecture.md sections 6-7, backend/schemas.py, .claude/skills/firewall-rules/SKILL.md and .claude/skills/attack-forge/SKILL.md.
Build CartTrap's self-healing firewall loop in backend/selfheal.py and backend/redteam_carbon.py, test-first (superpowers TDD: write failing tests, see them fail, implement, see them pass).

1. propose_probe(bypass_trace: list[TraceEvent]) -> Probe
   - Locate the stage where the attack slipped through (claims -> probe p-values -> gate).
   - Produce ONE atomic probe: a single yes/no question, schema-valid per rules.json, unique name, default threshold 0.10. Reject compound questions ("and"/"or" joining two checks) and duplicates of existing probe names or near-duplicates (normalized-text similarity > 0.9).
   - Gemini call via google-genai with a structured-output Pydantic schema; model ID from backend/config.py only. 10 s timeout -> raise SelfHealError (never return a half-built probe).
2. async validate_probe(probe, exploit: dict, benign: list[dict]) -> bool
   - Run probe on the exploit and all benign fixtures concurrently (asyncio.gather, bounded semaphore of 4).
   - Accept iff exploit p >= threshold AND every benign p < threshold. Return a ValidationReport (per-fixture p, latency, reason) alongside the bool.
   - On accept: RuleStore.append with version+1, atomic write (temp file + os.replace) so a crash never corrupts rules.json; keep a rules.json.bak of the previous version.
   - Idempotent: validating the same probe twice must not append twice.
3. async launch_redteam(product_id: str|None, rounds: int, bus, run_id) -> list[ManifestEntry]
   - Hard cap rounds at 3 regardless of input. Each round: forge or receive attack -> run_guarded -> if blocked, emit telemetry to the attacker and request a mutation -> if it bypasses, call propose_probe + validate_probe -> on accept, re-run the same attack and confirm it is now blocked.
   - Emit TraceEvents (pane "redteam") for every step; the full sequence must be writable to runs/redteam_demo.jsonl and replayable in order.
   - MANAGED_AGENTS env flag: True -> Carbon Managed Agent; False -> local forge() + Carbon via API. Sandbox Shop access read-only (search_catalog, get_product).
   - Any exception in a round ends the loop cleanly with a "redteam_error" event; never leaves rules.json half-written.
Constraints: never call complete_checkout, complete_spend_request or create_spend_request. ShopMCP only, never raw HTTP. No DB. Model IDs only from config.py. Secrets only from .env.
RuleStore (C4) and run_guarded (C7) may not exist yet: depend on Protocols and test with fakes.
Tests that must pass (fakes only, no network): test_validate_rejects_probe_that_fires_on_benign, test_validate_accepts_and_appends, test_validate_is_idempotent, test_append_is_atomic_on_crash, test_propose_rejects_compound_probe, test_propose_rejects_duplicate, test_launch_caps_rounds, test_loop_reblocks_after_heal, test_round_error_emits_event_and_stops, test_trace_replays_in_order.
Only edit: backend/selfheal.py, backend/redteam_carbon.py, tests/test_selfheal.py, tests/test_redteam_loop.py, handoff/codex-status.md.
Done = `pytest -q tests/test_selfheal.py tests/test_redteam_loop.py` all green, plus a 10-line design note in handoff/codex-status.md (key decisions + anything you were unsure of). Commit on m4-codex; never push to main.

Sandbox contract (from redteam/sandbox/AGENTS.md, already written by Claude):
- The attacker's log ends each round with one line `MANIFEST: {json}` (single-line JSON). Parse the LAST such line. Keys: round, id, vector, product_id, files, intended_hijack, expected_forbidden_tool (string), user_request, budget, mutation_of.
- On a block, send the attacker the Verdict JSON (action, severity, probes[{id, p, fired}]) plus the blocked tool call.
- Artifacts are written to the sandbox `out/` dir; pull them into `redteam/out/<round>/` (git-ignored).
- Read redteam/sandbox/AGENTS.md and redteam/sandbox/skills/attack-forge/SKILL.md before coding. Do not edit them.
