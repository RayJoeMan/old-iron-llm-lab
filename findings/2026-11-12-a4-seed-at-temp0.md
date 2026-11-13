# Seeds at temp 0: one hash for 43 / 1 / 1234 / 42 — and 42 does not restore the first draw (F-73)

- **Date:** 2026-11-12 (certified)
- **Platform:** Fortress — Windows/Vulkan Ollama lane, the
  :11435 (serve-second) instance only; see
  `platforms/fortress-provisional.md` for the machine
- **Source record:** FORTRESS-BACKLOG-2026-11-12.md item A4;
  on-box RESULTS, run `backlog-a-2026-11-12`

## Question

Is the seed live at temp 0 — and does returning to seed
42 restore the anchor draw?

## Method

llama3.2:3b Trap-60 at seeds 43, 1, 1234, then back to
42; hashes compared against the A2 anchor (F-71).

## Measured result

- All four seeds produced the **identical hash**
  (`3c06f862…`) — seed variation moves nothing at temp 0
  on this lane.
- The record flags `seed_live = true` (the seed parameter
  is accepted and tracked by the lane) and
  `return42_drift = true`: the return to seed 42 lands on
  the session's settled draw (`3c06f862…`), **not** on
  the anchor's opening draw (`b6db228d…`). What selects
  the draw is session history (F-72), not the seed.

## Verdict

**CERTIFIED.** At temp 0 the seed is not a draw variable
on this lane; "same seed" does not mean "same session
state."
