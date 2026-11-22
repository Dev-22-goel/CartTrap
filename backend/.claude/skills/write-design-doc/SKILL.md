---
name: write-design-doc
description: Write or update docs/architecture.md (CartTrap's technical design) from PRD.md. Use after the PRD changes or when choosing stack, data model, APIs or Gemini integration.
---

# Write the design doc

Spec Kit's "plan" step: turn the PRD into **how**. Every decision must trace back to a PRD story.

## Steps
1. Read `PRD.md` and the current `docs/architecture.md`.
2. Prefer boring, fast-to-ship choices. For each major decision note the alternative you rejected in one line.
3. Fill the template. Add a Mermaid diagram for the system and for the main sequence.
4. Flag any PRD story the design can't meet as **[Gap]** and tell the user.

## Template
```
# CartTrap architecture
## 1. Overview & diagram        (mermaid flowchart)
## 2. Stack & why               (table: layer, choice, rejected alternative)
## 3. Components                (responsibility, inputs/outputs, owner agent)
## 4. Data model                (entities, fields, storage)
## 5. API contracts             (endpoints / functions, request/response JSON)
## 6. Gemini integration        (model per task, prompts location, structured output schemas, function calling/tools, token+latency budget, fallbacks, keys handling)
## 7. Main flows                (mermaid sequence per P0 story)
## 8. Security & privacy
## 9. Testing strategy          (unit, prompt evals with golden inputs, demo smoke test)
## 10. Deployment               (where it runs, env vars, one-command deploy)
## 11. Decisions log            (ADR-style one-liners)
```
