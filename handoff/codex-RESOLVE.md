# One-time setup check for Codex (run once, before brief C1)

Run with:
```
codex exec -m gpt-6.2-sol -s workspace-write -C ..\CartTrap-codex (Get-Content ..\CartTrap\handoff\codex-RESOLVE.md -Raw)
```

You are Member 4's Codex lane for the CartTrap sprint. Don't write application code in this job. Report each step as PASS/FAIL with the output.

1. Run `git branch --show-current` (expected: `m4-codex`) and `git log -1 --oneline`. Run `git pull origin adish` (or merge it) so you have Member 4's docs. Then confirm these exist: `handoff/m4-lane-contract.md`, `handoff/codex-C1-metrics.md`, `handoff/codex-A2-runner.md`, `handoff/codex-L1-glue.md`, `handoff/codex-A1-selfheal.md`, `docs/decisions/m4/0001`…`0007`.
2. Read `handoff/m4-lane-contract.md`. In 5 lines, list the files the Codex lane owns and the 3 rules you consider most important.
3. Confirm the sandbox lets you write: create and delete `handoff/.codex-write-test`.
4. Confirm that the Context7 MCP server is available and that the Superpowers skills are visible to you (name one Superpowers skill you can see).
5. Run `python -c "import hypothesis, pytest_asyncio, numpy, vcr"` and `pytest --version`. Report any missing package. Don't install anything and don't edit requirements files.
6. Write a 5-line summary to `handoff/codex-status.md` and commit it on `m4-codex` with message `chore(codex): setup check`. Don't push to `main`.
7. Final line: `CODEX SETUP: READY` or `CODEX SETUP: BLOCKED — <reason>`.
