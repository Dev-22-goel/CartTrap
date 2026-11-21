---
status: accepted
date: 2026-11-21
decision-makers: "Adish (Member 4, doing Member 2's tuning per ADR 0019)"
informed: "Member 2 (owner of rules.json and the firewall)"
---

# Raise the probe thresholds off the noise floor and slim big PNGs before the firewall call

## Context and Problem Statement
Live tests today showed two failures:
- **The sticky note was blocked only because the firewall timed out** (1513 ms against the 1500 ms budget). The cause was the payload: a 1.1 MB PNG took 0.9–1.6 s per call, while the same pixels as a JPEG took 0.6–0.8 s.
- **Both benign goldens were hard-blocked.** Benign injection-probe scores sat at 0.10–0.27, but the seed thresholds were 0.10. Real injections score 0.85–0.95.

## Decision
- **Thresholds:** `backend/rules.json` goes from version 1 to version 2. Injection, spend_hijack, coercion and privacy probes move to a threshold of 0.30; pack_lie, split_payload and promo_benign move to 0.35. The gate is unchanged (approve iff p_approve ≥ 0.92 and no probe fires). No probe wording changed.
- **Image slimming:** a new `backend/gemini.py: slim_image()` re-encodes PNGs over 300 KB as q92 JPEG at the same pixel size. It never raises.
- **Timeout:** the 1500 ms fail-closed Global Constraint is **unchanged**. After the fix, p50 is ~487 ms and p95 ~831 ms (18 calls).
- **Tuning data:** this used `eval/golden/` only (allowed before and after the freeze), never `eval/cases/`.

## Consequences
* Good, because the sticky note now blocks on a real decision (error None), and both benign goldens approve.
* Bad, because the thresholds come from only 3 goldens, with a benign margin of about 0.27 against 0.30. They must be checked against the generated clean controls and the holdout. A Pillow dependency should also be declared in `pyproject.toml` (Member 1).

### Verification
- [x] `pytest -m live tests/test_firewall_live.py`: 4/4 passed twice
- [ ] Clean controls in the generated dataset approve at the new thresholds
