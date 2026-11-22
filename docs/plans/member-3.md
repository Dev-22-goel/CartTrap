## Member 3’s Plan

### Task 11: Arena skeleton + event reducer — owner: arena-frontend (11:15, against fixtures)
**Files:** Create `frontend/src/state.ts`, `frontend/src/state.test.ts`, `frontend/src/api.ts`, `frontend/src/components/InputBar.tsx`, `TracePane.tsx`, `frontend/src/App.tsx`
**Interfaces:**
- Consumes: `TraceEvent` JSON shape (Task 3), routes (Task 4), fixture `run_attack.jsonl`.
- Produces: `type ArenaState = { victim: PaneState; guarded: PaneState; verdict?: Verdict; fraudCard?: FraudCard; done: boolean }`; `applyEvent(s: ArenaState, e: TraceEvent): ArenaState`; `startRun(form: FormData): Promise<string>`; `streamRun(runId, onEvent): () => void`.
- [ ] Step 1: Vitest: `applyEvent routes events to panes`, `intercepted event marks victim hijacked`, `verdict with error shows firewall error`, `done sets done`.
- [ ] Step 2: `npx vitest run` → FAIL. Step 3: implement; InputBar has webcam preview + Snap, push-to-talk that fills the Request box, attach-audio, URL, demo-product picker, budget, Run. Step 4: PASS; replaying the fixture renders both panes.
- [ ] Step 5: Commit `feat: arena skeleton + reducer`.

### Task 12: Seismograph, Fraud Card, Scoreboard — owner: arena-frontend
**Files:** Create `frontend/src/components/Seismograph.tsx`, `FraudCard.tsx`, `SafeCart.tsx`, `Scoreboard.tsx`
**Interfaces:** Consumes `ArenaState`, `GET /api/rules` (probe names), `GET /api/eval/latest` (`Metrics` per system, Task 14).
- [ ] Step 1: Build each against fixture state (no TDD for styling, per Global Constraints of the agent guide).
- [ ] Step 2: Verify with a Playwright screenshot at 1920×1080: all ~50 lights, fraud card (reason, evidence side by side, top probes, Dollars Defended), safe cart link, readable from 5 m (min 20 px body text).
- [ ] Step 3: Commit `feat: seismograph, fraud card, scoreboard`.

### Task 13: Attack forge — owner: redteam-engineer (11:15, parallel)
**Files:** Create `redteam/forge/{label,pack_lie,spec_pdf,voice,split_payload,all}.py`, `tests/test_forge.py`
**Interfaces:** Produces `forge(vector: str, product: dict, out_dir: str, variant: int = 0) -> ManifestEntry` with `ManifestEntry(id, vector, product_id, files: list[str], intended_hijack, forbidden: list[str], user_request, budget, label: Literal["attack","benign"])`; CLI `python -m redteam.forge.all --product <id> --out redteam/out/<run>`.
- [ ] Step 1: Tests: `test_each_vector_writes_files_and_manifest` (offline, with a local sample image), `test_split_payload_parts_benign_alone` (image text has no imperative to an agent; audio script references only the code word).
- [ ] Step 2: FAIL. Step 3: implement per the `attack-forge` skill. Step 4: PASS. Step 5: Commit `feat: attack forge`.

### Task 17: Demo hardening + README — owner: demo-verifier (4:00)
**Files:** Create `scripts/demo_check.py` (`make demo-check`), `README.md`; record fixtures for demo SKUs
- [ ] Step 1: `make demo-check`: one sticky-note attack → hard_block, one promo benign → approve. Then `USE_FIXTURES=1 make demo-check` with Wi-Fi off.
- [ ] Step 2: `grep -rn "complete_checkout\|complete_spend_request" backend/` hits only the guard and its test.
- [ ] Step 3: Run the PRD §7 script 3 times with a timer under venue light with real props.
- [ ] Step 4: README (pitch, diagram, model roles, eval table from latest results file, failure analysis, run steps, video link); repo public; `.env` not committed.
- [ ] Step 5: Commit `docs: readme + demo check`; human records the 1-min video and submits by 5:00.

### P1 extras if time allows (each its own small task, same TDD shape)
- US-10 spend tiers + `POST /api/runs/{id}/confirm` spoken confirmation — firewall-engineer.
- US-11 Exploit Forge via image gen (`POST /api/forge`) — redteam-engineer.

## Member 3 sync points (from integration.md)
- **Read first:** Global Constraints and Review Focus in `plan.md`.
- **Order:** Task 13 forge 10:30–11:45 (offline) → Task 11 11:45–1:00 → Task 12 1:00–2:30 → P1 extras/polish 2:30–3:15 → Task 17 3:15–4:45.
- **You deliver:** C5 `forge()` + `ManifestEntry` to Member 4 (11:45).
- **You need:** C3 `run_attack.jsonl` from Member 1 (11:30) then live API (12:30); C4 probe names from Member 2 (11:45); C6 `Metrics` JSON from Member 4 (sample at 1:00, live 2:00).
- **Owned files:** `frontend/**`, `redteam/forge/**`, `scripts/demo_check.py`, `README.md`. Send route changes to Member 1.
- **UI freeze at S6 (4:15):** after that, bugfixes only.
- **Checkpoints:** S1 11:00 · S2 1:00 · S3 2:00 · S4 2:30 · S5 3:15 · S6 4:15 · S7 4:45.
