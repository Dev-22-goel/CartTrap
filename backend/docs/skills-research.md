# PRD / spec skills research (Nov 20, 2026)

Goal: pick a way to write a PRD, design doc and task plan for CartTrap that Claude Code agents can then build from, on a hackathon timeline.

## What's out there

| Option | What it produces | Popularity | Fit for a hackathon |
|---|---|---|---|
| **GitHub Spec Kit** (`github/spec-kit`) | `/speckit.specify` → spec, `/speckit.plan` → plan/architecture, `/speckit.tasks` → small testable tasks, `/speckit.implement`. Optional clarify/analyze/checklist. Markdown in git, agent-neutral (Claude Code, Gemini CLI, Copilot). | ~100k stars (per DataCamp, May 2026) | **Best match.** Its three outputs map 1:1 to PRD, design doc, plan.md. Skip constitution/checklist to cut ceremony. |
| **Superpowers** (`obra/superpowers`) | `brainstorming` (≈10 questions → spec), `writing-plans` (DoD, file map, numbered tasks), `subagent-driven-development` (test-first per task + reviewer subagent). | Very popular plugin | Great execution loop. Good to pair with Spec Kit-style docs. |
| **awesome-copilot `prd`** (`github/awesome-copilot`) | Interview (≥2 clarifying questions) then a 5-part PRD: exec summary, UX, AI requirements, tech spec, risks. | ~24.6k installs | Good PRD-only step; has an "AI requirements" section that suits a Gemini app. No tasks. |
| **BMAD-METHOD** | Six role agents (analyst, PM, architect, UX, dev...), PRD → architecture → epics/stories with readiness gate. | ~47k stars | Too much overhead for a weekend. Its role-agent idea is worth borrowing. |
| `deanpeters/Product-Manager-Skills` prd-development | 10-section PRD via one-question-per-turn interview, 2-4 day process. | 8.1k stars | Overkill; nice Assumption / Open Question tagging. |
| Small skills.sh PRD skills (write-a-prd, plan-prd, prd-writing) | Interview-first PRDs, some output to GitHub issues. | 2-5 installs each | Too unproven. |

## Decision

Use a **Spec Kit-shaped flow, hand-rolled as local skills** so there is nothing to install during the hackathon:

1. `PRD.md` (Spec Kit "specify" + awesome-copilot's AI-requirements section + Assumption/Open-Question tags)
2. `docs/architecture.md` (Spec Kit "plan")
3. `plan.md` (Spec Kit "tasks" + Superpowers Definition of Done per task)
4. Role agents in `.claude/agents/` (borrowed from BMAD, trimmed to what a small team needs) that build from those docs.

The skills in `.claude/skills/` (`write-prd`, `write-design-doc`, `write-plan`) encode this flow so the team can regenerate or extend the docs later. If the team prefers the official tooling, `uvx --from git+https://github.com/github/spec-kit.git specify init carttrap` and `/plugin install superpowers@claude-plugins-official` give the same shape.

## Reconciling with the Gemini chat's suggestion
The Gemini chat recommended `grill-me` + Superpowers (`brainstorming`, `writing-plans`, `executing-plans`, `dispatching-parallel-agents`, `verification-before-completion`, `systematic-debugging`) + Anthropic's `frontend-design` and `mcp-builder`, and skipping Spec Kit/BMAD as too heavy. That agrees with this decision: we use Spec Kit's *shape* (spec → plan → tasks) but not its tooling, and the PRD/design/plan are already written, so the brainstorming/grill-me steps are done. On hackathon day, use Superpowers for **execution** (executing-plans over `plan.md`, verification-before-completion), and `frontend-design` for the arena UI. The local `write-*` skills are for updating the docs if scope changes.

## Sources
- https://github.blog/ai-and-ml/github-copilot/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/
- https://www.datacamp.com/tutorial/spec-driven-development-with-claude-code
- https://claudemarketplaces.com/skills/github/awesome-copilot/prd
- https://claudeskills.info/skills/deanpeters/Product-Manager-Skills/prd-development/
- https://www.skills.sh/petekp/claude-code-setup/write-a-prd
- https://skills.sh/navidemad/claude-code-plugins/plan-prd
- https://www.skills.sh/meriley/claude-code-skills/prd-writing
