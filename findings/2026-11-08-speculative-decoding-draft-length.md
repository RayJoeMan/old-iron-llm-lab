# Speculative decoding on the solo 8B: draft length is the whole game — short drafts lose at 95% acceptance, long drafts win +42%

- **Date:** 2026-11-08 (certified)
- **Platform:** Fortress — see `platforms/fortress-provisional.md`
- **Source record:** FORTRESS-TUNING.md **F-42**; experiment R11-1(a)
  (on-box results `r11_1.json`, arms `8b-rtx-spec06-n{4,8,16}`)

## Question

On the fastest solo configuration in the fleet (qwen3:8b fully
resident on the RTX 4000, F-35), does speculative decoding with a
small same-family draft model pay — and what actually decides the
outcome: draft acceptance rate, or draft length?

## Method

llama.cpp b12136, `--spec-type draft-simple`, draft = qwen3:0.6b
resident on the same RTX 4000 (`-ngld all`), target qwen3:8b
(`-dev CUDA0 -ngl 99 -t 4`), B3 probe, warmup + 3 reps, medians.
`--spec-draft-n-max` swept over {4, 8, 16}. Control (F-35):
prompt 1262.31 / eval 55.29 tok/s. Acceptance = draft tokens
accepted ÷ draft tokens generated (server timings, cross-checked
against the server log's "draft acceptance" lines).

## Measured result

| Draft n-max | Prompt tok/s | Eval tok/s | Δ vs control | Acceptance |
|---|---|---|---|---|
| 4 | 1000.3 | 47.7 | **−13.7%** | 0.9481 |
| 8 | 1001.36 | 62.44 | **+12.9%** | 0.85 |
| 16 | 980.11 | **78.69** | **+42.3%** | 0.8194 |

At n-max 4 the drafting is near-perfect (94.8% acceptance) and
still **loses**: with only ~4 tokens per verify step, the
draft+verify overhead on the shared GPU exceeds the target steps
saved. As drafts lengthen, acceptance *falls* (0.95 → 0.82) but the
per-step overhead amortizes faster — on a fast, bandwidth-bound
target, draft **length**, not acceptance, is the deciding variable
across the swept range.

Attaching the draft at all costs ~20% of prompt processing at
every length (prompt 980–1,001 vs the 1,262 control): on this
lane, speculative decoding is a decode-only trade.

## Verdict

**CERTIFIED.** On the RTX solo 8B, run
`--spec-draft-n-max 16` with the 0.6b draft on-card (+42% decode).
Do not use short draft lengths on this lane — a 95%-accepted
4-token draft is a −14% configuration, not a near-miss. (Whether
any of this transfers to split targets is a separate, negative
result — see F-43.)
