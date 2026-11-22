---
status: accepted
date: 2026-11-21
decision-makers: "Adish (Member 4)"
informed: "Member 3 (scoreboard)"
---

# The eval report groups metrics by poisoned_modality

## Context and Problem Statement
ADR 0017 gave every case a `poisoned_modality`. The runner ignored it, so results showed one ASR per system and hid which modality the firewall misses.

## Decision
- `CaseResult.poisoned_modality` is copied from the case JSON (`None` if absent).
- `Report.by_modality` is `{system: {modality: Metrics}}`, built with `eval.metrics.summarize`. Cases without a modality (the legacy hand-shot set) and errored cases are left out of the groups; the per-system totals still include scored legacy cases.
- `ATTACK_VECTORS` gains `qty_hijack`, `spend_hijack`, `promo_hijack`; `BENIGN_VECTORS` gains `none`. `build_cases` keeps generating only the legacy vectors (new `LEGACY_*` lists), so the 30+20 stub set is unchanged.
- The CLI prints one line per system and modality under the main table.

## Consequences
* Good, because the results file shows per-modality ASR.
* Neutral: `by_modality` defaults to `{}` when reading older results files.

### Verification
- [x] `tests/test_run_eval.py::test_report_groups_metrics_by_poisoned_modality`
