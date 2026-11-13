# Think-on collapses the 8B trap to 0/60 in every cycle (F-89)

- **Date:** 2026-11-12 (certified)
- **Platform:** Fortress — Windows/Vulkan Ollama lane, the
  :11435 (serve-second) instance only; see
  `platforms/fortress-provisional.md` for the machine
- **Source record:** FORTRESS-BACKLOG-2026-11-12.md item
  A20; on-box RESULTS, run `backlog-a-2026-11-12`

## Question

Does think-on help or hurt qwen3:8b on Trap-60, read
cross-session?

## Method

3 reload cycles of Trap-60 under think-on, per-label
readout. Bar: helps iff median ≥53 (≥+3 over the
think-off 49–50); hurts iff median ≤46.

## Measured result

- Stricts: **0, 0, 0** — per-label 0/12 in every label
  in every cycle (TEACHING / COMEDY / GRAPHIC-NOVEL
  ACTION / SPOT-THE-MISTAKE / SEASONAL all 0/12 ×3).
- The failure is total and format-shaped, the same
  collapse class Qwythos shows under think-on (F-87) —
  while the same model's think-on *plain* set is
  untouched (F-91).

## Verdict

**CERTIFIED.** Think-on hurts the 8B trap absolutely:
49–50 → 0. On this lane, think-on and the trap
(amended-prompt) contract do not coexist, for either
model tested.
