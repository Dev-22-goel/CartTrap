# Member 4 startup: Claude Code + Codex (do in order)

Each step lists what you run and what "done" looks like. Decisions behind these steps: ADRs m4/0005, m4/0006, m4/0007.

## A. Tonight / before 10:00

1. **Install the 5 pending skills** (PowerShell, one at a time):
   ```powershell
   npx -y skills add trailofbits/skills --skill spec-to-code-compliance --skill property-based-testing -g -a claude-code -y
   npx -y skills add mattpocock/skills --skill git-guardrails-claude-code -g -a claude-code -y
   npx -y skills add affaan-m/ECC --skill eval-harness -g -a claude-code -y
   npx -y skills add skillrecordings/adr-skill -g -a claude-code -y
   npx -y skills add skillrecordings/adr-skill -g -a codex -y
   ```
2. **Turn off unused connectors** in claude.ai → Settings → Connectors (Apollo, Clay, OpenSEO, Bright Data, Vercel, Gamma, Canva, Taplio, Sentry, Gmail, Calendar, Notion), and the `data` and `upstash` plugins.
3. **Make `CartTrap` a git repo on `adish`.** Pick the case that fits.
   - *Team repo already exists on GitHub:*
     ```powershell
     cd D:\Documents\Desktop\CartTrap
     git init
     git remote add origin <TEAM_REPO_URL>
     git fetch origin
     git checkout -b adish
     git reset origin/main
     git status
     ```
     `git reset` (without `--hard`) keeps your files and puts the team's history under them. In `git status`, keep **your** M4 files (`.claude/agents/m4-*.md`, the 3 upgraded agents, `.claude/settings.json`, `docs/decisions/m4/`, `docs/integration-m4.md`, `docs/member-4-plan.md`, `docs/m4-startup.md`, `handoff/`). For any *team* file that shows as modified, take the team's version: `git restore <file>`.
   - *No team repo yet:* `git init`, `git checkout -b adish`, `git add -A`, `git commit -m "chore: kit + m4 setup"`, then create the GitHub repo and push.
4. **Commit and push your M4 setup:** `git add -A; git commit -m "chore(m4): agents, ADRs, lane contract, plan"; git push -u origin adish`.
5. **Create the Codex folder** (ADR m4/0005):
   ```powershell
   cd D:\Documents\Desktop
   git clone <TEAM_REPO_URL> CartTrap-codex
   git -C CartTrap-codex checkout -b m4-codex origin/adish
   ```

## B. 10:00–10:30 checks

6. **Claude check.** Open `claude` in `CartTrap`. Approve the Context7 server when asked. Paste the contents of `handoff/claude-RESOLVE.md`. Done = `SETUP: READY`.
7. **Codex check.** In a second terminal, from `D:\Documents\Desktop\CartTrap`:
   ```powershell
   codex exec -m gpt-6.2-sol -s workspace-write -C ..\CartTrap-codex (Get-Content handoff\codex-RESOLVE.md -Raw)
   ```
   Done = `CODEX SETUP: READY`.
8. **If either check says a package is missing:** `pip install hypothesis pytest-asyncio numpy vcrpy` in the team venv, and tell Member 1 (ADR m4/0007).
9. **Post** `docs/integration-m4.md` in the team channel and get OKs on ADRs 0001–0004 and 0007 before S1 (11:00).
10. **Model IDs:** when the 10:00 resource sheet lands, check them against `backend/config.py` (Member 2 / Member 1 own it).

## C. 10:30: GO
Run the two commands in `docs/member-4-plan.md` §7. Codex then follows the merge points in `handoff/m4-lane-contract.md` §3.

## If something goes wrong
| Symptom | Fix |
|---|---|
| Codex says it can't write files | You forgot `-s workspace-write` |
| Codex can't find the briefs or ADRs | Step 4 wasn't pushed, or step 5 wasn't based on `origin/adish`. In `CartTrap-codex`: `git pull origin adish` |
| A Claude agent runs on Opus unexpectedly | Check `/agents`; don't set `CLAUDE_CODE_SUBAGENT_MODEL` |
| Merge conflict at a merge point | Someone edited the other lane's file. Keep the owning lane's version (lane contract §1), then re-run `m4-spec-verifier` |
