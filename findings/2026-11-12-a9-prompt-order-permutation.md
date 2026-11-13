# Prompt order: the 3B's misses are item-intrinsic; the 8B's are not (F-78)

- **Date:** 2026-11-12 (certified)
- **Platform:** Fortress — Windows/Vulkan Ollama lane, the
  :11435 (serve-second) instance only; see
  `platforms/fortress-provisional.md` for the machine
- **Source record:** FORTRESS-BACKLOG-2026-11-12.md item A9;
  on-box RESULTS, run `backlog-a-2026-11-12`

## Question

Are the Trap-60 baseline misses properties of the items
themselves, or of their position in the bulk prompt?

## Method

Trap-60 in the 3 frozen permutations (seeds 101/102/103),
llama3.2:3b and qwen3:8b, scored title-mapped against the
8-title baseline miss set {4, 8, 22, 40, 49, 50, 52, 56}.
Bar: item-intrinsic iff ≥70% of baseline misses recur in
≥2 of 3 permutations; position effect iff second-half
miss rate ≥2× first-half.

## Measured result

- **3B recurrence: 8 / 7 / 8 of the 8 baseline misses**
  recur in the three permutations — the item-intrinsic
  clause is met in every permutation.
- **8B recurrence: 2 / 2 / 1** — the clause is not met;
  the 8B's baseline misses do not follow the items.
- Per-half counts as recorded — 3B: [14, 10], [10, 12],
  [18, 7]; 8B: [2, 1], [2, 2], [2, 3] — show no
  consistent second-half excess in either model, so the
  position-effect clause fires for neither.

## Verdict

**CERTIFIED.** Same instrument, two different failure
kinds: the 3B misses *these titles* wherever they sit;
the 8B's misses are session/draw artifacts that move
when the order does.
