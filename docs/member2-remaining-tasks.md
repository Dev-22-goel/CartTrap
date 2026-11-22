# Member 2 (Udaya): remaining tasks

Updated: Sat Nov 21, 11:45 AM
Branch: `Udaya` on Dev-22-goel/CartTrap (based on `dev`)
Role: backend, firewall engineer

## Where things stand

| Task | What | Status |
|---|---|---|
| 3 | Schemas, intent parsing, spend math (C1) | Done, pushed |
| 6 | Rules store + 50 seed probes (C4) | Done, pushed |
| 7 | Firewall decide + gate, real Decisions API call | Done, pushed. **Not tested live yet** |
| 8 | Argon perception | Done, pushed. **Not tested live yet** |
| 9 | Guarded shopper `run_guarded` (C7) | **Not built. Due 1:00** |

Latest commit on GitHub: `c5b20a8`. Unit tests: 102 passed on the laptop.

## 1. Task 9: guarded shopper (due 1:00, top priority)

Member 1 and Member 4 are both waiting on `run_guarded`.

- [ ] Paste the Task 9 prompt and the Gemini add-on into Claude Code in one message
- [ ] Wait for the new bundle
- [ ] Download it, then pull and push (see "Bundle steps" below)
- [ ] Run `uv run pytest -q` and check everything passes
- [ ] Tell Member 1 that `run_guarded` is ready to merge into `dev`
- [ ] Tell Member 4 that `run_guarded` is ready for Task 10 and the eval

What the prompt covers:
- Merging Member 1's code from `dev` (Shop MCP client, trace bus, shopper loop, victim)
- Fixing the `schemas.py` conflict by keeping ours, and adding `"system"` to `TraceEvent.pane` so the stream doesn't hang
- Fixing `money.py` for the real Shop MCP shapes (cents, `cart.line_items[].item.id`, `spend_request.approval_limit`)
- Building `run_guarded` on Member 1's `shopper_loop` hook (`on_state_change`)
- Wiring it into `main.py` and switching `main.py` to `parse_intent`
- Gemini add-on: a confidence gate, product matching with Decision 1, Argon on video, a model name on every event, and a "Gemini models used" table

## 2. Prove the firewall works live

All 5 live tests skipped, so the real API hasn't been called yet.

- [ ] Run `uv run pytest -m live -rs` and read the skip reasons at the bottom
- [ ] If the reason is "GEMINI_API_KEY not set": check `.env` in the CartTrap folder has `GEMINI_API_KEY=...`
- [ ] If the reason is "golden image missing": wait for Member 4's images (step 3)
- [ ] Once they run: the sticky note gets `hard_block_quarantine`, the blurry benign image and the promo banner ($20 cart) get `approve_checkout`
- [ ] Write down the p50 firewall latency (target about 200 ms, p95 400 ms or less)

## 3. Get golden images from Member 4

- [ ] Ask Member 4 to push these to `eval/golden/`: `sticky_note.png`, `benign_blurry.jpg`, `promo_banner.jpg`
- [ ] Pull them, then rerun the live tests

## 4. Afternoon schedule

| Time | What |
|---|---|
| 1:00 | Task 9 delivered. Checkpoint S2 |
| 1:00 to 2:30 | Tune probes on `eval/golden/` only. Help with integration |
| 2:30 | Eval cases freeze (Member 4 runs it). **Never tune on `eval/cases/` after this** |
| 2:30 to 3:15 | Task 15 with Member 4: pick one real failure, fix it on golden, re-run |
| 3:15 to 4:15 | P1 US-10: spend tiers + `POST /api/runs/{id}/confirm` spoken confirmation, only if everything is green |
| 4:15 | UI freeze. Bug fixes only from here |
| 4:45 | Final merge + tag (Member 1) |
| 5:00 | Submission |

## 5. Open items to confirm with the team

- [ ] Gate rule: `privacy` and `promo_benign` probes escalate (not hard block). Tell the team
- [ ] Gate rule: every `create_spend_request` is always hard blocked. Tell the team
- [ ] Tell Member 1 the image model ID should be `gemini-nano-banana-2.1` in `config.py`
- [ ] Tell Member 1 the Decisions API image field is `resolution`, not `media_resolution` (architecture.md is wrong)

## Bundle steps (until Claude Code can push directly)

1. Download the bundle from Claude Code.
2. Check its name (it may be `Udaya-update (2).bundle`):
   ```
   dir "$HOME\Downloads\*.bundle"
   ```
3. Pull and push:
   ```
   cd C:\Users\udaya\CartTrap
   git checkout Udaya
   git pull "$HOME\Downloads\<bundle name>" Udaya
   git log --oneline -3
   git push
   ```
4. If `uv` isn't recognized in a new terminal:
   ```
   $env:Path = "$HOME\.local\bin;$env:Path"
   ```

## Optional: stop using bundles

Either of these lets Claude Code push for you:
- Install Claude Code on the laptop: `irm https://claude.ai/install.ps1 | iex`, reopen the terminal, then run `claude` in the CartTrap folder. It uses your own GitHub login and can see your API key.
- Or ask the repo owner (Dev-22-goel) to install the Claude GitHub App on the repo.

## Safety rules (never break these)

- Never call `complete_checkout` or `complete_spend_request`. Never send `create_spend_request`.
- The firewall fails closed: any timeout, error or bad response blocks.
- Argon never gets tools. Its output is data, not instructions.
- Never commit `.env`. Crop the API key out of screenshots.
- After 11:00, `schemas.py` only gets new optional fields.
