# Member 2 integration notes (firewall track)

Branch: `Udaya`
Owner: Member 2 (Udaya)
Status: C1, C4, Task 7 firewall, Task 8 Argon and **Task 9 C7 `run_guarded` done and wired into `/api/run`**. `origin/dev` (Member 1) is merged into `Udaya`. Nothing has run against the live Gemini APIs yet (no key in the build container): run `uv run python scripts/check_decisions.py` with a key first.

Run the tests: `uv sync` then `uv run pytest -q`. My tests are test_intent, test_money, test_rules, test_firewall_gate, test_perception, test_product_match, test_guarded and test_main_wiring. The full suite (with Member 1's) is 187 offline tests.

## What's ready

| Contract | Files | Who uses it |
|---|---|---|
| C1 schemas, intent, spend math | `backend/schemas.py`, `backend/intent.py`, `backend/money.py` | everyone |
| C4 rules store and 50 seed probes | `backend/rules.py`, `backend/rules.json` | Member 3 (probe names for the lights), Member 4 (self-heal `append`), me (firewall) |
| Task 8 Argon perception | `backend/perception_argon.py`, `backend/prompts/argon.md` | me (guarded shopper), Member 4 (Neon can quote `Claims` in the fraud card) |
| **C7 guarded shopper** | `backend/guarded_shopper.py`, `backend/product_match.py`, wired in `backend/main.py` | Member 1 (`/api/run`), Member 4 (`after_block` hook for Task 10), Member 3 (verdict/log events), eval |
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
- **Added after the merge (all optional, nothing renamed):** `Claims.product_description` (Argon's short search query for the product shown, used for camera matching), `Verdict.model` (e.g. `gemini-decision-1`) and `Verdict.confidence` (calibrated confidence of the firewall_action answer).
- `Verdict.error` is `None` normally. When the firewall fails closed (timeout, bad response) it holds the reason and `action` is `hard_block_quarantine`. The UI should show "firewall error" when it's set.
- `TraceEvent.pane` is `victim | guarded | redteam | system` (`system` is only for the final `done` event, from Member 1's `main.py`). `kind` is `tool_call | tool_result | intercepted | verdict | fraud_card | log | done`. Anything else fails validation.

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
attempted_spend(call: ToolCall, products: dict[str, dict]) -> float   # DOLLARS, 2 dp
```

- Returns **dollars** (the spend tiers are $40/$150). Shop money is integer **cents** and is converted inside.
- **Real Shop shapes (tested):**
  - `create_cart`: `{"shop": ..., "cart": {"line_items": [{"item": {"id": variant_id}, "quantity": n}]}}`. The price is looked up by `item.id`.
  - `create_spend_request`: `{"spend_request": {"approval_limit": cents, "totals": [{"type": "total", "amount": cents}]}}`. Uses the larger of `approval_limit` and the `total`, i.e. the most it could spend.
- `products` can be `ShopperContext.variants` (`variant_id -> {"price_usd": 19.99, ...}`, what the guarded shopper passes), raw Shop variants (`{"price": {"amount": 1999, "currency": "USD"}}`, read as cents), or `ShopperContext.products` (`product_id -> raw product`; its variants are searched).
- **Member 4:** Dollars Defended = `attempted_spend(blocked_call, ctx.variants)` minus the safe cart total (Shop `totals` are cents, so divide by 100).
- Older flat shapes still work (`lines`, `product_id`, prices like `19.99` / `"19.99"` / `{"amount": "19.99"}`). Unknown prices count as 0. It never raises.
- `create_checkout` with only a `cart_id` returns 0. The guarded shopper uses the last approved cart total then.

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
- Backend switch: `FIREWALL_BACKEND=decisions|json_llm`. `decisions` calls `gemini-decision-1` on the v1beta Decisions API; `json_llm` uses the Interactions API with `config.FIREWALL_JSON_LLM_MODEL` (env `MODEL_FIREWALL_JSON_LLM`, default `gemini-4-argon`). Call shapes are in `docs/notes-apis.md`. Neither has run live yet.
- Probe ids must match `[A-Za-z0-9_-]{1,64}` (Decisions API question keys). **Member 4:** `RuleStore.append` now raises `ValueError` for a bad id, so self-heal probes need ids like `neon_fake_receipt_v2`.
- A safety block from the API (HTTP 400) is a fail-closed hard block with `error` set.
- `cart_total`: pass the cart total for the call being checked. For `create_checkout` with only a `cart_id`, pass the total from the earlier `create_cart`.

## Task 8: Argon perception (`backend/perception_argon.py`)

```python
from backend.perception_argon import perceive
claims = await perceive(media)   # -> Claims
```

- Argon has no tools. `Claims` are untrusted: pass them to other models only as quoted data (the firewall wraps them in an `UNTRUSTED_CLAIMS` block). **Member 4:** never put `Claims` text into Neon's instructions; quote it as evidence.
- Never raises. Any error or malformed model output returns empty `Claims` with `notes="perception_error"`. No media returns empty `Claims` with `notes="no_media"` and makes no API call.
- Uses `MODELS["perception"]` (`gemini-4-argon`) via the Interactions API with the `Claims` JSON schema, images at `resolution: "ultra_high"`, prompt in `backend/prompts/argon.md`. Not run live yet.
- There is no perception timeout in `config.py`, so the guarded shopper (Task 9) bounds it when it awaits the result.

## C7: guarded shopper (`backend/guarded_shopper.py`)

```python
from backend.guarded_shopper import run_guarded, GuardedResult
res = await run_guarded(intent, media, product_ref, bus, run_id, shop=ShopMCP(), rules=RuleStore("backend/rules.json"))
# GuardedResult(verdicts, blocked_call, approved_calls, claims, product_json)
```

- Wired into `/api/run` as `guarded_pipeline` in `main.py`, with a shared `RuleStore` and a live `ShopMCP()`. `main.py` now uses `parse_intent(request, budget)`. **Member 1:** those were the two TODOs; the diff is 15 lines.
- Uses Member 1's `shopper_loop` with `pane="guarded"`, the **same model (`MODELS["victim"]`) and the same prompt (`VICTIM_PROMPT`)** as the victim. The firewall is the only difference.
- Argon `perceive(media)` starts as a task at once and runs while the shopper searches. It is awaited before the first firewall check.
- Every state-changing call: `cart_total = attempted_spend(call, ctx.variants)`, product context, `decide(...)`, then a `verdict` event.
  - **Approve:** sent through the live shop (a real anonymous cart; `continue_url` is in the `tool_result`). `shop_mcp` still always intercepts spend requests and forbids `complete_*`.
  - **Anything else: the loop stops.** No more model or tool calls. A `log` event with `event: "stopped"` says why, then `after_block(...)` runs.
- **Product context (decision 7), in order:** the product looked up for `product_ref`; else a confident camera match (below); else the product of the variant being bought; else `None` (mismatch probes skipped).
- **Camera matching** (`backend/product_match.py`): only with no `product_ref`, an image attached and `FIREWALL_BACKEND=decisions`. Argon's `product_description` goes to `search_catalog`, then ONE Decisions API `choice` question over the image and the top 5 results plus `other`. It's used only if confidence >= `THRESHOLDS["product_match_min_confidence"]` (0.60). It runs in the background, never inside the firewall call. A `log` event with `event: "product_match"` reports the match and its confidence.
- **Member 4 (Task 10):** fill in `after_block(b: BlockContext)` in `guarded_shopper.py`, or pass `on_block=`. `BlockContext` has `intent, media, call, verdict, claims, product_json, cart_total, ctx (products, variants, shop), bus, run_id`. Emit `fraud_card` on pane `guarded`. If it raises, run_guarded logs the error and still returns.

**Events on pane `guarded`** (besides `shopper_loop`'s `tool_call` / `tool_result`):

| kind | data |
|---|---|
| `verdict` | `Verdict` fields (`action`, `probes`, `action_probs`, `severity`, `latency_ms`, `tier`, `backend`, `error`, `model`, `confidence`) plus `tool`, `cart_total`, `product_id` |
| `log` `event: "perception"` | `model` (gemini-4-argon), `instructions_detected`, `visible_text` (first 5), `pack_count_claim`, `notes`, `message` |
| `log` `event: "product_match"` | `model`, `confidence`, `choice`, `product_id`, `query`, `error`, `message` |
| `log` `event: "stopped"` | `model`, `action`, `tool`, `error`, `message` (last guarded event before `done`) |

Every `verdict` and every `log` I emit has a `model` field. The agent's final-text `log` comes from Member 1's `shopper_loop` and has none.

**Firewall additions:** `gate()` never approves when the `firewall_action` confidence is below `THRESHOLDS["min_confidence"]` (0.75). With consistent probabilities this can't change a result: approving already needs P(approve) >= 0.92, so confidence is already >= 0.92. It only matters when the API reports a confidence lower than its own probabilities. Argon now sends video with `processing: "agentic"` (frame scrubbing); the firewall does not.

## Gemini models used

| Model | Job | Where in the code |
|---|---|---|
| `gemini-4-hydrogen` (`MODELS["victim"]`) | Shopper for **both** panes (fair comparison) | `backend/shopper_loop.py` (Member 1), via `victim_hydrogen.py` and `guarded_shopper.py` |
| `gemini-4-argon` (`MODELS["perception"]`) | Perception: media to untrusted `Claims` (no tools; video uses agentic processing) | `backend/perception_argon.py::_call_argon` (Interactions API) |
| `gemini-decision-1` (`MODELS["firewall"]`) | Firewall: every probe as a noul question, plus `firewall_action` and `attack_severity`, in one call | `backend/firewall_decisions.py::_call_decisions` (Decisions API v1beta) |
| `gemini-decision-1` (`MODELS["firewall"]`) | Camera product match: one choice question over image + top 5 catalog results | `backend/product_match.py::match_product` (same `_call_decisions`) |
| `config.FIREWALL_JSON_LLM_MODEL` (default `gemini-4-argon`) | Firewall fallback when `FIREWALL_BACKEND=json_llm` | `backend/firewall_decisions.py::_call_json_llm` (Interactions API) |
| `gemini-4-neon` (`MODELS["defender"]`) | Fraud card, safe swap, self-heal (Member 4, Task 10) | `after_block` hook in `backend/guarded_shopper.py` |
| `gemini-4-carbon` (`MODELS["redteam"]`) | Red team (Member 3/4) | not built yet |
| `gemini-nano-banana-2.1` (`MODELS["imagegen"]`) | Attack images (forge) | not built yet |

Rules kept: model IDs only in `config.py`; no temperature, top_p, top_k or thinking_budget on Gemini 4 calls; `thinking_level` is `low` for Argon and `minimal` only for the json_llm fallback, which switches to `low` if pointed at Hydrogen or Neon.

**Latency set-up:**
- `backend/gemini.py` creates each genai client (default and v1beta) **once per process**, lazily, and every call reuses it. A client keeps its HTTP connection pool, so warm calls skip the TLS handshake.
- On FastAPI startup, `main.py` fires `firewall_decisions.warm_up()` in the background: one tiny Decisions call that opens the connection. A failure is only logged, and startup never waits for it. It's skipped with no key or with `FIREWALL_BACKEND=json_llm`.
- `FIREWALL_TIMEOUT_MS` (env, default 1500) sets `THRESHOLDS["firewall_timeout_ms"]`. Fail-closed behaviour is unchanged.
- `uv run python scripts/check_decisions.py` runs 6 calls on one client: (a) 1 question, (b) the full firewall request, (c) the full request plus an image, each twice. It prints every latency and the warm p50.
- **Member 1:** `shopper_loop` creates a new `genai.Client` per run (`client or genai.Client(...)`), so the Hydrogen shopper pays for a fresh connection on each run. It doesn't affect the firewall, but `backend.gemini.client()` would reuse one.

**Decisions API with our key:** it works (Udaya confirmed). Member 1 saw that `gemini-decision-1` isn't in `models.list()`; it's served on v1beta and just unlisted. A cold single call from a fresh process took 1547 to 1688 ms, over the 1500 ms timeout, which is why the client reuse and warm-up above exist. `FIREWALL_BACKEND` is still `decisions`.

## Coming next from me

| What | When | Interface |
|---|---|---|
| Task 15 fix with Member 4 | 2:30 to 3:15 | tune on `eval/golden/` only |

## What I need from others

- **Member 1:** `ShopMCP` and fixtures (11:45), the `shopper_loop` signature as soon as it's stable (code due 12:45), the real cart argument names from `tools_list.json`, and `backend/config.py` with `MODELS`, `THRESHOLDS`, `TIERS`, `FIREWALL_BACKEND`.
- **Whoever has the 10:00 resource sheet:** the exact firewall and Argon model IDs, and the Decisions API docs or sample code. If the Decisions API can't return a probability per question, we switch to `FIREWALL_BACKEND=json_llm`.
- **Member 4:** golden images for Task 7 in `eval/golden/`: `sticky_note.png`, `benign_blurry.jpg`, `promo_banner.jpg`.

## Open questions

1. Decided: when a `privacy` or `promo_benign` probe fires, the gate escalates to a Neon swap (not a hard block). Implemented in Task 7.
2. This branch is based on `dev` (Member 1 scaffold), so it merges into `dev` cleanly.
