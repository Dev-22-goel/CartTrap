# F1 frontend contract alignment

Implemented seams S1–S6, S15, and S18 in Member 3's frontend under the whole-app extension of ADR 0019. [ADR 0022](../docs/decisions/m4/0022-frontend-contract-alignment.md)

- System completion closes the EventSource, finishes every pane, and satisfies the single-agent runner's terminal event check.
- Tool and interception rows accept nested arguments and use backend-reported dollar amounts when present. Compact catalog variants support the local spend fallback. Nested spend request limits convert from cents.
- Guarded verdicts attach cart totals to matching pending tool calls. Verdict and safe-cart types expose the new metadata.
- Eval normalization preserves per-modality metrics, per-system errors, and fail-closed counts. Marked sample reports produce an empty scoreboard.

## Verification

The test-first run reported 11 expected failures and 52 passing existing tests. The final run used the local dependencies with npm offline mode and ran the requested command chain through Windows Command Prompt.

```text
> npx vitest run && npx tsc -b --noEmit
Test Files  5 passed (5)
     Tests  63 passed (63)
```

The command chain exited 0. Verification was offline. Claude owns the commit on `m4-codex`.
