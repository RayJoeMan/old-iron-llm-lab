# The 14B split's context ceiling is 16384 — and depth is nearly free up to it

- **Date:** 2026-11-08 (certified)
- **Platform:** Fortress — see `platforms/fortress-provisional.md`
- **Source record:** FORTRESS-TUNING.md **F-46**; experiment
  R11-4 (on-box results `r11_4.json`)

## Question

The 14B layer-split (ts 2,1) is the fleet's unlock for models
that fit neither card (F-37). How far does its context window
stretch across the two 8 GB cards, what does a doubled context
cost at depth, and where exactly is the wall?

## Method

llama.cpp b12136, ud-qwen3:14b layer split ts 2,1, `-ngl 99`.
Arms at ctx 32768 (attempted), ctx 16384 (B3 probe + longprobe
4,241-token probe), against the certified ctx-8192 control
(prompt 102.59 / eval 12.43).

**KV measurement method (declared):** build 12136 logs no
KV-buffer-size line at default verbosity — there is no log
figure to cite. KV growth was therefore measured by **per-card
VRAM deltas** (`nvidia-smi` used-memory before/after load)
between the ctx-8192 and ctx-16384 loads, and the 32768
requirement is extrapolated from that slope. The deltas are the
measure; no log-derived KV size is claimed anywhere in this
finding.

## Measured result

**ctx 32768 fails at init** — `failed to allocate buffer for
kv cache`. The VRAM-delta accounting: raising ctx 8192 → 16384
grew the split's footprint from RTX 6,669 / M4000 4,080 MiB to
7,429 / 4,313 MiB — **+760 / +233 MiB, ≈993 MiB per +8192
tokens across the split**. ctx 32768 would need ~1 GiB beyond
the 16384 footprint (7,429 / 4,313 MiB) — not available after
weights. **16384 is the context ceiling for this split.**

**At ctx 16384, B3 is unchanged:** prompt 104.08 / eval 12.5 vs
the ctx-8192 control 102.59 / 12.43. Doubling the allocated
context costs nothing measurable at shallow depth — capacity
headroom is free until it isn't (the 32768 wall).

**Depth cost at 4,241 tokens (longprobe, ctx 16384):** prefill
181.35 tok/s; decode **10.74** — **−14%** vs the shallow rate.
Long-context work on this split is viable at 16k with a modest
depth tax.

## Verdict

**CERTIFIED.** Serve the 14B split at ctx 16384 as the default
ceiling configuration: B3-class work runs at the full shallow
rate, 4k-token-depth decode pays only ~14%, and 32768 is not a
configuration this pair of cards can allocate at all in
build 12136.
