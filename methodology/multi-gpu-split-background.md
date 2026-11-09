# Background brief — multi-GPU split strategies for llama.cpp

> **BACKGROUND RESEARCH — NOT A FLEET FINDING.** This brief condenses a
> web-research synthesis (deep-research report read 2026-11-09,
> sources cited inline as [S#]). Every number below was measured by
> *someone else, on other hardware*, and is transferred to the
> Fortress scenario **by mechanism, not by direct evidence**: no
> published benchmark of the exact Maxwell+Turing pair exists. This
> brief exists to explain where the R10 battery's benchmark list came
> from (see the 2026-11-08 Fortress findings in `findings/` for what
> the fleet itself measured) and to record the published claims —
> including the folklore — that the battery was designed to test.

Scenario the research addressed: llama.cpp / Ollama, two dissimilar
PCIe-only GPUs (Maxwell 8 GB, no tensor cores + Turing 8 GB, tensor
cores), dual-socket AVX-only Xeon host, 128 GB RAM; dense 8B/14B and
a 30B MoE (Qwen3-30B-A3B class).

## Layer split buys capacity, not single-stream decode speed

Layer split (`-sm layer`, the default and the only mode Ollama uses)
is a sequential pipeline: contiguous layer slices per card, one
activation handoff (~16 KB) per token boundary. Measured decode is
flat as cards are added — Llama 3 70B Q4_K_M generation: 14.71 tok/s
on 1× RTX A6000, 16.57 on 2× RTX 3090, 17.07 on 4× 3090, 19.22 on
2× RTX 4090, 18.94 on 8× 4090 [S4]. Prefill is the exception: it
scales with cards in layer split (an 8K prompt got faster at each
step from one to six 3090s), because many prompt tokens fill the
pipeline [S5]. Project guidance agrees: layer split "can tolerate
slow interconnect speeds"; its priority is fast prefill [S1].

**Folklore flag:** calculator/guide sites that model layer-split
bandwidth as *summing* across cards ("effective bandwidth = Σ × 0.85")
contradict both the documented mechanism and the flat measured
series — treat as estimates, not measurements [S10].

## Split proportions follow measured speed, not VRAM

For layer split at batch 1, time per token ≈ Σ (bytes on card *i* ÷
bandwidth of card *i*) — a serial sum of stage times. The default
split is proportional to device memory, which for two equal-VRAM,
unequal-speed cards degenerates to ~50/50 and overloads the slow
card. Measured on an asymmetric V100 pair (16 GB + 32 GB): a wrong
tensor-split proportion collapsed performance from 39.9 to 26.1
tok/s, erasing the entire split advantage [S8]. Recommendation from
the synthesis: sweep `--tensor-split` around the *speed* ratio
(e.g. 1,1 → 3,2 → 2,1, fast card first), capped by the fast card's
VRAM headroom [S1][S8][S9].

## Tensor split: real evidence both ways

Tensor split (`-sm tensor`, experimental, merged 2026-04-09 in
PR #19378) splits weights and KV of every layer and all-reduces
across the interconnect (~2 synchronisations per layer per token).
It requires flash-attention on, unquantised KV, and a manually set
context size [S1][S3].

- **For:** 2× RTX 3090 on PCIe Gen3, no NVLink — Llama 3.3 70B
  Q4_K_M decode 19.5 (layer) → 31.9 tok/s (tensor, 1.64×); Qwen3 32B
  1.69× [S2]. On 4× RTX 4090, 70B decode 21.25 → 48.31 (2.27×) [S4].
- **Against:** in PR #19378's own 2× RTX 4090 table, a MoE model
  lost heavily (prefill 0.39×, decode 0.70×) and small dense models
  lost on prefill (0.48–0.76×) [S3]. On a Turing pair (2× modded
  RTX 2080 Ti), tensor alone bought +1.2% — "nothing" [S6].

Synthesis: tensor split is a per-model experiment, weighted by model
type and interconnect — not a plan.

## Row split is gone

Row split synchronised after *every operation*; its one documented
niche was old, slow GPUs (dual Tesla P40: row 12–14 tok/s vs layer
~7 on a 72B) [S7]. Its CUDA implementation was **removed in July
2026 (PR #24216)** — current builds fail at load with `device CUDA0
does not support split buffers` [S2][S6]. Any guide recommending
`-sm row` predates the removal.

## MoE: CPU expert offload and the GPU expert cache

Qwen3-30B-A3B Q4_K_M is ~17.3 GB of weights — more than two 8 GB
cards combined — so expert offload is structural at Q4, not a tuning
choice. `--cpu-moe` puts all routed experts in RAM; `--n-cpu-moe N`
offloads the first N layers' experts [S11][S12].

- **The knee rule (measured):** offload the *minimum* that makes the
  model genuinely fit. If the model already fits, every added
  offloaded layer costs monotonically (GLM-4.5-Air IQ4_XS tg 60.84
  at ncmoe 8 → 25.08 at ncmoe 64) [S12].
- **Folklore correction:** the famous ~4.87× "offload speedup"
  (11.09 → 54.04 tok/s) was a broken baseline — the model didn't fit
  and the Windows driver silently paged VRAM over PCIe; offload
  stopped the thrashing, it didn't accelerate anything [S12].
- **On this VRAM class (measured):** RTX 2080 8 GB, Qwen3-30B-A3B
  Q4_K_M — settled config `--n-cpu-moe 34` gave ~41 tok/s at
  ~6.5 GB VRAM, on a much faster CPU than this scenario's [S15].
- **Expert cache (`--moe-cache-mib`, PR #29887, merged 2026-10-07;
  multi-GPU PR #30112):** an LRU VRAM cache for host-resident
  experts; hits run the expert matmul on GPU, misses upload over
  PCIe; applies only to batches ≤ 32 tokens (decode) [S13][S14].
  Author's measurements (Qwen3.8-Flash-Next, PCIe 4.0): decode
  1.57×–2.20× at 72–89% hit rates, cache sized ~10% of expert size;
  prefill cost 0.73×–0.91×. A post-merge 2-GPU regression (decode
  halved at a 43.5% hit rate) is also on record — review-thread
  consensus: the cache pays only at ≳75% hits [S14].

## NUMA: cross-socket costs are real — where the CPU touches weights

Cross-socket RAM reads measured at ~38% of local bandwidth
(53.7–54.6 vs 136–143 GB/s, dual Xeon 8360Y) [S22]. The founding
llama.cpp measurement (issue #1437, CPU inference): one socket
146.6 ms/token; naive dual-socket 253.7 (73% *slower*); interleaved
111.9 [S21]. GPU↔GPU topology code **SYS** means cross-card traffic
traverses the inter-socket link [S24]; in a tensor-parallel serving
post-mortem, per-GPU throughput fell ~43% the moment a TP group
crossed sockets [S25]. Guidance: NUMA matters most for
CPU-offload configs (experts in RAM), least for fully GPU-resident
models; `distribute` vs `isolate`-to-the-GPU's-socket is a two-run
A/B, not a doctrine [S8][S21].

## Replicas beat splits for models that fit one card

Ollama's documented behaviour already prefers a single GPU when the
model fits ("typically provides the best performance") [S19]. Two
independent per-card instances never synchronise and never wait on
each other: a dual RX 6800 eGPU study measured 164.3 tok/s aggregate
with independent instances while a split of one model across the
same cards segfaulted on that topology [S20]. Batching is the
in-server analogue: on the dual-P40 system, layer-split aggregate
rose 8.46 → 12.8 → 15.0 tok/s at 1 → 2 → 4 parallel slots —
aggregate throughput, not per-stream latency [S7].

## Sources

All read 2026-11-09. Confidence labels per the research report:
**primary** = project docs/PRs; **measured** = a named run with
numbers; **index** = via search index/summary; **model** = estimate.

- [S1] llama.cpp, *Using multiple GPUs with llama.cpp*
  (docs/multi-gpu.md, master) —
  https://raw.githubusercontent.com/ggml-org/llama.cpp/refs/heads/master/docs/multi-gpu.md — primary
- [S2] ComputingForGeeks, *Dual RTX 3090 for Local LLMs: 70B
  Benchmarks and Build* (b11741, 2026-10-19) —
  https://computingforgeeks.com/build-dual-rtx-3090-llm/ — measured
- [S3] ggml-org/llama.cpp PR #19378, *backend-agnostic tensor
  parallelism (experimental)*, merged 2026-04-09 —
  https://github.com/ggml-org/llama.cpp/pull/19378 — primary
- [S4] CanItRun, *Multi-GPU Setups for Local LLMs (2026)* (summarises
  the May 2024 XiongjieDai set + PR #19378) —
  https://canitrun.dev/guides/multi-gpu-setups/ — index
- [S5] CanRunLLM, *Two GPUs for local LLMs: memory adds up, speed
  doesn't* — https://canrunllm.com/guides/multi-gpu — index
- [S6] ai-muninn, *Two Modded 2080 Tis Reach 59.6 tok/s on Qwen3.8-27B
  With llama.cpp Tensor Parallel* —
  https://ai-muninn.com/en/blog/qwen38-dual-2080ti-tensor-parallel —
  index (author-caveated, 1–2 runs/config)
- [S7] DevBrewery, *The Flag We Tuned Around Got Deleted* (dual
  Tesla P40 post-mortem, 2026-09-08) —
  https://dev.to/devbrewery/the-flag-we-tuned-around-got-deleted-31ge — measured
- [S8] AICompass summary of a user report, *Asymmetric pair of Tesla
  V100s (16 GB + 32 GB)* —
  https://bittide.aicompass.dev/article/20e32f55-d88e-4812-8c00-c68494258ddd — measured (secondary republication)
- [S9] SharedLLM, *llama.cpp tensor-split: running one model across
  multiple GPUs* — https://sharedllm.org/blog/llama-cpp-tensor-split.html — index
- [S10] GPUFits, *Multi-GPU Setup for Local LLMs* —
  https://www.gpufits.com/en/guides/multi-gpu-setup-for-llm/ — model/estimate, flagged in text
- [S11] llama.cpp, *tools/server/README.md* (master) —
  https://github.com/ggml-org/llama.cpp/blob/master/tools%2Fserver%2FREADME.md — primary
- [S12] Aliteq, *--n-cpu-moe in llama.cpp (Nov 2026)* —
  https://aliteq.com/n-cpu-moe-llama-cpp-what-it-actually-does — measured compilation
- [S13] ggml-org/llama.cpp PR #29887, *add a GPU cache for MoE
  experts kept in host memory* —
  https://github.com/ggml-org/llama.cpp/pull/29887 — primary
- [S14] DevelopersDigest, *llama.cpp MoE Offload: --n-cpu-moe vs the
  New Expert Cache* (2026-10-09) —
  https://www.developersdigest.tech/blog/llama-cpp-moe-offload-n-cpu-moe-vs-moe-cache-2026 — labelled compilation of PR reports
- [S15] Akciali, *A 30B model on an 8 GB GPU* (RTX 2080, 2026-06-20) —
  https://www.akciali.com/articles/posts/a-30b-model-on-an-8gb-gpu/ — measured
- [S19] AICassindra, *Ollama on the GPU, in depth* (checked against
  Ollama FAQ/source) —
  https://www.aicassindra.com/blogs/gpu/gpu_ollama_deep.html — index
- [S20] philmcneely/t2-egpu-linux, *Dual-Card Benchmark — Raw Data*
  (2× RX 6800) —
  https://github.com/philmcneely/t2-egpu-linux/blob/HEAD/dual-gpu/benchmark-results.md — index
- [S21] ggml-org/llama.cpp Issue #1437, *LLaMA NUMA could be better* —
  https://github.com/ggml-org/llama.cpp/issues/1437 — primary
- [S22] heiketu/PeoplesLLM commit 4a11318, *NUMA bandwidth matrix
  re-test* (dual Xeon 8360Y) —
  https://github.com/heiketu/peoplesllm/commit/4a11318ad0866639da3f285a47a4ed7e7cb32247 — fork benchmark data
- [S24] NVIDIA, *nvidia-smi documentation* (topology codes) —
  https://docs.nvidia.com/deploy/nvidia-smi/index.html — primary
- [S25] Spheron, *NUMA GPU Topology: Why Our 8-GPU Node Scaled Like
  4* —
  https://www.spheron.network/blog/we-debugged-why-our-8-gpu-node-scaled-like-4-a-numa-postmort/ — index
