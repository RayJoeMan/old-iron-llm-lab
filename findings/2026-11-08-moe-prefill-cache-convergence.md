# MoE prefill: the dual split wins long-prompt ingestion too — but the expert cache closes most of the gap as prompts grow

- **Date:** 2026-11-08 (certified)
- **Platform:** Fortress — see `platforms/fortress-provisional.md`
- **Source record:** FORTRESS-TUNING.md **F-47**; experiment
  R11-5 (on-box results `r11_5.json`), with the R10-3c
  longprobe series from F-39

## Question

F-38 settled decode placement for the 30B MoE (dual split first,
one-card cache arm second) at B3's 169-token prompt. Ingestion
is a different regime: for a 4,241-token prompt, does the split
still win prefill — or does the expert cache's prompt-pass
benefit (F-39 found no prefill tax, and rising prompt rates
with cache size) change the ordering at long prompts?

## Method

llama.cpp b12136, ud-qwen3-30b-a3b-2507, longprobe (4,241
tokens, np 48): (a) dual-GPU layer split; (b) RTX + `-cmoe` +
`--moe-cache-mib 4096`. Compared against the same pair at B3
(169 tokens) and against the one-card longprobe cache series
from R10-3c.

## Measured result

| Config | Prefill tok/s | Decode tok/s | RSS |
|---|---|---|---|
| Dual-GPU split | **154.58** | **20.02** | 723 MiB |
| RTX + `-cmoe` + cache 4096 | 136.52 | 14.15 | 13,387 MiB |

The split wins ingestion by **+13%** (and decode at depth by
+41%) at ~1/18th the host RAM. But the prefill gap narrows
sharply with prompt length: at B3 the same pair reads 104.73 vs
60.57 (**+73%** for the split); at 4,241 tokens it is +13%. The
cache's prefill benefit grows with prompt length — the one-card
longprobe prefill series is monotone in cache size across all
three measured points: 1024 MiB → 106.53 · 2048 MiB → 116.5
(R10-3c) · 4096 MiB → 136.52.

## Verdict

**CERTIFIED.** F-38's placement ordering holds for ingestion
as well as decode — the dual split is first choice when both
cards are free, on every axis measured (prefill, decode, host
RAM). The refinement: for big-context ingestion confined to one
card, the 4096 MiB cache arm is much closer to the split than
B3 numbers suggest (+73% gap at 169 tokens → +13% at 4,241), so
one-card long-prompt work should always run the largest legal
cache (F-44).
