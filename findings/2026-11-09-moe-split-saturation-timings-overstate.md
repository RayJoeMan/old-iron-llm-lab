# The MoE split saturates by np4 — and timings sums overstate it ~1.9×

- **Date:** 2026-11-09 (certified)
- **Platform:** Fortress — see `platforms/fortress-provisional.md`
  (2026-11-08 fingerprint)
- **Source record:** FORTRESS-TUNING.md **F-55**; experiment R15-S3
  (on-box results `r15_s3.json`)

## Question

Does concurrent serving lift the 30B MoE dual split the way
it lifts the dense models — and how far do the server's own
timings sums drift from wall-clock truth on this placement?

## Method

ud-qwen3-30b-a3b-2507 dual layer split ts 1,1, llama.cpp
b12136, `-np` swept 2 / 4 / 8, concurrent B3 batches,
wall-clock aggregates against timings sums.

## Measured result

| Slots | Wall aggregate (tok/s) | Timings sum (tok/s) |
|---|---|---|
| np2 | 20.11 | — |
| np4 | **23.56** | — |
| np8 | 20.64 | 43.71 (peak) |

The split saturates by np4, replicating F-45's saturation
read (np4 wall control 22.45). Timings sums reach 43.71 —
**~1.9× the honest wall figure**, the widest wall-vs-timings
gap in the program. VRAM ~7,260 MiB RTX / ~7,420 MiB M4000
(both cards near-full).

## Verdict

**CERTIFIED.** On the MoE split, timings sums must never be
headlined; the wall aggregate is the only honest serving
figure, and it stops growing at 4 slots.
