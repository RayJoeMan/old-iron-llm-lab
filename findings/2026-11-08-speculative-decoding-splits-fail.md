# Speculative decoding does not transfer to the splits: VRAM-infeasible with a GPU draft, collapsing with a CPU draft, crash-unstable on the MoE split

- **Date:** 2026-11-08 (certified)
- **Platform:** Fortress — see `platforms/fortress-provisional.md`
- **Source record:** FORTRESS-TUNING.md **F-43**; experiment R11-1
  (on-box results `r11_1.json`; server logs in `~/flane/r11/logs/`)

## Question

Speculative decoding pays +42% on the solo 8B (F-42). The fleet's
other serving shapes are splits — the 14B layer-split (ts 2,1) and
the 30B MoE dual split (F-37, F-38). Does the technique transfer
to either?

## Method

llama.cpp b12136, `--spec-type draft-simple`, B3 probe, warmup +
3 reps, medians. Three placements tried against the certified
controls (14B split: prompt 102.59 / eval 12.43; MoE dual split:
prompt 104.73 / eval 22.57):

1. 14B split + qwen3:0.6b draft pinned to the RTX (GPU draft),
   n-max {4, 8, 16}.
2. 14B split + draft on CPU (`--spec-draft-device none`,
   8 draft threads), n-max {4, 8, 16}.
3. MoE dual split + draft on CPU, n-max {4, 8}.

**Substituted draft (declared):** the original design called for
qwen3:4b as the MoE-split draft. qwen3:4b is **absent from the
on-box Ollama store** (verified via `/api/tags`), and pulling it
(~2.5 GB) on top of the run's qwen3:0.6b pull (0.52 GB) would
have breached the run's 2.5 GB download cap — so the same-family
qwen3:0.6b was substituted in arm 3, on CPU placement as planned
(the dual split's VRAM is full either way: 7,259 / 7,479 MiB used
of 8 GB per card). The substitution is labeled wherever its
numbers appear.

## Measured result

**Arm 1 — 14B split + GPU draft: cannot load at any draft
length.** The speculative (MTP) context requests 896.00 MiB on
CUDA0 for its KV buffer; the ts 2,1 split leaves less than that
free → `cudaMalloc failed: out of memory` →
`failed to allocate buffer for kv cache` →
`common_speculative_init_result: failed to create MTP context`.
A split target has no VRAM headroom for an on-card draft, full
stop.

**Arm 2 — 14B split + CPU draft: a collapse, monotone in draft
length.**

| Draft n-max | Prompt tok/s | Eval tok/s | Δ vs 12.43 | Acceptance |
|---|---|---|---|---|
| 4 | 29.06 | 3.67 | −70% | 0.5151 |
| 8 | 28.92 | 1.76 | −86% | 0.3035 |
| 16 | 29.04 | 1.21 | −90% | 0.1825 |

Two compounding causes: the 0.6b tracks the 14B target far worse
than the 8B (acceptance 0.52 vs 0.95 at n-max 4), and the
AVX-only CPU draft competes for the same cores the split's host
side needs. Prompt processing collapses too (102.59 → ~29).

**Arm 3 — 30B MoE dual split + 0.6b draft on CPU (substituted
draft):**

- n-max 4 completes at prompt 28.73 / eval **5.16** vs the 22.57
  control (**−77%**, acceptance 0.7692).
- **n-max 8 crashes llama-server during decode, reproduced 2/2
  attempts** (the original arm plus an identical-flags retry,
  both recorded in `r11_1.json`). The client sees
  `RemoteDisconnected`; the server log shows:

  `ggml-cuda.cu:111: CUDA error: out of memory` in
  `llama_context::decode` → `server_context_impl::decode` /
  `update_slots`, after which the process aborts.

  Mechanism: the dual split leaves only ~0.65–0.93 GiB free per
  card, which admits the 4-token verification batch's buffers
  but not the 8-token one.

## Verdict

**CERTIFIED.** Speculative decoding is a **solo-card technique
on this host** (F-42's configuration only). Do not attach drafts
to split targets in build 12136: GPU placement cannot allocate
the draft context at all, CPU placement runs 3–10× slower than
the target alone, and the MoE split is crash-unstable at
n-max ≥ 8. A clean loss everywhere it was tried — recorded as a
finding, not forced.
