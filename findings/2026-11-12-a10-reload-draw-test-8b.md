# The 8B's 49/60 is not reload-borne: five cycles, span 0 (F-79)

- **Date:** 2026-11-12 (certified)
- **Platform:** Fortress — Windows/Vulkan Ollama lane, the
  :11435 (serve-second) instance only; see
  `platforms/fortress-provisional.md` for the machine
- **Source record:** FORTRESS-BACKLOG-2026-11-12.md item
  A10; on-box RESULTS, run `backlog-a-2026-11-12`

## Question

Is qwen3:8b's standing 49–50 Trap-60 split a product of
unload/reload cycles (the A5 test, run on the 8B)?

## Method

qwen3:8b unload → reload → Trap-60, 5 cycles, same
protocol as A5 (F-74).

## Measured result

- All 5 draws: hash `0bfdc8e8…`, strict **49/60** —
  `changed = false`, **span 0**.

## Verdict

**CERTIFIED.** The 8B's 49 is a stable property of the
draw, not a reload artifact — the same null reload
result as the 3B (F-74), on the model where the question
mattered more.
