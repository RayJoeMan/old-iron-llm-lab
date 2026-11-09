# Heterogeneous replicas as specified: the qwen3:4b + qwen3:8b pair runs at 98–99% of its sequential sum

- **Date:** 2026-11-09 (certified)
- **Platform:** Fortress — see `platforms/fortress-provisional.md`
- **Source record:** FORTRESS-TUNING.md **F-49**; experiment
  R115-1 (on-box results `r115_1.json`)

## Question

F-48's cross-check of F-40's lossless-concurrency claim had to
run with a substituted pair (llama3.2:3b + qwen3:8b), because
qwen3:4b was absent from the on-box store and its pull would
have breached that run's download cap; the *specified*
heterogeneous pair — qwen3:4b on the M4000 + qwen3:8b on the
RTX — was left explicitly NOT RUN. Measured as originally
written, does the specified pair also run losslessly?

## Method

llama.cpp b12136, B3 probe, one CUDA_VISIBLE_DEVICES-masked
llama-server instance per card (the replica arrangement of
F-48). qwen3:4b was pulled for this run (2,497,280,480 B — the
run's only download) and a real generation verified before
lane work. Fresh solo comparator: qwen3:4b on the M4000
(`-dev CUDA1`), warmup + 3 reps. The sequential sum pairs that
fresh solo figure with the certified F-35 control for the 8B
leg (55.29). Concurrent: two rounds, both instances generating
simultaneously.

## Measured result

Solo qwen3:4b on the M4000: prompt 119.26 / eval **17.4**
(reps 17.4 / 17.4 / 17.3), VRAM 4,062 MiB. Sequential sum:
17.4 + 55.29 = **72.69**.

Concurrent aggregates: **71.42 / 71.95 — 98.3% / 99.0% of the
sequential sum.** The 4B leg runs at (fractionally above) its
solo rate (17.65 / 17.59); the 8B leg gives back ~2–3%
(53.77 / 54.36 vs the 55.29 control).

**Comparator note (declared):** F-48's substituted pair read
≈101% against a sequential sum measured fresh in the same run;
this run's 8B comparator is the certified F-35 control, as
tasked. The 1–2% difference between the two ratios is
comparator choice plus run noise, not a pairing effect anyone
should act on.

## Verdict

**CERTIFIED.** The specified heterogeneous pair reproduces
F-40/F-48's lossless-concurrency result: two cards run two
different models concurrently at 98–99% of the sum of their
solo rates. This closes the last open item from the R11
battery — every arm of F-48's specification has now been
measured as written.
