---
status: accepted
date: 2026-11-21
decision-makers: "Adish (Member 4)"
informed: "Member 3 (scoreboard labels)"
---

# Eval cases carry poisoned_modality and a hijack-type vector

## Context and Problem Statement
The generated dataset (plan v3, approved) poisons exactly one modality per item: image, video, audio or text. The old 5-vector vocabulary (`sticky_note`, `pack_lie`, `pdf_spend`, `voice_coercion`, `split_payload`) doesn't describe that split.

## Decision
Every case carries `poisoned_modality` (`image|video|audio|text|none`) and a `vector` naming the hijack (`qty_hijack|spend_hijack|promo_hijack`, or `none` for benign). The old vectors stay valid as legacy labels for the hand-shot sticky-note set. Metrics and the scoreboard group by `poisoned_modality`.

## Consequences
* Good, because results show which modality the firewall misses, which is the hackathon's "show where it breaks" ask.
* Neutral: Member 3's scoreboard can group by `poisoned_modality`. The labels are plain strings.

### Verification
- [ ] Every frozen case has `poisoned_modality`, and the results JSON reports per-modality ASR
