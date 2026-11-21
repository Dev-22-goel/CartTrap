---
status: proposed
date: 2026-11-21
decision-makers: "Adish (Member 4)"
consulted: "Member 1 (ShopMCP, fixtures), Member 3 (forge, demo)"
informed: "Member 2"
---

# Follow the Shopify challenge rules in the safe swap and the eval

## Context and Problem Statement

The Shopify side-quest rules (resource gist, 2026-11-21; docs at shop.dev/docs) add requirements the kit didn't account for:

1. **"A judge must be able to make a real purchase through your project."** Purchases happen on the merchant's page: one checkout per merchant, then the shopper opens its `continue_url`. Our safe swap is the natural place for that purchase.
2. **"Use live data… Don't cache results or re-host merchant images."**
3. **"Keep links exactly as returned"**, with every query parameter.
4. Tool shapes (shop.dev/docs/tools.md): `create_cart` and `create_checkout` both need `shop` (the offer's `seller.domain`, exactly) plus `line_items`. `create_checkout` does **not** take a cart ID. The plan.md Task 2 signature `create_checkout(cart_id: str)` doesn't match the real tool.

Our existing rule (never call `complete_checkout`) already matches "your project can't complete checkouts itself".

## Decision

- **Safe swap ends in a real checkout link.** `safe_swap` picks an honest product (qty = intent, total ≤ budget), then calls `create_checkout` with `shop = seller.domain` and the line items, through `ShopMCP`. It returns `{checkout_id, continue_url, shop, line_items, total}`. The Fraud Card shows `continue_url` **unchanged** as the "Buy the safe one" button. That button is the judge's real purchase path. If anonymous checkout fails live, fall back to `create_cart` and show its URL (plan.md Task 2 step 4 decides).
- **Ask to Member 1:** `ShopMCP.create_cart(shop, lines)` and `ShopMCP.create_checkout(shop, lines)` take `shop`, matching the real tools. Additive if they keep the old names.
- **Eval uses live Shop for the official runs.** The 2:30 frozen run and the 3:15 re-run call Shop MCP live. Record/replay (vcrpy) is for unit tests and dry runs only. Cases store product IDs, not cached product JSON. The runner fetches product details at run time, and the results file keeps the `get_product` snapshot it scored against, as evidence.
- **No merchant images committed.** `eval/cases/` stores product IDs and our own attack overlays. Images are fetched live and composited at run time. The 6 sticky-note props are our own photos, so committing them is fine. **Ask to Member 3:** `forge()` writes composites to a git-ignored folder (`redteam/out/`), not into the repo.
- **Links:** never rewrite, shorten or strip parameters from product URLs or `continue_url`.

## Consequences

* Good, because CartTrap qualifies for the Shopify side quest, and the defender's output becomes a real, buyable safe cart.
* Good, because eval numbers come from live data judges can reproduce.
* Bad, because live runs are slower and depend on Shop being up. The runner's per-case timeout and error recording (brief A2) cover that.
* Bad, because Member 1's `ShopMCP` signatures change slightly.

## Implementation Plan

* **Affected paths**: `backend/defender_neon.py` (`safe_swap` returns checkout), `eval/build_cases.py` (IDs, not cached JSON), `eval/run_eval.py` (`--live` default for official runs; replay only with `--replay`); Member 1: `backend/shop_mcp.py` signatures; Member 3: forge output folder
* **Patterns to follow**: pass `seller.domain` exactly as `shop`; one checkout per merchant; keep URLs byte-for-byte
* **Patterns to avoid**: `complete_checkout`; caching product data in committed files; re-hosting merchant images

### Verification

- [ ] `test_safe_swap_returns_continue_url_unchanged` passes (fake shop returns a URL with query params; the card shows the identical string)
- [ ] A live sticky-note run shows a "Buy the safe one" link that opens the merchant's checkout page
- [ ] `git ls-files eval/cases | grep -iE '\.(jpg|png|webp)$'` lists only our own prop photos
- [ ] The 2:30 results file's `meta` shows `shop_mode: live`
