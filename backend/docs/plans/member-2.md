## Member 2’s Plan

### Task 3: Schemas and intent — owner: firewall-engineer
**Files:** Create `backend/schemas.py`, `backend/intent.py`, `backend/money.py`, `tests/test_intent.py`, `tests/test_money.py`
**Interfaces (pydantic v2, used by every later task):**
- `Media(kind: Literal["image","audio","video","pdf"], path: str, mime: str)`
- `Intent(text: str, budget: float|None, quantity: int = 1)`
- `Claims(visible_text: list[str], pack_count_claim: int|None, brand_claims: list[str], audio_transcript: str|None, instructions_detected: bool, notes: str = "")`
- `ToolCall(name: str, arguments: dict)`
- `Probe(id: str, type: Literal["noul","choice","score"], category: Literal["injection","pack_lie","spend_hijack","coercion","split_payload","privacy","promo_benign"], instructions: str, threshold: float = 0.10, tiers: dict[str,float] = {}, added_by: str, created_at: str)`
- `ProbeResult(id: str, p: float, fired: bool)`
- `Verdict(action: Literal["approve_checkout","escalate_to_neon_swap","hard_block_quarantine"], action_probs: dict[str,float], probes: list[ProbeResult], severity: int, latency_ms: int, tier: Literal["low","normal","high","spend_request"], backend: Literal["decisions","json_llm"], error: str|None = None)`
- `FraudCard(reason: str, media_claimed: list[str], shopify_sells: dict|None, top_probes: list[ProbeResult], dollars_defended: float, safe_cart: dict|None)`
- `TraceEvent(run_id: str, pane: Literal["victim","guarded","redteam"], t_ms: int, kind: Literal["tool_call","tool_result","intercepted","verdict","fraud_card","log","done"], data: dict)`
- `parse_intent(text: str, budget: float|None) -> Intent` (budget field wins; else "$25"/"under 25" in text; quantity from "one/two/3"/digits, default 1)
- `attempted_spend(call: ToolCall, products: dict[str, dict]) -> float` (Σ qty × price over cart lines; spend requests use their `amount`)
- [ ] Step 1: Tests: `test_parse_intent_budget_from_text` ("buy one pack under $25" → budget 25, qty 1), `test_parse_intent_field_wins`, `test_parse_intent_no_budget` (→ None, qty 1), `test_attempted_spend_cart` (qty 50 × 19.99 = 999.50), `test_attempted_spend_spend_request` (amount 400 → 400).
- [ ] Step 2: Run → FAIL. Step 3: implement. Step 4: Run → PASS. Step 5: Commit `feat: schemas, intent parsing, spend math`.

### Task 6: Rules store — owner: firewall-engineer (parallel with 5)
**Files:** Create `backend/rules.json` (≈50 seed probes: ≥ 8 per attack category, ≥ 3 cross-modal split-payload, ≥ 5 `promo_benign`), `backend/rules.py`, `tests/test_rules.py`
**Interfaces:**
- Produces: `RuleSet(version: int, probes: list[Probe])`; `class RuleStore(path: str)` with `current() -> RuleSet` (reloads when mtime changes), `append(probe: Probe) -> int` (writes atomically, returns new version).
- [ ] Step 1: Tests: `test_seed_rules_valid` (parses; 40 ≤ len ≤ 60; ids unique), `test_hot_reload` (edit file → `current().version` changes), `test_append_bumps_version`.
- [ ] Step 2: FAIL. Step 3: implement; write probes per the `firewall-rules` skill (atomic, grounded, cross-modal). Step 4: PASS. Step 5: Commit `feat: rules store + seed probes`.

### Task 7: Firewall decide + gate — owner: firewall-engineer
**Files:** Create `backend/firewall_decisions.py`, `tests/test_firewall_gate.py`, `tests/test_firewall_live.py`, `eval/golden/` (≥ 3 attack + 3 benign images incl. `sticky_note.png`, `benign_blurry.jpg`, `promo_banner.jpg`)
**Interfaces:**
- Consumes: `RuleSet`, `Intent`, `Media`, `Claims`, `ToolCall`, `config`.
- Produces: `tier_for(call: ToolCall, cart_total: float) -> str`; `gate(action_probs: dict[str,float], results: list[ProbeResult], probes: list[Probe], tier: str, severity: int) -> str` (rules in architecture §0 decision 5); `async decide(intent: Intent, media: list[Media], product_json: dict|None, proposed: ToolCall, claims: Claims|None, rules: RuleSet, cart_total: float) -> Verdict` — one call to the configured backend (`decisions` or `json_llm`), images at `ultra_high`, timeout `firewall_timeout_ms`.
- [ ] Step 1: Unit tests (mocked backend): `test_gate_all_low_probes_approves`, `test_gate_injection_fires_hard_block`, `test_gate_pack_lie_only_escalates`, `test_gate_low_tier_relaxes_promo`, `test_tier_spend_request`, `test_tier_without_budget`, `test_decide_timeout_fails_closed` (→ hard_block, `error` set), `test_decide_malformed_fails_closed`, `test_decide_without_product_skips_mismatch` (pack_lie probes not sent when `product_json is None`).
- [ ] Step 2: FAIL. Step 3: implement; wrap the real SDK call shape from `docs/notes-apis.md` in one private function per backend.
- [ ] Step 4: Unit PASS; live: `sticky_note.png` → `hard_block_quarantine`, `benign_blurry.jpg` and `promo_banner.jpg` (cart $20) → `approve_checkout`; log p50 latency of 10 calls.
- [ ] Step 5: Commit `feat: firewall decide + gate`.

### Task 8: Argon perception — owner: firewall-engineer (parallel with 7)
**Files:** Create `backend/perception_argon.py`, `backend/prompts/argon.md`, `tests/test_perception.py`
**Interfaces:** Produces `async perceive(media: list[Media]) -> Claims` (structured output, no tools; on error returns `Claims(..., notes="perception_error")`).
- [ ] Step 1: Tests: `test_perceive_error_returns_empty_claims` (mock raises); live `test_sticky_note_detected` (`instructions_detected is True`, visible_text contains "budget" case-insensitive).
- [ ] Step 2: FAIL. Step 3: implement. Step 4: PASS. Step 5: Commit `feat: argon perception`.

### Task 9: Guarded shopper — owner: firewall-engineer (12:00)
**Files:** Create `backend/guarded_shopper.py`, `tests/test_guarded.py`; modify `backend/main.py` to wire Tasks 5 + 9 into `/api/run`
**Interfaces:**
- Consumes: `shopper_loop` (Task 5), `perceive`, `decide`, `RuleStore`, `ShopMCP`.
- Produces: `GuardedResult(verdicts: list[Verdict], blocked_call: ToolCall|None, approved_calls: list[ToolCall], claims: Claims|None, product_json: dict|None)`; `async run_guarded(intent, media, product_ref, bus, run_id, shop, rules: RuleStore) -> GuardedResult`. Argon starts concurrently with the first search step; each state-changing call awaits `decide`; non-approve stops the loop. Product context per architecture §0 decision 7.
- [ ] Step 1: Tests (fakes): `test_guarded_blocks_and_stops` (decide → hard_block; no further tool calls; `verdict` event emitted), `test_guarded_checks_every_state_change` (cart then checkout → 2 decide calls), `test_argon_runs_concurrently` (perceive and first search overlap in time).
- [ ] Step 2: FAIL. Step 3: implement. Step 4: PASS; live: `curl -N` on a sticky-note run shows victim `intercepted` + guarded `verdict: hard_block_quarantine`.
- [ ] Step 5: Commit `feat: guarded shopper wired into run API` — **walking skeleton done (12:45).**

## Member 2 sync points (from integration.md)
- **Read first:** Global Constraints and Review Focus in `plan.md`.
- **You deliver:** C1 `schemas.py` + `intent.py` + `money.py` (**11:00, everyone waits on this**), C4 `rules.json` + `RuleStore` (11:45), C7 `run_guarded` (1:00).
- **You need:** C2 `ShopMCP` from Member 1 (11:45; use fixtures before), C8 `shopper_loop` from Member 1 (12:45; code against the signature before).
- **After Task 9:** tune only on `eval/golden/`; 2:30–3:15 apply the Task 15 fix with Member 4; 3:15–4:15 P1 US-10 if green, else support; bugfix only after 4:15.
- **Owned files:** `schemas.py` (additive changes only after S1), `firewall_decisions.py`, `rules.json`, `perception_argon.py`, `guarded_shopper.py`.
- **Checkpoints:** S1 11:00 · S2 1:00 · S3 2:00 · S4 2:30 · S5 3:15 · S6 4:15 · S7 4:45.
