# MoE placement for a 13.8 GB Qwen3-30B-A3B: dual-GPU layer split is fastest AND lightest on RAM

- **Date:** 2026-11-08 (certified)
- **Platform:** Fortress — see `platforms/fortress-provisional.md`
- **Source record:** FORTRESS-TUNING.md **F-38**; experiments R10-3,
  R10-3b (on-box results `r10_3.json`, `r10_3b.json`)

## Question

A 30B mixture-of-experts model (ud-qwen3-30b-a3b-2507, UD Q3_K_XL,
13.83 GB) exceeds either 8 GB card alone. On a host whose supposed
advantage is 128 GB of system RAM, where should it live: split across
both GPUs, on one GPU with experts offloaded to CPU RAM (fully,
`-cmoe`, or partially, `-ncmoe`), with a GPU expert cache
(`--moe-cache-mib`), on the slower card, or CPU-only?

## Method

llama.cpp b12136, B3 probe conventions (ctx 8192, `-t 4` except the
CPU-only arm at `-t 8`), medians; server RSS and per-GPU VRAM recorded
per arm.

**Two scope notes, stated plainly:**

- **Generation span:** the model ends this probe deterministically —
  every arm generated the same **54-token span** (of np 256
  requested). The span is identical on every arm, so all comparisons
  are like-for-like; no arm is credited with a longer or shorter
  decode than another.
- **Quant scope / declared substitution:** the MoE arms ran on the
  on-hand UD Q3_K_XL file — the quant that can be GPU-resident on
  this pair at all (the stock Q4_K_M's ~17.3 GB of weights exceed the
  pair's 16 GB combined VRAM). The same battery's 14B one-card arm
  carries the declared config-5 substitution (no 14B Q3 file on hand;
  UD Q4_K_XL max-fit used instead — see F-37).

## Measured result

| Placement | Prompt tok/s | Eval tok/s | RSS | VRAM (RTX / M4000) |
|---|---|---|---|---|
| **(a) Dual-GPU layer split** (ngl 99) | 104.73 | **22.57** | **784 MiB** | 7,259 / 7,479 MiB |
| (b) RTX + `-cmoe` (all experts on CPU) | 43.2 | 4.65 | 13,377 MiB | 1,871 / — |
| (b2) RTX + `-cmoe` + expert cache 4096 MiB | 60.57 | **17.71** | 13,387 MiB | 5,971 / — |
| (b3) RTX + `-ncmoe 36` | 53.44 | 6.01 | 10,055 MiB | 5,047 / — |
| (c) M4000 + `-cmoe` | 22.83 | 4.98 | 13,400 MiB | — / 2,294 MiB |
| (d) CPU only (ngl 0, `-t 8`) | 29.76 | 3.69 | 14,342 MiB | — |

- **(a)** The dual split is the fastest placement *and* the lightest
  on RAM: both cards' VRAM holds the model and the 128 GB system RAM
  is nearly untouched. A q8_0-KV variant at ctx 4096 costs ~2%
  (prompt 108.73 / eval 22.09) — capacity headroom is nearly free.
- **(b)** Adding the 4 GiB expert cache to the one-card offload arm
  is the single biggest one-card lever measured in the battery:
  4.65 → **17.71 eval (+281%)** (the cache itself is F-39).
- **(c) `-ncmoe` knee sweep (RTX):** 48 → 4.57 · 40 → 5.79 · 34 →
  7.02 · 28 → 9.03 eval (prompt 39.04 / 49.23 / 55.0 / 68.55; RSS
  13,377 → 7,959 MiB). Monotone — the knee lies below 28, and even
  the sweep floor (9.03) is half the cache arm. Manual layer-count
  tuning is dominated by the cache on this host.
- **(d)** With all experts on CPU, decode is CPU-bound and GPU choice
  barely matters (M4000 arm 4.98 vs RTX arm 4.65); the GPU shows only
  in prefill (43.2 vs 22.83). CPU-only is the viable floor (3.69),
  beaten by every GPU-touching placement.

## Verdict

**CERTIFIED placement policy, as measured:**

**dual split (22.57) > RTX + cache (17.71) > RTX partial offload
(≤ 9.03) > CPU-offload arms (~4.7–5.0) > CPU-only (3.69)**

RAM guidance inverts the naive expectation on a big-RAM host: the
split that uses the *least* system RAM is also the fastest;
CPU-offload placements spend 8–14 GB of RAM to go slower. The expert
cache is the one-card lever; the second card is worth more as the
split partner than as anything else for this model.
