# One-time setup check for Claude Code (paste into Claude in the CartTrap folder)

You are setting up Member 4's Claude Code lane for the CartTrap sprint. Do these steps in order. Don't write application code. Report each step as PASS/FAIL with the command output, in caveman style. Stop at the first FAIL that needs Adish.

1. **Contract.** Read `handoff/m4-lane-contract.md` and `docs/decisions/m4/*.md`. Confirm you understand which files the Claude lane owns.
2. **Agents.** Confirm these 10 agents load, and that each M4 agent has the intended model: eval-engineer, defender-engineer, redteam-engineer = sonnet; m4-failure-analyst = opus; m4-spec-verifier, m4-handoff-scribe = haiku. Confirm `.claude/settings.json` has `"model": "opusplan"` and the deny rules.
3. **Tools.** Call `mcp__context7__resolve-library-id` once for "google-genai" to prove Context7 works. Check that these skills are visible: superpowers, caveman, adr-skill, spec-to-code-compliance, property-based-testing, git-guardrails-claude-code, eval-harness, and the 8 kit skills. List any that are missing (Adish installs them; don't install them yourself).
4. **Git.** Run `git status` and `git branch --show-current`. Expected branch: `adish`. If the M4 files (`.claude/agents/m4-*.md`, the three upgraded agents, `.claude/settings.json`, `docs/decisions/m4/`, `docs/integration-m4.md`, `docs/member-4-plan.md`, `handoff/`) are uncommitted, commit them with message `chore(m4): agents, ADRs, lane contract, plan` and push `adish`. Don't commit `.env` or `.mcp.json` secrets (`.mcp.json` has no secrets; it's fine).
5. **Python.** Run `python -c "import hypothesis, pytest_asyncio, numpy, vcr"`. If it fails, write `requirements-m4.txt` with those 4 packages (ADR m4/0007) and report that Adish should run `pip install -r requirements-m4.txt`.
6. **Progress file.** Use the m4-handoff-scribe agent to create `.superpowers/sdd/progress.md` with rows T10, T14, T15, T16 (all "not started").
7. **Verdict.** Final line: `SETUP: READY` or `SETUP: BLOCKED — <what Adish must do>`.
