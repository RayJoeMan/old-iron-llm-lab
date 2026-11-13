# Load history does not move the 3B draw (F-75)

- **Date:** 2026-11-12 (certified)
- **Platform:** Fortress — Windows/Vulkan Ollama lane, the
  :11435 (serve-second) instance only; see
  `platforms/fortress-provisional.md` for the machine
- **Source record:** FORTRESS-BACKLOG-2026-11-12.md item A6;
  on-box RESULTS, run `backlog-a-2026-11-12`

## Question

Does an eviction-and-reload history (a larger model
taking the slot in between) change the 3B's draw beyond
the plain reload rate?

## Method

llama3.2:3b evicted by a qwen3:14b load, reloaded,
Trap-60; 4 cycles, read against A5's reload baseline
(F-74).

## Measured result

- All 4 draws: hash `b6db228d…`, strict **47/60** —
  `changed = false`, **span 0**, identical to the plain
  reload cycles.

## Verdict

**CERTIFIED.** Allocator/placement history via eviction
is not a session variable for the 3B on this lane.
