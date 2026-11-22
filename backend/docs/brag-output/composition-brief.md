# Hyperframes Composition Brief: CartTrap

## Objective
Create a 25-second launch-style brag video for CartTrap, an execution firewall for AI shopping agents.

## Output
- Composition directory: `brag-output/composition/`
- Rendered video: `brag-output/brag.mp4`
- Format: landscape — 1920x1080
- Duration: 25 seconds

## Source Material
- Project root: `E:\CartTrap`
- Primary files read: `index.html`, `src/index.css`, `src/App.tsx`, `src/components/Home.tsx`, `src/components/Arena.tsx`, `src/components/OutcomeStrip.tsx`, `src/components/FraudCard.tsx`, `src/components/Seismograph.tsx`, `src/components/SafeCart.tsx`, `src/components/RedTeam.tsx`, `README.md`, `PRD.md`, `docs/architecture.md`, `eval/results/latest.json`
- Product name: CartTrap
- Tagline / strongest claim: “An execution firewall for AI shopping agents.”
- Key UI or visual moment to recreate: the Compare arena with an unexpected order on the Assistant side and Safe Checkout's 50-probe seismograph, Fraud Card, localized evidence, and safe alternative on the protected side
- Copy that must appear verbatim:
  - “An execution firewall for AI shopping agents.”
  - “Held for review”
  - “Checked before money moves.”
  - “$312.16 protected”
  - “propose → validate → publish”

Use fictional demo product records only. Do not show live merchant names, customer data, checkout URLs, API details, or secrets.

## Creative Direction
- Tone preset: cinematic
- Creative direction: high-stakes security trailer built from a real commerce interface
- Interpretation: use full-scale type only at the hook and outro; the center is a dense but readable reconstruction of the actual dark-mode UI, with red reserved for the trap and Shopify green reserved for the protected path.
- Angle: an ordinary product photo becomes a crime scene, then CartTrap proves the intervention in its actual two-pipeline arena.
- Hook: “THE NEXT SHOPPING SCAM IS HIDING IN THE PHOTO.” with a red evidence box on a tiny instruction
- Outro / punchline: “CARTTRAP — THE EXECUTION FIREWALL FOR AI SHOPPING AGENTS. CHECKED BEFORE MONEY MOVES.”
- Avoid:
  - Generic SaaS language
  - Abstract filler visuals
  - Unrelated visual redesign
  - Aspirational PRD numbers or latency claims
  - Real product/customer records

## Visual Identity
- Background: `#141414`
- Text: `#e8e8e8`
- Accent: `#2fb985`
- Danger: `#ff6b5e`
- Surface: `#1e1e1e`
- Raised surface: `#262626`
- Lines: `#404040`
- Display font: Inter 900
- Body font: Inter 400/700
- Telemetry font: IBM Plex Mono 400/700
- Visual references from the project: Shopify-Polaris-inspired cards, the two-column Compare view, red evidence boxes, green Safe Checkout banners, mono probe labels, restrained 12px radii and hairline borders

LOOK: 2026 commerce-security control room; ground `#141414`, surface `#1e1e1e`, raised `#262626`, ink `#e8e8e8`, muted `#a8a8a8`, safe `#2fb985`, danger `#ff6b5e`; Inter 900 display, Inter 400/700 body, IBM Plex Mono 400/700 telemetry; card radius 12px, 1px `#404040` borders, no generic glass, no blue-purple gradient, no particle field, no fake 3D device.

## Storyboard
Use `brag-output/brag-plan.md` as the creative contract.

Scene summary:
1. The poisoned pixel — 2.73s — product/request card, hidden instruction, red evidence lock, hook line
2. Same request. Two agents. — 6.01s — faithful Compare arena, unexpected 24-item order, 50 checks illuminating
3. Evidence, not vibes — 4.37s — Fraud Card, evidence crop, listing comparison, `$312.16 protected`
4. Safe swap — 4.36s — quarantine the unsafe item, verified in-budget alternative, human-controlled continue button
5. It learns from the bypass — 5.46s — Carbon → Neon → rule v3→v4 → re-blocked
6. CartTrap — 2.07s — wordmark, grounded tagline and final promise

## Audio
- Audio role: cinematic support with sparse professional accents
- Audio arc: restrained threat → deterministic UI ticks → warm verdict → broader safe-swap release → strongest self-heal beat → clean logo fade
- Music: `assets/music/happy-beats-business-moves-vol-12-by-ende-dot-app.mp3`
- Music treatment: `data-volume="0.34"`, light fade-in, full level until 23.8s, fade to zero by 25s
- Music cue guidance: rich bundled preset at `C:\Users\saran\.codex\skills\brag\assets\music\cues\happy-beats-business-moves-vol-12-by-ende-dot-app.music-cues.json`; lock major moments at 8.74s, 17.47s, 22.93s. Use beat points 6.56, 7.09, 7.64, 8.19 for non-rushed probe accents.
- Audio-reactive treatment: subtle; extract 30fps/8-band data from the chosen local music and use it at build time to modulate only the evidence halo and safe-card presence by 0–4%.
- Audio-coupled moments:
  - Poisoned instruction — tiny glitch and evidence-lock impact
  - Probe grid — four low-risk clicks aligned with red-family reveals
  - Held-order verdict — warm impact at 8.74s
  - Safe cart — subdued bell
  - Rule v3→v4 and re-block — warm impact with strongest event at 17.47s
  - Final logo — restrained bell at 22.93s
- SFX selection guidance: prefer low/medium high-frequency-risk files; use `impactSoft_medium_*`, `interface/click_00*`, one tiny `glitch_002`, and one `impactBell_heavy_*`; avoid dense or repeated bright effects.
- SFX analysis guidance: `C:\Users\saran\.codex\skills\brag\assets\sfx\sfx-analysis.md`
- Exact SFX choice: Hyperframes should choose filenames, timestamps, density, and volume based on the implemented animation.
- Audio files: copy the chosen music and selected SFX into `brag-output/composition/assets/`.

## Hyperframes Instructions
Use the loaded `hyperframes`, `hyperframes-registry`, `media-use`, and `hyperframes-cli` skills. This is Brag's workflow: the plan and this brief replace generic storyline/SPEC/REVIEW steps. Do not propose storylines, write `SPEC.md`, or route into the generic launch-video workflow.

Requirements:
- Show the real CartTrap UI language and exact project copy, not a generic security dashboard.
- Keep all important text inside the 80% title-safe area and all content inside 90% action-safe.
- Root duration is exactly 25 seconds at 1920×1080 and 30fps.
- Include the planned music and sparse SFX layer.
- Use the bundled cue metadata only as timing hints; readability wins.
- Mark the 8.74s, 17.47s, and 22.93s major locks in source comments as `beat-locked`.
- Mark the 6.56s, 7.09s, 7.64s, and 8.19s probe sequence as `beat-grid`.
- Extract local audio data and use it to modulate existing evidence/safe-card glow subtly; no waveform or equalizer visual.
- Use local assets only; no remote fetches in the composition.
- Run the Brag gate: `hyperframes check --json` with expected text actually audited and zero errors before render.
- Open a background preview before the delivery render, verify its URL returns 200, then render locally at delivery quality.
