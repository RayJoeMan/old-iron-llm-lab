# Unload/reload is not a draw: six cycles, one hash, span 0 (F-74)

- **Date:** 2026-11-12 (certified)
- **Platform:** Fortress — Windows/Vulkan Ollama lane, the
  :11435 (serve-second) instance only; see
  `platforms/fortress-provisional.md` for the machine
- **Source record:** FORTRESS-BACKLOG-2026-11-12.md item A5;
  on-box RESULTS, run `backlog-a-2026-11-12`

## Question

Does unloading and reloading the 3B re-draw its Trap-60
output — the mechanism that could explain the record's
cross-session score span (57 / 53 / 40 / 40)?

## Method

llama3.2:3b keep_alive=0 unload → reload → Trap-60, 6
cycles; device placement logged per load. Bar: CHANGES =
reload is a session variable; the record is reproduced
only if the distinct-score span is ≥5.

## Measured result

- All 6 draws: hash `b6db228d…`, strict **47/60** —
  `changed = false`, **span 0**.
- Reloading never re-draws: every cycle lands on the
  same output, which is also the anchor's opening draw
  (F-71).

## Verdict

**CERTIFIED.** Reload is not a session variable for the
3B on this lane, and it does not reproduce the record's
span — the cross-session differences in the historical
record are not reload-borne.
