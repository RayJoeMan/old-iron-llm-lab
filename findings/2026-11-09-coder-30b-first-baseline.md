# ud-qwen3-coder:30b first baseline — tied with the instruct MoE in the same placement

- **Date:** 2026-11-09 (certified)
- **Platform:** Fortress — see `platforms/fortress-provisional.md`
  (2026-11-08 fingerprint)
- **Source record:** FORTRESS-TUNING.md **F-57**; experiment R15-S5
  (on-box results `r15_s5.json`)

## Question

Does the coder build of the 30B MoE cost throughput against
the instruct build in the fleet's standard MoE placement?

## Method

ud-qwen3-coder:30b, dual layer split ts 1,1, standard B3
probe, llama.cpp b12136.

## Measured result

**prompt 108.0 / eval 22.18 tok/s** medians (eval reps
21.79 / 22.68 / 22.18); output coherence validated
(`content_coherent = true`); load 36.1 s; VRAM ~7,270 MiB
RTX / ~7,400 MiB M4000.

That is statistically tied with the instruct 30b-a3b in the
same configuration (104.73 / 22.57, F-37 family).

## Verdict

**CERTIFIED.** The coder build costs nothing in this
placement; model choice between the two 30B MoEs can be
made on output grounds alone.
