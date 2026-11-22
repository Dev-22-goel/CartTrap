# Defender call block for `guarded_shopper.py` (ADR m4/0002)

Member 2 pastes this where `run_guarded` handles a non-approve verdict, right after the `verdict` TraceEvent is emitted and the loop is about to stop. Member 4 does not edit `guarded_shopper.py`.

```python
from backend.defender_neon import build_fraud_card, safe_swap
from backend.schemas import attempted_spend

# verdict.action != "approve_checkout"; `call` is the blocked ToolCall
attempted = attempted_spend(call, {product_json["id"]: product_json} if product_json else {})
safe_cart = await safe_swap(intent, product_json, shop)          # None if nothing fits budget/qty
card = await build_fraud_card(verdict, claims, product_json, call, attempted, safe_cart)  # 8 s cap, template fallback
bus.emit(TraceEvent(run_id=run_id, pane="guarded", t_ms=now_ms(), kind="fraud_card", data=card.model_dump()))
```

Notes:
- `safe_swap` only uses `shop` (ShopMCP): `search_catalog`, `get_product`, then `create_checkout(shop_domain, lines)`; it falls back to `create_cart(shop_domain, lines)` if checkout raises. Both need the `shop` first argument per ADR m4/0008. The `ShopMCP` signatures must be `create_checkout(shop, lines)` and `create_cart(shop, lines)`.
- `safe_cart` is `{checkout_id, continue_url, shop, line_items, total}`; `continue_url` is the merchant URL byte for byte. The UI shows it as "Buy the safe one". In a dry-run `ShopMCP`, `continue_url` is `None` and `safe_cart["intercepted"]` is `True`.
- `build_fraud_card` never raises: Neon timeout or error returns the template card. `dollars_defended` is already computed (attempted minus `safe_cart["total"]`).
- `attempted_spend` comes from Task 3 (`backend/schemas.py` or `backend/money.py`); adjust the import to where it landed.
