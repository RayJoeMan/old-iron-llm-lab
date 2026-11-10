# The 14B split's serving throughput flattens after 4 slots

- **Date:** 2026-11-09 (certified)
- **Platform:** Fortress — see `platforms/fortress-provisional.md`
  (2026-11-08 fingerprint)
- **Source record:** FORTRESS-TUNING.md **F-53**; experiment R15-S1
  (on-box results `r15_s1.json`)

## Question

The 14B dual layer split decodes at 12.43 tok/s single-stream
(F-37). What does concurrent serving buy — how far does the
aggregate climb as server slots (`-np`) increase?

## Method

llama.cpp b12136, ud-qwen3:14b dual layer split ts 2,1,
server `-np` swept 1 / 2 / 4 / 8, concurrent B3 batches.
All figures are **wall-clock aggregates** (the F-45 rule);
timings sums appear only parenthetically.

## Measured result

| Slots | Wall aggregate (tok/s) | Timings median (tok/s) |
|---|---|---|
| np1 | 11.62 | 12.58 |
| np2 | 18.07 | 19.86 |
| np4 | 24.99 | 28.12 |
| np8 | 26.96 | 30.16 |

The np4 wall figure replicates the F-45 control (25.09)
almost exactly. Gains flatten beyond 4 slots (+8% to np8).
VRAM ~6,660 MiB RTX / ~4,320 MiB M4000; post-arm temps
≤65 °C / ≤64 °C.

## Verdict

**CERTIFIED.** Four slots is the 14B split's serving point;
eight slots buys +8%, not another doubling.
