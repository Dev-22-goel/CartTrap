---
status: accepted
date: 2026-11-21
decision-makers: "Adish (Member 4)"
informed: "Member 1"
---

# Define one written lane contract that both Claude Code and Codex read before every job

## Context and Problem Statement

Member 4 splits work between Claude Code agents and Codex (Astra, Sol, Luna). A 2026-11-21 audit of the setup found these gaps:

1. `AGENTS.md` (read by both tools) still lists the old team ownership. For example, it says `defender-engineer` owns self-heal and `redteam-engineer` owns the Carbon loop. Codex would follow that and edit Claude-lane files.
2. Codex can't see `.claude/skills/` (no `.agents/skills` link), but brief A1 told it to "use skills firewall-rules and attack-forge".
3. `codex exec` defaults to a **read-only** sandbox, so the briefs as written would fail to write files.
4. Claude has deny rules (`.claude/settings.json`); Codex has none. After the 2:30 freeze, nothing stops a Codex job from editing `eval/cases/`.
5. The Codex folder is a separate clone. ADRs, briefs and the upgraded agents exist only in the `CartTrap` folder until they're committed and pushed, so Codex would read stale or missing files.
6. Three agents listed a Context7 tool (`get-library-docs`) that doesn't exist. The real tools are `resolve-library-id` and `query-docs`.

## Decision

- `handoff/m4-lane-contract.md` is the single source of who owns which file, and the rules both tools follow. Every Codex brief begins with "Read handoff/m4-lane-contract.md first", and every Member 4 Claude agent's guardrails point to it. The team file `AGENTS.md` is **not** edited; the contract overrides it for Member 4 work only.
- Codex reads skills by path (`.claude/skills/<name>/SKILL.md`). No junction is needed.
- Every Codex job runs with `-s workspace-write -C ..\CartTrap-codex`. Never `danger-full-access`.
- Freeze rule for Codex: after 2:30 PM, no Codex brief may list any path under `eval/cases/` or `eval/holdout/`. The Haiku verifier checks `git diff --stat` on every merge.
- Before the first Codex job, all Member 4 docs are committed to `adish` and pushed, so the Codex clone can pull them (`handoff/claude-RESOLVE.md` step 4).
- Agent `tools:` lines now use the real Context7 tool names (done 2026-11-21).

## Consequences

* Good, because each tool has one place to check ownership, so the two lanes can't overwrite each other.
* Good, because the team's shared `AGENTS.md` stays untouched.
* Bad, because every brief carries an extra file to read (small).

## Implementation Plan

* **Affected paths**: `handoff/m4-lane-contract.md` (new), `handoff/codex-*.md` (prefix line), `.claude/agents/{eval,defender,redteam}-engineer.md` (Context7 names, contract pointer), `docs/member-4-plan.md` §7 (sandbox flags)
* **Patterns to follow**: Codex status only in `handoff/codex-status.md`; Claude status only via `m4-handoff-scribe`
* **Patterns to avoid**: editing `AGENTS.md`; running Codex outside its own folder

### Verification

- [ ] `grep -L "m4-lane-contract" handoff/codex-*.md` returns nothing
- [ ] `grep -r "get-library-docs" .claude/agents` returns nothing
- [ ] The first Codex job reports `sandbox: workspace-write` and writes its files
- [ ] `git -C ..\CartTrap-codex log -1 -- docs/decisions/m4` shows the ADRs are present
