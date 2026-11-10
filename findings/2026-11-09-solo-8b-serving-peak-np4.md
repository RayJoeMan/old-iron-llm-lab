# Solo-8B serving on the RTX peaks at 4 slots — 2.05× single-stream

- **Date:** 2026-11-09 (certified)
- **Platform:** Fortress — see `platforms/fortress-provisional.md`
  (2026-11-08 fingerprint)
- **Source record:** FORTRESS-TUNING.md **F-54**; experiment R15-S2
  (on-box results `r15_s2.json`)

## Question

How does solo 8B serving scale with server slots on the
fast card — and where does the aggregate peak?

## Method

qwen3:8b solo on the RTX 4000, llama.cpp b12136, `-np` swept
1 / 2 / 4 / 8, concurrent B3 batches, wall-clock aggregates.

## Measured result

| Slots | Wall aggregate (tok/s) |
|---|---|
| np1 | 52.46 |
| np2 | 83.25 |
| np4 | **107.68** |
| np8 | 101.44 |

Aggregate throughput peaks at np4 — **2.05× the np1 wall
figure** — and recedes at np8. The batch spread at high slot
counts is wide and is part of the record: np4 wall batches
{74.04, 107.68, 110.82}, np8 {98.79, 129.29, 101.44}. The np1
wall figure (52.46) sits in family with the F-35 timings
control (55.29). RTX post-arm temp up to 79 °C; VRAM
~6,050 MiB.

## Verdict

**CERTIFIED.** 4 slots is the solo-RTX serving sweet spot
for the 8B on this host.
