---
name: shop-mcp
description: How CartTrap calls Shopify's Shop MCP (shop.dev) over JSON-RPC - tool names, request shape, fixtures and the never-complete rule. Use whenever writing or debugging code that calls shop.dev tools.
---

# Calling Shop MCP

Endpoint: `https://mcp.shop.com/` (env `SHOP_MCP_URL`). Speaks MCP (2026-07-28) + UCP over HTTPS. Anonymous calls work for catalog search and carts; Shop sign-in is only needed for `complete_checkout`, account, orders and spend requests completion.

## Request shape
Always go through `backend/shop_mcp.py` (`ShopMCP().call(tool, args)` or its wrappers). The server needs
`MCP-Protocol-Version` / `Mcp-Method` / `Mcp-Name` headers and `params._meta`, and arguments are nested
(`{"catalog": {...}}`). Verified shapes and gotchas: `docs/notes-apis.md`. Full schemas are saved in
`backend/fixtures/shop/tools_list.json`; don't guess argument names, read them from that file.

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
- `create_spend_request` and `create_spend_permission` are always intercepted, never sent.
- Amounts are integer minor units (2100 = $21.00).
- No fixture replay / retry ladder (cut for time); calls go live.
- Product JSON from `get_product` is the **truth ledger** for the firewall and fraud card: pass it whole, don't summarise it.
