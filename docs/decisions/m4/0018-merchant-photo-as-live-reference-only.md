---
status: accepted
date: 2026-11-21
decision-makers: "Adish (Member 4)"
informed: "Member 1, Member 3"
---

# Merchant photos may be a live, in-memory reference for generation, never stored (amends ADR 0008)

## Context and Problem Statement
Adish wants both reference modes: product text plus our own reference images, and the merchant's photo as a visual reference. The Shopify rules forbid re-hosting merchant images.

## Decision
- Half of the items use `reference_mode: "text"`. They're generated from product text, with our own reference images as style refs.
- The other half use `reference_mode: "merchant_ref"`. The merchant image is fetched live, passed in memory to the image model, and **never written to disk, logged or committed**.
- Generated outputs are synthetic and carry a TEST-FIXTURE marker (PNG metadata plus a corner strip), with `synthetic: true` and the `reference_mode` in the manifest.
- If the team or the judges object, the `merchant_ref` items can be dropped by filtering on the manifest, without regenerating anything else.

## Consequences
* Good, because the props look closer to real listings, and the source of every item is traceable.
* Bad, because `merchant_ref` outputs are derivatives of merchant photos. That's disclosed in the README, and the items are easy to remove.

### Verification
- [ ] `test_merchant_image_never_written_to_disk` passes
- [ ] `git ls-files eval/props` holds no merchant image bytes (only generated files with the marker)
