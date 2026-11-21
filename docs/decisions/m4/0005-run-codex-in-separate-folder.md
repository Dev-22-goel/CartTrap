---
status: accepted
date: 2026-11-21
decision-makers: "Adish (Member 4)"
informed: "Member 1 (merges adish to main)"
---

# Run Member 4's Codex work in a separate folder, merged into adish by Opus

## Context and Problem Statement

Member 4 splits work between Claude Code and Codex (Astra, Sol, Luna models) to save Claude quota and work in parallel. If both tools edit the same working copy, they overwrite each other's half-finished files. The team's merge rules (integration.md §5) assume one `adish` branch per member.

## Decision

- Codex works in its own folder, `CartTrap-codex`, a separate checkout of the repo. It owns only the files listed in `docs/integration-m4.md` §3 (the Codex lane), and never pushes to `main`.
- Member 4 merges Codex's work into `adish` using a Claude Opus plan turn: review, merge, then run the Haiku verifier. This happens at 11:40, 12:20, 1:15 and 3:15.
- To the team, nothing changes: Member 4 still delivers through `adish`, and Member 1 still merges `adish` into `main` at S1–S6.

## Consequences

* Good, because Claude and Codex never touch the same files at the same time.
* Good, because the team sees one Member 4 branch, as integration.md expects.
* Bad, because Member 4 spends about 5 minutes on each of the 4 merges.

## Implementation Plan

* **Affected paths**: none in the shared repo beyond the files each lane owns
* **Patterns to follow**: Codex writes status only to `handoff/codex-status.md`; it follows `AGENTS.md` and plan.md Global Constraints
* **Patterns to avoid**: Codex pushing to `main` or to other members' branches; Codex in full-access sandbox mode

### Verification

- [ ] `git log main --author` never shows Codex commits that didn't come through `adish`
- [ ] Each merge is followed by an `m4-spec-verifier` PASS
