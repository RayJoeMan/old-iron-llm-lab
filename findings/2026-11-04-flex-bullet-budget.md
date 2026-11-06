# Flex bullet budget — a hard 3-bullet cap was arithmetic, not judgment

- **Date:** 2026-11-04 (adopted)
- **Platform:** Mint — see `platforms/mint.md`
- **Source record:** TUNING #97(d); experiment E100 (mechanism: E93/E95)

## Question

Fact-dense sources kept losing facts under the summaries lane's hard
"exactly 3 bullet points" rule. Was the model failing to *select*, or was
the budget simply too small to hold the facts?

## Method

One fact-dense source (12 scored facts) under both budgets, on both
candidate models. Mechanism work first established that the drops were
budget arithmetic under the cap, not salience judgment.

## Measured result

| Model | Hard 3 bullets | "3 or 4 bullet points" |
|---|---|---|
| qwen3:8b | 9/12 | **12/12** (exactly 4 bullets used) |
| phi-4-mini | 7/12 | **12/12** |

## Verdict

**ADOPTED:** the summary brief uses a **flex bullet budget** — fact-dense
sources (~10+ numeric facts) brief "3 or 4 bullet points"; lean sources
keep exactly 3. The generalizable point: when a format cap and a coverage
demand conflict, measure which one is binding before blaming the model's
judgment. (This finding is also why the long-input work concluded that
single-pass summarization of figure-dense text fails *structurally* —
past ~20 figures, chunking is the only measured route; see the merge-loop
finding.)
