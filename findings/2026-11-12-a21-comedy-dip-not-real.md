# The COMEDY dip is not confirmed real (F-90)

- **Date:** 2026-11-12 (certified)
- **Platform:** Fortress — Windows/Vulkan Ollama lane, the
  :11435 (serve-second) instance only; see
  `platforms/fortress-provisional.md` for the machine
- **Source record:** FORTRESS-BACKLOG-2026-11-12.md item
  A21; on-box RESULTS, run `backlog-a-2026-11-12`

## Question

Is the 8B's apparent COMEDY weakness under think-on a
real think effect, or an artifact of the 60-bulk draw?

## Method

Plain COMEDY-12 subset: think-on ×3 reload cycles vs
think-off ×1. Bar: the dip is real iff think-on COMEDY
≤10/12 in ≥2/3 sessions with ≥1 overlapping missed item
**and** think-off is 12/12.

## Measured result

- The bar's precondition fails on its face: think-off
  COMEDY strict is **3/12**, not 12/12.
- Recomputed strict scores are identical across
  conditions: think-off **3/12**; think-on **3/12 in
  each of the 3 cycles**. The item verdict records
  `dip_real = false`.

## Verdict

**CERTIFIED — dip not real.** On the isolated COMEDY
subset there is no think-on deficit to explain: both
conditions score the same low 3/12. The bulk-draw
contrast that suggested a dip (F-89 vs F-91) does not
survive isolation as a COMEDY-specific effect.
