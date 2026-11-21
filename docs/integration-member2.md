# Member 2 integration notes (firewall track)

Branch: `Udaya`
Owner: Member 2 (Udaya)
Status: C1, C4, Task 7 firewall (`decide`/`gate`/`tier_for`) and Task 8 Argon `perceive` done. The Decisions API call itself is not wired yet (fails closed). C7 (`run_guarded`) due 1:00.

Run the tests: `uv sync` then `uv run pytest -q`. My tests are test_intent, test_money, test_rules, test_firewall_gate and test_perception.

## What's ready

| Contract | Files | Who uses it |
|---|---|---|
| C1 schemas, intent, spend math | `backend/schemas.py`, `backend/intent.py`, `backend/money.py` | everyone |
| C4 rules store and 50 seed probes | `backend/rules.py`, `backend/rules.json` | Member 3 (probe names for the lights), Member 4 (self-heal `append`), me (firewall) |
| Task 8 Argon perception | `backend/perception_argon.py`, `backend/prompts/argon.md` | me (guarded shopper), Member 4 (Neon can quote `Claims` in the fraud card) |
| Task 7 firewall | `backend/firewall_decisions.py` | me (guarded shopper), Member 4 (Neon reads `Verdict`), Member 3 (seismograph), eval |

## C1: schemas (`backend/schemas.py`)

All shapes match `plan.md` Task 3 exactly. Import them, don't redefine them.

```python
from backend.schemas import Media, Intent, Claims, ToolCall, Probe, ProbeResult, Verdict, FraudCard, TraceEvent
```

Rule from now on: `schemas.py` only gets new optional fields. Nothing is renamed or removed. If you need a change, message me.

Things worth knowing:
- `Intent.quantity` must be 1 or more.
- `Probe.tiers` is a per-tier threshold override, for example `{"low": 0.5}`. Each probe gets its own dictionary.
- `Verdict.error` is `None` normally. When the firewall fails closed (timeout, bad response) it holds the reason and `action` is `hard_block_quarantine`. The UI should show "firewall error" when it's set.
- `TraceEvent.pane` is `victim | guarded | redteam`. `kind` is `tool_call | tool_result | intercepted | verdict | fraud_card | log | done`. Anything else fails validation.

## C1: intent (`backend/intent.py`)

```python
parse_intent(text: str, budget: float | None) -> Intent
```

- Only call this on the Request box text. Never on anything from media.
- The budget field wins over any number in the text.
- Otherwise it reads "under $25", "max 30", "less than $18.50", "budget of 40 dollars", "$12", and so on.
- Quantity comes from "one/two/three", "a pair of", "a dozen", or digits. Default is 1.
- Pack and unit sizes are not quantity: "buy a 12-pack" is 1, "buy one 16 oz bottle" is 1. Dollar amounts are never read as quantity.
- No budget in the text and no budget field gives `budget=None`.

## C1: spend math (`backend/money.py`)

```python
attempted_spend(call: ToolCall, products: dict[str, dict]) -> float
```

- Cart calls: sum of quantity times price over the cart lines. Spend requests: their `amount`.
- `products` is keyed by product or variant id, with the product JSON as the value.
- **Member 1:** the real Shop MCP argument names aren't confirmed yet. For now it accepts `lines | line_items | items | cart_lines`, `quantity | qty`, `product_id | variant_id | merchandise_id | id`, and prices as `19.99`, `"19.99"` or `{"amount": "19.99"}`. Once `tools_list.json` is saved, tell me the real names and I'll add a test for them.
- Unknown prices count as 0. It never raises on odd input.
- `create_checkout` with only a `cart_id` returns 0, since there are no lines to price. The guarded shopper passes the cart total from the earlier `create_cart`.

## C4: rules (`backend/rules.py`, `backend/rules.json`)

```python
store = RuleStore("backend/rules.json")
rs = store.current()          # RuleSet(version, probes). Reloads when the file changes.
new_version = store.append(probe)   # Adds a probe, bumps the version, saves safely.
```

- `current()` is cheap. Call it on every firewall check and edits show up with no restart.
- If someone saves broken JSON, it keeps the last good version and logs an error. The firewall never runs with zero rules.
- `append` raises `ValueError` if the probe id already exists.
- **Member 4:** self-heal writes probes with `added_by="neon"` through `append`. Validate first (the exploit must fire, 5 benign cases must not), as in the `firewall-rules` skill.
- **Member 3:** `rules.json` has `{"version": int, "probes": [...]}`. Each probe has `id`, `category`, `threshold`. Use `id` as the light label. `GET /api/rules` (Member 1) should just return this file.

### The 50 seed probes

| Category | Count | Gate result if one fires |
|---|---|---|
| injection | 9 | hard block |
| spend_hijack | 8 | hard block |
| coercion | 8 | hard block |
| split_payload | 8 (all combine image + audio + product data) | hard block |
| pack_lie | 8 | escalate to Neon swap |
| privacy | 3 | escalate (my proposal, see open questions) |
| promo_benign | 6 | escalate (my proposal, see open questions) |

- Every probe is a yes or no question where "yes" means risk, so high p is bad for every probe.
- Probes refer to the firewall inputs by name: `MEDIA`, `USER_INTENT`, `SHOP_PRODUCT_JSON`, `PROPOSED_TOOL_CALL`, `CLAIMS`.
- Every `pack_lie` probe needs `SHOP_PRODUCT_JSON`. When there's no product match, the firewall skips all of them (architecture decision 7).
- Promo probes don't fire just because a promo is visible. They only fire when the promo changed the cart (more items, a different product, an add-on). Threshold is 0.10, relaxed to 0.50 for carts under $40.
- Default threshold for everything else is 0.10.

## Task 7: firewall (`backend/firewall_decisions.py`)

```python
from backend.firewall_decisions import decide, gate, tier_for
v = await decide(intent, media, product_json, proposed_call, claims, rules_store.current(), cart_total)
```

- One backend call per state-changing tool call. Never raises: any failure returns a `Verdict`.
- **Fails closed.** Timeout (over `THRESHOLDS["firewall_timeout_ms"]`, 1500 ms), API error, input blocked by the content filter, missing media file, or a malformed/incomplete response gives `action="hard_block_quarantine"`, `probes=[]`, `action_probs={}`, and `error` set. **Member 3:** show "firewall error" when `error` is set.
- **Gate** (architecture decision 5): **any `create_spend_request` is always `hard_block_quarantine`** (team decision, Nov 21: nothing in our flow needs one; probes still run so Neon gets evidence). Otherwise hard block if any `injection | spend_hijack | coercion | split_payload` probe fires or severity is 3. Escalate if only `pack_lie | privacy | promo_benign` fire, or P(approve) < 0.92. Otherwise approve. A probe fires when p ≥ its threshold for the tier (`probe.tiers[tier]` if set, else `probe.threshold`).
- **Tiers** from the cart total only (works with no budget): `create_spend_request` → `spend_request`; > $150 → `high`; < $40 → `low`; else `normal`.
- **No product** (`product_json=None`): `pack_lie` probes are not sent and not in `Verdict.probes`. Injection and the rest still run. **Member 3:** the seismograph should show only the ids in `Verdict.probes`.
- `Verdict.probes` holds every probe that was sent, with `p` and `fired`. `Verdict.backend` says which backend produced it. `Verdict.latency_ms` covers the whole `decide` call.
- Backend switch: `FIREWALL_BACKEND=decisions|json_llm`. **Right now `decisions` blocks everything** because the SDK call is a TODO (see `docs/notes-apis.md`). The `json_llm` path is written but not run live yet. For json_llm, set `MODEL_FIREWALL` to a fast generate-content model.
- `cart_total`: pass the cart total for the call being checked. For `create_checkout` with only a `cart_id`, pass the total from the earlier `create_cart`.

## Task 8: Argon perception (`backend/perception_argon.py`)

```python
from backend.perception_argon import perceive
claims = await perceive(media)   # -> Claims
```

- Argon has no tools. `Claims` are untrusted: pass them to other models only as quoted data (the firewall wraps them in an `UNTRUSTED_CLAIMS` block). **Member 4:** never put `Claims` text into Neon's instructions; quote it as evidence.
- Never raises. Any error or malformed model output returns empty `Claims` with `notes="perception_error"`. No media returns empty `Claims` with `notes="no_media"` and makes no API call.
- Uses `MODELS["perception"]`, images at ultra_high, prompt in `backend/prompts/argon.md`. Not run live yet.
- There is no perception timeout in `config.py`, so the guarded shopper (Task 9) bounds it when it awaits the result.

## Coming next from me

| What | When | Interface |
|---|---|---|
| Task 9 C7 `run_guarded` | 1:00 | `async run_guarded(intent, media, product_ref, bus, run_id, shop, rules: RuleStore) -> GuardedResult` |

## What I need from others

- **Member 1:** `ShopMCP` and fixtures (11:45), the `shopper_loop` signature as soon as it's stable (code due 12:45), the real cart argument names from `tools_list.json`, and `backend/config.py` with `MODELS`, `THRESHOLDS`, `TIERS`, `FIREWALL_BACKEND`.
- **Whoever has the 10:00 resource sheet:** the exact firewall and Argon model IDs, and the Decisions API docs or sample code. If the Decisions API can't return a probability per question, we switch to `FIREWALL_BACKEND=json_llm`.
- **Member 4:** golden images for Task 7 in `eval/golden/`: `sticky_note.png`, `benign_blurry.jpg`, `promo_banner.jpg`.

## Open questions

1. Decided: when a `privacy` or `promo_benign` probe fires, the gate escalates to a Neon swap (not a hard block). Implemented in Task 7.
2. This branch is based on `dev` (Member 1 scaffold), so it merges into `dev` cleanly.
