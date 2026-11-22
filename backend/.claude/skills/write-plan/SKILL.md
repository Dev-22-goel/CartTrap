---
name: write-plan
description: Write or update CartTrap's plan.md from PRD.md and docs/architecture.md in Superpowers writing-plans format. Use when starting the build, after design changes, or to re-plan mid-hackathon.
---

# Write the plan

Follows Superpowers `writing-plans` (use that skill directly if installed). `plan.md` at the repo root is the plan location (overrides `docs/superpowers/plans/`).

## Required structure
1. Header: Goal, Architecture, Tech Stack, Spec (PRD.md + docs/architecture.md), and the line telling agentic workers to use subagent-driven-development or executing-plans.
2. **Global Constraints:** project-wide rules with exact values copied from the spec (thresholds, forbidden tools, tiers, freeze time).
3. **Review Focus:** the 5 inputs or failure modes the spec implies but no test covers, each with a named test added to the owning task.
4. Milestones with clock times (10:30 to 5:00).
5. Tasks: `### Task N: name — owner: <agent> (time)`, then **Files** (create/modify/test, exact paths), **Interfaces** (Consumes / Produces with exact signatures and types), then checkbox steps: write failing test (names + assertions) → run, expect FAIL → implement signature → run, expect PASS → commit.
6. Cut list and "never cut".

## Rules
- A task is the smallest unit with its own test cycle; fold setup and docs into the task that needs them.
- Steps decide things (names, values, tests); never "TBD", "handle edge cases", or full function bodies.
- No TDD for UI styling; verify UI with a Playwright screenshot instead.

## Self-review before handing over
Spec coverage (every P0 story has a task) · step scan · type consistency across Interfaces · Review Focus present · plan length proportional to the spec.
