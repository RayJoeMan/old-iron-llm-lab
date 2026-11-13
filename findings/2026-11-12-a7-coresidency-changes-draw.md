# Co-residency changes the 3B draw (F-76)

- **Date:** 2026-11-12 (certified)
- **Platform:** Fortress — Windows/Vulkan Ollama lane, the
  :11435 (serve-second) instance only; see
  `platforms/fortress-provisional.md` for the machine
- **Source record:** FORTRESS-BACKLOG-2026-11-12.md item A7;
  on-box RESULTS, run `backlog-a-2026-11-12`

## Question

Does holding a second small model resident beside the 3B
alter its numerics — i.e. is co-resident layout a session
variable?

## Method

qwen3:0.6b held resident (keep_alive 60m) beside
llama3.2:3b; Trap-60 ×3; hashes compared to the solo
anchor (F-71).

## Measured result

- Hashes: `b6db228d…`, `3c06f862…`, `3c06f862…` —
  recorded verdict **changes = true**.
- With a co-resident model, the session leaves its
  opening draw and settles to the second draw — the same
  selection pattern prefix history produces (F-72),
  unlike reload or eviction history, which change
  nothing (F-74, F-75).

## Verdict

**CERTIFIED.** Co-residency is a real session variable
on this lane: what else is resident can select which
draw the 3B serves.
