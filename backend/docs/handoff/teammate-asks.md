# Messages for teammates (copy and paste)

## To Member 1 (Shop MCP, main.py)
Hi! Member 4 (Adish) here. I need two small things in `backend/main.py` so my routes and the defender show up in the app. Details are in ADRs m4/0001, 0009 and 0010 on branch `adish`.
```python
from backend.m4_routes import m4_router
app.include_router(m4_router)
app.state.rules = RULES          # one shared rules writer (ADR 0009)
# after ~1:15, once the defender merges:
from backend.defender_neon import on_block as defender_on_block
await run_guarded(..., shop=ShopMCP(), rules=RULES, on_block=defender_on_block)
```
FYI: the eval runs live Shop only (ADR 0015), and I'm not adding any dependencies to `pyproject` (ADR 0016).

## To Member 2 (firewall)
Hi! Member 4 here. Good news: your `run_guarded(on_block=)` hook means I don't need to touch `guarded_shopper.py` at all (ADR m4/0010 replaces my old snippet). Self-heal writes rules only through your `RuleStore.append`, via the app's shared instance (ADR 0009). Could you OK ADRs 0010 and 0014? 0014 says the eval scores a fail-closed verdict as a block and shows the count.

## To Member 3 (frontend)
Hi! Member 4 here. A few things for the arena (ADRs m4/0012, 0013):
- Red-team events now use your `data.stage` vocabulary plus `data.message`. The button should call `POST /api/redteam/launch`, take the `run_id` from the response, then stream `/api/runs/{run_id}/stream`.
- Eval results: `failures[]` has `case_id`, `vector`, `system`, `note` and `reason`. `meta.shop_mode` is `"live"`, and there's also `meta.n_fail_closed`.
- `SafeCart.line_items[]` now carries `variant_id`, `product_id`, `title` and `price` (in dollars). Its "Buy the safe one" link is `continue_url`, exactly as returned.
- The backend emits `done` on pane `"system"`. Please treat that pane as global.
- Please don't commit forge output that contains merchant images (Shopify rule, ADR 0008).
