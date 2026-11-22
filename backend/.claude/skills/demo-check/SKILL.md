---
name: demo-check
description: Run CartTrap's pre-demo checklist - smoke test, offline fallback, props, timing of the 3-minute script. Use before 4:15 PM, before judging, and after any late change.
---

# Demo check

1. `make demo-check` (one sticky-note attack must block, one promo-banner benign must approve). Paste output.
2. `USE_FIXTURES=1 make demo-check` with Wi-Fi off.
3. Browser at 1920×1080 on the projector: both panes, seismograph, fraud card visible without scrolling.
4. Webcam test under venue light with real props: sticky note, fake "12-Pack" label, promo sticker. Use "Snap" for a still frame if motion blur.
5. Run the PRD section 7 script end to end with a timer: segment 1 ≤ 60 s, 2 ≤ 60 s, 3 ≤ 60 s. If the self-heal run exceeds 60 s, switch the button to replay the recorded trace.
6. `grep -rn "complete_checkout\|complete_spend_request" backend/` only hits the guard and its test.
7. Scoreboard shows the latest frozen-set results file, not a hand-typed number.
