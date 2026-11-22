---
status: accepted
date: 2026-11-21
decision-makers: "Adish (Member 4)"
---

# Red-team events carry stage and message at the source

## Context and Problem Statement
ADR 0012 specified `data.stage` + `data.message` on every red-team event, but the loop only emitted `data.step`, so the RedTeam UI ignored live runs. The launch route also returned 404 without golden fixtures.

## Decision
`backend/redteam_carbon.py` emits `stage` and `message` on every event and keeps `step`: fixture_loaded->attack (message = manifest intended_hijack), blocked->blocked (+latency_ms, top_probe), bypass->bypass (+approve_p), probe_proposed->probe_proposed, validation->validate (`exploit {p,fired}`, `benign [{id,p}]`), probe_published->patched (`rules_version_from/to`), reblocked->reblocked, redteam_error->diagnose, done->done. Verdict events use stage `verdict`, which the UI ignores.

Cross-member changes (ADR 0019): the loop wraps any store with a `path` (shared `backend.rules.RuleStore`) so rules.json is copied to rules.json.bak before append. `selfheal._gemini_draft` now uses a `DraftSchema` without `extra="forbid"` (Gemini returned 400 on additionalProperties), thinking_budget 0, and `PROPOSAL_TIMEOUT_S` 20 (the draft took 20-40 s with default thinking). `evaluate_fixture` resolves relative media paths against the repo root. `record_round` keeps stage, message (<=240 chars, no URL), and public telemetry; the secrets test now plants its canary in `notes`, not `message`.

Fixtures come from `scripts/make_redteam_fixtures.py` (tuning set only, never the holdout). Round 3 (brand_lie_sticker with claims) is the attack the firewall approved live; validation is probabilistic, so a run can end with "failed validation" (seen once: gift_tag p=0.11 vs threshold 0.10).

## Verification
- [x] test_events_have_stage_and_message, test_patched_has_versions, test_validate_event_shape, test_shared_rulestore_backup_then_append
