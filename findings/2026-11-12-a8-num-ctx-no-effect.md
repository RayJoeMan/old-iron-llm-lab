# num_ctx is not a session variable (F-77)

- **Date:** 2026-11-12 (certified)
- **Platform:** Fortress — Windows/Vulkan Ollama lane, the
  :11435 (serve-second) instance only; see
  `platforms/fortress-provisional.md` for the machine
- **Source record:** FORTRESS-BACKLOG-2026-11-12.md item A8;
  on-box RESULTS, run `backlog-a-2026-11-12`

## Question

Does the context-window setting (num_ctx 8192 vs 16384
vs the config-of-record default) move the 3B's Trap-60
draw?

## Method

llama3.2:3b Trap-60 at num_ctx 8192 and 16384, then back
to the default; read conditional on A5 (a ctx change
forces a reload, and reload alone changes nothing —
F-74).

## Measured result

- All three settings: hash `b6db228d…` — **changes =
  false** across 8192, 16384, and default.

## Verdict

**CERTIFIED.** num_ctx is not a draw variable for this
instrument on this lane.
