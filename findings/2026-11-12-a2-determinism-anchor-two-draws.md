# The determinism anchor: three reps, two hashes — the first draw differs (F-71)

- **Date:** 2026-11-12 (certified)
- **Platform:** Fortress — Windows/Vulkan Ollama lane, the
  :11435 (serve-second) instance only; see
  `platforms/fortress-provisional.md` for the machine
- **Source record:** FORTRESS-BACKLOG-2026-11-12.md item A2;
  on-box RESULTS, run `backlog-a-2026-11-12`

## Question

Is a fresh-loaded model's Trap-60 output at the
classification config of record (temp 0, seed 42) identical
across in-session reps — the determinism premise the whole
M-series reads against?

## Method

Fresh load of llama3.2:3b, Trap-60 ×3 in-session, raw
response hashes compared. Pre-registered bar: 3 identical
hashes define the anchor H0; non-identical hashes refute
the premise as stated.

## Measured result

- Hashes: `b6db228d…`, `3c06f862…`, `3c06f862…` — **not
  identical**. The first rep differs; reps 2–3 agree.
- The bar's identical-hash premise therefore **fails as
  stated**: a session opens on one of (at least) two
  draws.
- The battery's later items bound what the two hashes
  mean: each is itself perfectly stable — six
  unload/reload cycles never leave the first hash
  (F-74), restarts and device pinning hold it (F-97,
  F-98) — so the variance is *which draw a session opens
  with*, not within-session noise. This is the Windows
  lane's sighting of the two-draw pattern the Mint lane
  certified as prompt-cache-selected (see the Mint
  de-noising band finding).

## Verdict

**CERTIFIED.** In-session determinism at temp 0 holds
*after* the opening draw; the opening draw itself is a
two-valued session variable. Every M-series read in this
battery is filed against that anchor.
