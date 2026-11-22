---
status: accepted
date: 2026-11-21
decision-makers: "Adish (Member 4)"
informed: "Member 3 (frontend owner), Member 1 (stream API owner), eval-engineer"
---

# Align the frontend with backend trace and eval reports

## Context

The shopping API emits a final `system` event after its selected panes finish. The frontend only closed streams for pane-specific completion, so EventSource could reconnect and replay completed runs. The shopper and guarded verdicts also use Shop MCP payload shapes that the older frontend fixtures only partially represent.

Member 4 is updating Member 3's frontend under the whole-app extension of ADR 0019. These changes cover task F1 in the integration plan. [ADR 0019](0019-member4-does-m1-m2-wiring.md), [Full-app integration plan](../../full-app-integration-plan.md)

## Decision

- `src/types.ts` models the `system` pane, guarded verdict metadata, safe-cart variant IDs, and the extra eval report fields.
- `src/api.ts` closes on system completion and retains pane-specific completion for existing callers. A system terminal event also satisfies the single-agent runner's completion check.
- `src/state.ts` finishes all three panes on system completion. For tool calls and interceptions, it reads top-level arguments, then nested result arguments, then the legacy fixture alias. Reported spend takes precedence over local calculation, and an explicit victim hijack flag takes precedence over the intent check. A guarded verdict supplies the spend for the pending call matching its tool.
- `src/lib/spend.ts` reads nested cart lines and variant IDs. The reducer keeps compact catalog variants available for the spend fallback. When a spend request lacks a flat dollar amount, the calculator converts its approval limit from cents.
- `src/api.ts` keeps per-modality metrics and error counts. Reports with `meta.sample: true` use the empty-results shape expected by the frontend. [ADR 0013](0013-align-c6-results-json.md), [ADR 0015](0015-live-shop-only-for-eval.md)

## Consequences

The frontend accepts enriched events as well as recorded events and nested backend payloads. An intercepted cart may still have unknown spend if the event omits a total and the catalog trace lacks the referenced variant price. Task F2 can consume the per-modality metrics through `EvalResults`.

## Verification

- [x] `npx vitest run` passed all 63 tests, including 11 new contract regressions in `src/state.test.ts`.
- [x] `npx tsc -b --noEmit` passed across the frontend.
