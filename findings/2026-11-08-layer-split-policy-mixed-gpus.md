# Layer-split policy on a mixed pair: split only what doesn't fit; weight layers toward the fast card; tensor split is a dead end here

- **Date:** 2026-11-08 (certified)
- **Platform:** Fortress — see `platforms/fortress-provisional.md`
- **Source record:** FORTRESS-TUNING.md **F-37**; experiments R10-1
  (arm e), R10-3b (on-box results `r10_1.json`, `r10_3b.json`)

## Question

On two dissimilar 8 GB cards joined only by PCIe (GPU↔GPU topology
SYS, cross-socket, no NVLink), when does llama.cpp layer split
(`-sm layer`) help, how should the split proportions
(`--tensor-split`, in device order CUDA0 = RTX 4000, CUDA1 = M4000)
be set, and is the experimental tensor split (`-sm tensor`) worth
anything on this pair?

## Method

Same lane and probe conventions as the solo baselines (F-35):
llama.cpp b12136, B3 probe, medians of 3 reps after 1 warmup. The 8B
split is judged against the RTX-only control (55.29 eval tok/s). The
tensor-split one-shot ran `-sm tensor -fa on -ctk f16 -ctv f16
-c 8192`, with output text validated coherent at both proportions
before any number was trusted.

**Declared substitution (research config 5):** the benchmark plan
called for a 14B Q3-on-one-card vs Q4-split comparison. No 14B Q3
GGUF was on hand and the run's 2 GB download cap forbade fetching one
(~8.5 GB), so the one-card arm is the on-hand UD-14B (Q4_K_XL) at max
fit (ngl 30). The substitution is declared here and wherever the
comparison is reported; no Q3 14B number exists in this battery.

## Measured result

**Splitting a model that fits the fast card loses, heavily:**

| Config | Prompt tok/s | Eval tok/s |
|---|---|---|
| qwen3:8b, dual layer split ts 1,1 | 118.86 | 14.27 |
| qwen3:8b, RTX 4000 only (control) | 1262.31 | **55.29** |

The split runs at **−74%** of the single-card control. A model that
fits the RTX runs there alone; the second card's value is
concurrency/replicas (F-40), not splitting.

**For the 14B, which fits neither card alone, the split is the
unlock — and the proportion is a first-order knob:**

| ud-qwen3:14b dual layer split | Prompt tok/s | Eval tok/s |
|---|---|---|
| ts 1,1 (even) | 65.71 | 8.69 |
| ts 3,2 | 81.95 | 9.83 |
| ts 2,1 (RTX-weighted) | 102.59 | **12.43** |

ts 2,1 is **+43%** over the even split and **3.6×** the best
single-card run (3.47 at ngl 30, declared substitution above); it
also beats Ollama's own dual-GPU read of the same model taken the
same day (7.88–8.58). The mechanism: decode on a layer split is a
serial sum of per-card stage times, so proportions must follow
*measured card speeds* (here a 4.85× decode ratio, F-35), not VRAM
symmetry — both cards have 8 GB, so the default ~50/50 split
systematically overloads the Maxwell card.

**Tensor split: runs, validates, loses.**

| ud-qwen3:14b tensor split | Prompt tok/s | Eval tok/s |
|---|---|---|
| ts 1,1 | 53.64 | 5.32 |
| ts 3,2 | 60.64 | 5.62 |

Tensor mode executed on the mixed sm_52+sm_75 pair with no error and
coherent output at both proportions — but at ~**2.2× slower** than
the best layer split.

## Verdict

**CERTIFIED policy:** split only what doesn't fit; weight layers
toward the fast card by measured speed, not VRAM; tensor split is
functional but not useful on a SYS-topology PCIe pair with no
NVLink — do not revisit it without an interconnect change.
