# Summary coverage line — one sentence that makes summaries keep the numbers

- **Date:** 2026-11-04 (adopted)
- **Platform:** Mint — see `platforms/mint.md`
- **Source record:** TUNING #97(b); experiments E85, E86, E93 (challenger history: E82)

## Question

Small-model summaries silently drop numeric facts — quantities, times,
prices — while reading fluently. Can a single brief line fix coverage
without buying inventions, and which model should own the lane?

## Method

Design ruler (18 scored facts) with and without the line; then a fresh-set
confirmation (30 scored facts, unseen text) pitting the incumbent brief
against a challenger model that had won an earlier round.

The adopted line, verbatim (an application of the restatement law):

> "Your summary must include every number, quantity, and time stated in the source."

## Measured result

- **E85 (design ruler):** coverage **14/18 → 18/18** with the line;
  inventions 0 in both arms; wall +17%.
- **E93 (fresh set):** qwen3:8b + line **27/30** vs phi-4-mini 24/30 —
  the earlier phi-for-summaries candidate (E82) was **downgraded and not
  adopted**; phi is fast-lane only on summaries.
- **E86:** the line is safe on phi too (17/18 vs 18/18 — a within-noise
  one-fact reshuffle), so one unified brief serves either model.

## Verdict

**ADOPTED:** qwen3:8b is the summary model (temp 0.3), and the coverage
line is mandatory in the standard summary brief. The fleet note that
travels with this finding: a fluent summary is not a complete one — this
lane keeps a mandatory independent figure check regardless (see
Methodology), because the model's residual failure mode is omission.
