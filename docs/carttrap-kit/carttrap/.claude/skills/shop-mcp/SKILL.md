---
name: shop-mcp
description: How CartTrap calls Shopify's Shop MCP (shop.dev) over JSON-RPC - tool names, request shape, fixtures and the never-complete rule. Use whenever writing or debugging code that calls shop.dev tools.
---

# Calling Shop MCP

Endpoint: `https://mcp.shop.com/` (env `SHOP_MCP_URL`). Speaks MCP (2026-07-28) + UCP over HTTPS. Anonymous calls work for catalog search and carts; Shop sign-in is only needed for `complete_checkout`, account, orders and spend requests completion.

## Request shape
```python
payload = {"jsonrpc": "2.0", "id": next_id(), "method": "tools/call",
           "params": {"name": tool, "arguments": args}}
r = httpx.post(SHOP_MCP_URL, json=payload, timeout=15)
```
First call `tools/list` once and save it to `backend/fixtures/shop/tools_list.json` so argument schemas are on disk. Don't guess argument names; read them from that file.

## Tools (17)
| Group | Tools | CartTrap use |
|---|---|---|
| Catalog | `search_catalog`, `lookup_catalog`, `get_product` | victim shopping, ground-truth JSON, safe swap, eval case sampling |
| Stores | `search_locations`, `lookup_locations` | Later: local pickup swap |
| Cart | `create_cart`, `get_cart`, `update_cart` | gated by firewall |
| Checkout | `create_checkout`, `get_checkout`, `update_checkout`, `complete_checkout` | create/update gated; **complete forbidden** |
| Account | `get_account`, `search_orders` | Later: privacy-leak probes |
| Spend requests | `create_spend_request`, `get_spend_request`, `update_spend_request`, `cancel_spend_request`, `complete_spend_request` | create = highest-risk tier; **complete forbidden** |

## Rules
- `complete_checkout` and `complete_spend_request` raise `ForbiddenToolError` in `shop_mcp.py`. Keep it that way.
- `USE_FIXTURES=1` replays from `backend/fixtures/shop/<tool>/<sha1(args)>.json`; `RECORD_FIXTURES=1` writes them.
- Cache catalog calls in eval; back off on 429 (0.5 s, 1 s, 2 s).
- Product JSON from `get_product` is the **truth ledger** for the firewall and fraud card: pass it whole, don't summarise it.
