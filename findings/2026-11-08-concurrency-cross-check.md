# Cross-check: lossless dual-card concurrency reproduces under the replica arrangement (substituted pair)

- **Date:** 2026-11-08 (certified)
- **Platform:** Fortress — see `platforms/fortress-provisional.md`
- **Source record:** FORTRESS-TUNING.md **F-48**; experiment
  R11-6 (on-box results `r11_6.json`)

## Question

F-40's most load-bearing operating claim — two cards run two
independent models at ~101% of the sequential sum, losslessly —
was measured in R10 with per-card server instances addressed
via `-dev CUDA0/CUDA1`. Does the result reproduce through a
different harness arrangement (one CUDA_VISIBLE_DEVICES-masked
instance per card, the replica arrangement), or was it an
artifact of the addressing mode?

## Method

llama.cpp b12136, B3 probe, two concurrent rounds, aggregate vs
a fresh sequential sum measured in the same run.

**Substituted pair (declared):** the specified hetero pair for
this cross-check was qwen3:4b (M4000) + qwen3:8b (RTX).
**qwen3:4b is absent from the on-box Ollama store** (verified
via `/api/tags`), and pulling it (~2.5 GB) would have breached
the run's 2.5 GB download cap on top of the qwen3:0.6b pull.
The substituted pair is **llama3.2:3b on the M4000 + qwen3:8b
on the RTX**, one CUDA_VISIBLE_DEVICES-masked instance per
card — the same model pairing as R10-4, which is what makes the
run a harness cross-check of the certified figure. **The
qwen3:4b hetero-replica measurement itself remains NOT RUN**
(see Verdict).

## Measured result

Fresh solo comparator in-run: 3B on M4000 prompt 163.41 / eval
**22.13** (R10's figure for the same arm: 22.09 — the harnesses
agree). Sequential sum with the 8B RTX control (55.29): 77.42.

Concurrent rounds: **77.99 / 77.74 aggregate** (RTX 55.34 /
55.12 + M4000 22.65 / 22.62) — **≈101% of the sequential sum,
lossless**, and a near-exact reproduction of the certified
R10-4 result for the same pairing (78.11 / 77.99) measured
through `-dev` addressing.

## Verdict

**CERTIFIED (the cross-check).** F-40's lossless-concurrency
finding is independent of harness and device-addressing mode:
masked-instance replicas reproduce the `-dev` instance numbers
to within run variance. **Explicitly NOT RUN:** the qwen3:4b
hetero-replica measurement as originally specified — it waits
on the model being present in the store within a download
budget, and no qwen3:4b concurrency figure is claimed anywhere
in this program until it is measured.
