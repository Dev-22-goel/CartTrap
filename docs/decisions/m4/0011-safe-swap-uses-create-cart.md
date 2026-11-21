---
status: proposed
date: 2026-11-21
decision-makers: "Adish (Member 4)"
consulted: "Member 1 (backend/shop_mcp.py)"
---

# Safe swap uses ShopMCP.create_cart and the cart's continue_url (amends ADR 0008)

## Context and Problem Statement
ADR 0008 asked for `create_checkout`. Member 1's `ShopMCP` only exposes `create_cart(shop, lines)` with `lines=[{"variant_id","quantity"}]` (`shop_mcp.py:117-123`). `docs/notes-apis.md` confirms that the cart result already carries `continue_url` and `totals`. As written, the defender's calls would crash on a live run.

## Decision
`safe_swap` calls `create_cart(seller.domain, [{"variant_id", "quantity"}])` and returns its `continue_url` byte for byte. `total` comes from `totals`, converted from cents (÷ 100). We drop the ask for a `create_checkout` wrapper. All other ADR 0008 rules still apply.

## Consequences
* Good, because Member 1's file doesn't change and judges still get a real buy link.
* Neutral: the link opens a cart page rather than a checkout page. The merchant handles the rest.

## Implementation Plan
* **Affected paths**: `backend/defender_neon.py`, `tests/test_defender.py`

### Verification
- [ ] `test_safe_swap_against_real_shopmcp_mocktransport` passes and `continue_url` comes back unchanged
