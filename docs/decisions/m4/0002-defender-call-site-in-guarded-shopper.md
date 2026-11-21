---
status: proposed
date: 2026-11-21
decision-makers: "Adish (Member 4), Member 2"
consulted: "Member 2 (owner of backend/guarded_shopper.py)"
informed: "Member 1"
---

# Member 2 owns the defender call site in guarded_shopper.py; Member 4 supplies the functions

## Context and Problem Statement

`plan.md` Task 10 (Member 4) says to "modify `guarded_shopper.py` to call it on non-approve". `guarded_shopper.py` is created by Task 9, which belongs to Member 2, and it's still being written at 1:00 PM, when Task 10 starts. Two people editing it at once would conflict, and Member 4 would be coding against a moving target.

## Decision

Member 4 owns everything in `backend/defender_neon.py` and exposes a stable interface, exactly as in plan.md Task 10:

- `async build_fraud_card(verdict, claims, product_json, blocked: ToolCall, attempted: float, safe_cart: dict|None) -> FraudCard` (8 s Neon timeout, falls back to `template_fraud_card`)
- `async safe_swap(intent: Intent, original: dict|None, shop: ShopMCP) -> dict|None`
- `dollars_defended(attempted: float, safe_total: float|None) -> float`

**Member 2** adds the call in `guarded_shopper.py` on any non-approve verdict: first `safe_swap`, then `build_fraud_card`, then emit a `fraud_card` TraceEvent. That's about 10 lines. Member 4 sends the exact snippet at S2 (1:00 PM).

If Member 2 is overloaded at S3 (2:00 PM), Member 4 may add the snippet instead, with Member 2's OK in the channel. Only that block changes.

Non-goals: Member 4 does not change gate, threshold or verdict logic.

## Consequences

* Good, because each file has one writer, so S2/S3 merges are clean.
* Good, because Task 10 can be built and tested at 1:00 against a fake `GuardedResult`, without waiting for Task 9.
* Bad, because the S3 E2E test (`test_e2e_attack.py` expects a `fraud_card` with `dollars_defended > 0`) depends on Member 2 adding the call before 2:00.

## Implementation Plan

* **Affected paths**: `backend/defender_neon.py`, `backend/prompts/neon_fraud_card.md`, `tests/test_defender.py` (Member 4); `backend/guarded_shopper.py` call block only (Member 2)
* **Dependencies**: C7 `run_guarded` / `GuardedResult` (Member 2), C2 `ShopMCP` (Member 1)
* **Patterns to follow**: `safe_swap` uses `ShopMCP` only; Neon timeout → template card so the UI never hangs
* **Patterns to avoid**: raw HTTP in `defender_neon.py`; calling `complete_checkout`, `complete_spend_request` or `create_spend_request`

### Verification

- [ ] `pytest -q tests/test_defender.py` passes (5 tests named in plan.md Task 10)
- [ ] `grep -n "httpx\|requests\|urllib" backend/defender_neon.py` returns nothing
- [ ] `tests/integration/test_e2e_attack.py` sees a `fraud_card` event with `dollars_defended > 0` at S3
