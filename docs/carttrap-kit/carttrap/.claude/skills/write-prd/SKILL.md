---
name: write-prd
description: Write or update CartTrap's PRD.md (product spec) from an idea, interview answers or feedback. Use when the product scope, users, features or success criteria change.
---

# Write the PRD

Spec Kit's "specify" step, with an AI-requirements section for the Gemini parts. The PRD says **what and why**, never the stack (that goes in `docs/architecture.md`).

## Steps
1. Read `PRD.md` if it exists, plus `AGENTS.md`. Update in place; don't start over.
2. If anything below is unknown, ask at most 3 clarifying questions in one message (problem, who it's for, what the demo must show). If the user says "best guess", guess and tag it.
3. Fill the template. Tag every guess inline as **[Assumption]** and every unresolved item as **[Open Q]**.
4. Keep it to what a hackathon can ship: every P0 must be demoable. Move the rest to "Later".
5. End by listing the open questions back to the user.

## Template
```
# CartTrap PRD
## 1. Summary            (2-3 sentences: what, for whom, why now)
## 2. Problem            (pain, evidence, who has it)
## 3. Users & personas   (1-2 personas, their job-to-be-done)
## 4. Goals / non-goals
## 5. User stories       (As a… I want… so that…) each with acceptance criteria (Given/When/Then), tagged P0/P1/Later
## 6. AI requirements    (which Gemini model/API does what, inputs, outputs, latency budget, failure/fallback, safety)
## 7. Demo script        (the 2-3 minute judge walkthrough, step by step)
## 8. Success metrics    (for the demo and for real users)
## 9. Risks & mitigations
## 10. Open questions
```

## Done when
Every P0 story has acceptance criteria, the demo script only uses P0 stories, and section 6 names a concrete model per feature.
