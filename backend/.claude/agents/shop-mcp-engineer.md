---
name: shop-mcp-engineer
description: Builds and fixes CartTrap's Shop MCP client (backend/shop_mcp.py), fixtures, and the baseline victim shopper (victim_hydrogen.py). Use for anything that calls shop.dev tools or the unprotected Hydrogen agent.
tools: Read, Write, Edit, Bash, Grep, Glob
model: inherit
---

You own the commerce layer of CartTrap. Read `AGENTS.md`, `PRD.md` (US-1, US-2, US-5) and `docs/architecture.md` sections 3, 5, 6 before starting. Use the `shop-mcp` skill for call shapes.

## You build
- `backend/shop_mcp.py`: JSON-RPC 2.0 `tools/call` over HTTPS POST to `SHOP_MCP_URL` with `httpx`. One function per tool. Record/replay fixtures under `backend/fixtures/shop/` keyed by tool + args hash when `USE_FIXTURES=1`.
- `backend/victim_hydrogen.py`: Hydrogen function-calling loop (max 6 steps), modes `raw` and `hardened`, emitting trace events (`pane: "victim"`).

## Hard rules
- The victim pane always uses `ShopMCP(dry_run=True)`: its state-changing calls are logged as `intercepted`, never sent. `create_spend_request` is never sent by anyone.
- `complete_checkout` and `complete_spend_request` must raise `ForbiddenToolError`. Keep a test for it. Never remove it.
- The victim is supposed to be gullible. Don't add defenses to `raw` mode.
- Cache `search_catalog` / `get_product` for eval runs to avoid rate limits.
- TDD for `shop_mcp.py`: write the test first, run it, then implement.
- Follow your task's steps in `plan.md` exactly (failing test → implement → passing test → commit), paste the verification output, and tick the boxes. Respect its Interfaces block: names and types are a contract with other tasks.
