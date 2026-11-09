# Per-card solo baselines on a mixed Maxwell+Turing pair — the RTX 4000 wins every solo class

- **Date:** 2026-11-08 (certified)
- **Platform:** Fortress — see `platforms/fortress-provisional.md`
- **Source record:** FORTRESS-TUNING.md **F-35**; experiments R10-1, R10-2
  (on-box results `r10_1.json`, `r10_2.json`, ledgered in R10-RUN-LEDGER.md)

## Question

Fortress ran for its whole pre-build life on one GPU (Quadro M4000,
Maxwell sm_52). With a Dell OEM Quadro RTX 4000 (Turing sm_75) installed
beside it, what is each card's standalone inference speed — decode and
prefill measured separately — on the lane's standard probe, and what
work is the older card still good for?

## Method

llama.cpp 0.9.0-dev b12136 (commit 2c192444c), CUDA 12.1 build,
Ollama-store GGUF blobs. Standard probe **B3**: 169-token prompt,
np 256, ctx 8192, temp 0.3, seed 42, `-t 4`, cache_prompt off;
1 warmup + 3 reps, medians; prompt-eval and eval tok/s reported
separately. Device order in this build is **CUDA0 = RTX 4000,
CUDA1 = M4000** (reversed vs nvidia-smi). The prefill-isolation arm
(R10-2) uses the longprobe prompt (4,241 tokens, np 48). Card identity
was VRAM-verified on every arm.

**Harness caveat, recorded in full:** the first arm's flat 51 °C M4000
temperature trace exposed a mask-order error in the harness itself —
`CUDA_VISIBLE_DEVICES` mask 0 addresses the RTX 4000 on this WSL stack
(matching llama.cpp's `--list-devices`, *not* nvidia-smi's index
order). The bisect that caught it, the correction, and the re-runs are
ledgered as R10-0b/R10-0c. Every figure below is from corrected arms.

## Measured result

| Model / arm | Prompt tok/s | Eval tok/s |
|---|---|---|
| qwen3:8b solo, RTX 4000 (ngl 99) — the R10 control | 1262.31 | **55.29** |
| qwen3:8b solo, M4000 (ngl 99) | 65.8 | **11.4** |
| qwen3:8b prefill isolation (4,241-tok prompt), RTX 4000 | **1441.42** | 50.53 |
| qwen3:8b prefill isolation (4,241-tok prompt), M4000 | **99.36** | 10.78 |
| ud-qwen3:14b solo (ngl 25), RTX 4000 | 73.52 | 2.67 |
| ud-qwen3:14b solo (ngl 25), M4000 | 24.81 | 2.37 |
| ud-qwen3:14b, RTX 4000 at ngl 30 (R10-3b) | 109.91 | 3.47 |
| llama3.2:3b solo, M4000 (ngl 99) | 162.91 | 22.09 |

- Decode separates the cards **4.85×** (55.29 vs 11.4); short-prompt
  prefill **19.2×**; long-prompt prefill **14.5×**. Tensor cores are a
  prefill multiplier, not just a decode one: the RTX's prefill *rises*
  with prompt length (1,262 → 1,441 tok/s) as batch efficiency rises,
  while the M4000's barely moves (65.8 → 99.36) — it is compute-starved,
  with no tensor cores.
- The 14B at partial offload decodes nearly card-independently
  (2.67 vs 2.37 — CPU-bound); its prefill is still 3× on the RTX.
  ngl 30 on the RTX (3.47) is the best single-card 14B number measured.
- Ambient across the whole battery: RTX ≤ 51 °C, M4000 ≤ 66 °C;
  no abort line approached.

## Verdict

**CERTIFIED.** The RTX 4000 is the primary lane in every solo class.
The M4000's solo value is prefill-light work and service as an
independent second lane (see the concurrency/replica finding, F-40);
it remains a competent small-model lane in its own right
(llama3.2:3b at 22.09 eval tok/s).
