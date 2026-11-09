# The speculative-decoding draft-length curve plateaus at 16: longer drafts buy nothing on the solo 8B

- **Date:** 2026-11-09 (certified)
- **Platform:** Fortress — see `platforms/fortress-provisional.md`
- **Source record:** FORTRESS-TUNING.md **F-50**; experiment
  R115-2 (on-box results `r115_2.json`)

## Question

F-42 mapped the speculative-decoding curve on the solo 8B
rising through n-max 16 (47.7 → 62.44 → 78.69) and set the
operating rule at 16 — but the sweep stopped there. Is 16 the
peak, or does a longer draft keep paying?

## Method

Configuration identical to F-42: llama.cpp b12136,
`--spec-type draft-simple`, qwen3:0.6b draft resident on the
same RTX 4000 (`-ngld all`), target qwen3:8b, B3 probe,
medians. `--spec-draft-n-max` at 16 (re-run as this run's
control), 24, and 32.

## Measured result

| Draft n-max | Prompt tok/s | Eval tok/s | Δ vs n16 | Acceptance |
|---|---|---|---|---|
| 16 (control re-run) | 982.43 | **79.02** | — | 0.8194 |
| 24 | 993.77 | 78.56 | −0.6% | 0.6928 |
| 32 | 992.86 | 80.11 | +1.4% | 0.6541 |

The n-max 16 control **reproduces F-42 essentially exactly**:
79.02 vs the certified 78.69, with acceptance identical to
four decimal places (0.8194) under the same seed and prompts —
a cross-run validation of the harness as well as the figure.

Past 16 the curve is **flat**: both deltas (±1.4%) are within
rep noise. Acceptance keeps falling as drafts lengthen
(0.82 → 0.69 → 0.65), but the falling acceptance and the
amortized per-step overhead cancel out. Prefill is unchanged
(~983–994 tok/s — the ~20% draft tax F-42 measured) at every
length.

## Verdict

**CERTIFIED.** F-42's operating rule — run
`--spec-draft-n-max 16` with the 0.6b draft on-card — stands,
now bounded on both sides: 16 is the peak *region* of the
draft-length curve on this lane, and there is no further gain
to buy with longer drafts.
