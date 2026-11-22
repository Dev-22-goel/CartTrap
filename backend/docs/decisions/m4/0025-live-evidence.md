---
status: proposed
date: 2026-11-21
informed: "Member 1 (API), Member 2 (trace schema), Member 3 (UI), Member 4 (defender)"
---

# Serve localized evidence after a guarded block

The shopper needs to see where an instruction appeared in an attachment. The template fraud card is emitted immediately. The defender then starts localization and the safe swap concurrently. Either result can reach the shopper first. The handler joins both tasks before the run stream closes.

## Event contract

The guarded pane emits one `evidence` event with `data.items` in upload order when at least one attachment yields a location. Treat quotes and transcripts as untrusted display text.

| Modality | Item fields | Display coordinates or timing |
| --- | --- | --- |
| Image | `modality`, `text`, `box`, `crop_bounds`, `crop_url` | Both boxes are [top, left, bottom, right] on the original display-oriented image, normalized to 0–1000. Map the instruction box into the crop by subtracting the crop origin and dividing each axis by the corresponding crop extent. The JPEG includes 15% padding per edge, clipped to the source. |
| Video | `modality`, `text`, `t_s`, `box`, `frame_url` | `t_s` is seconds from the start. Draw the normalized box on the full extracted JPEG frame. |
| Audio | `modality`, `transcript`, `start_s`, `end_s`, `duration_s`, `peaks`, `segment`, `clip_url` | Times refer to the source WAV. The 200 peaks span the entire recording and are relative to its loudest absolute PCM sample across all channels. Highlight the half-open bucket range `[segment[0], segment[1])`. The WAV URL plays just the selected interval. |

The URLs use `/api/evidence/{run_id}/{file}`. Artifact names are `crop_N.jpg`, `frame_N.jpg`, or `clip_N.wav`. N is the zero-based index in the original attachment list. The route checks the names and resolved paths before serving a file from `runs/evidence/{run_id}`.

## Localization

Claims describe the run as a whole and can be unavailable at block time. Each attached image, video and audio file is therefore a candidate. Each receives one tool-free Interactions call to the configured perception model with quoted claims. A JSON null means no instruction could be located in that file. PDFs are outside this contract.

Model calls and media extraction share a 12-second deadline. An error or timeout yields an empty result for the batch. The safe swap keeps its own deadline. Successful localization supplies display evidence and has no effect on the firewall decision.

## Cross-member changes

- Member 1's `backend/main.py` imports and includes `evidence_router`.
- Member 4's `backend/defender_neon.py` starts the evidence task after the template card.
- **Pending Member 2 change.** The closed `TraceEvent.kind` literal in `backend/schemas.py` needs the value `"evidence"` for the real bus to accept the event. The EV handoff grants ownership of the router and hook but omits the shared schema. The EV checkout currently leaves this change to the owner pending authorization.

## Verification

Offline tests exercise all three artifacts through the API, padding, timestamps, stereo waveform bins, null matches, error handling, the shared timeout, and path rejection. An additional check extracted a JPEG from a locally generated MP4 at 1.2 seconds with the installed ffmpeg. The real TraceBus ordering test currently fails at schema validation. See [the EV status](../../../handoff/codex-status-EV.md) for the suite output.
