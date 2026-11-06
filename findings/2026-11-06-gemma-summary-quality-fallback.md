# Gemma as summary quality-fallback — the program's first perfect score, in its regime only

- **Date:** 2026-11-06 (adopted as fallback of record)
- **Platform:** Mint — see `platforms/mint.md`
- **Source record:** Nov 6 adoption filing #5; experiment E148
  (regime bounds: E157, E162, E169, E175)

## Question

Can the 12B (gemma3:12b), running the summaries lane's *adopted* brief
verbatim, beat the champion's fresh-set record — well enough to bank as
the quality fallback for when quality matters more than wall time?

## Measured result

- **Coverage 30/30 with zero inventions** — the first perfect score on
  this set in the program's history — including a multi-part cluster
  both earlier models dropped whole (sub-scores 12/12, 11/11, 7/7)
- Bar met on both clauses (≥27/30 coverage; inventions 0)
- Wall: 136.0 s = **1.99×** the champion's 68.5 s, against a ≤2× routing
  clause — recorded as borderline by the runner itself. Banking a
  *fallback* (invoked when quality matters, not by default) is exactly
  what that evidence supports

## The regime map (why this is not "gemma is the better summarizer")

The same model's other summary regimes are measured and closed:

- **Dense single-pass: collapses exactly like the champion** (E157:
  40% vs 48% at the 40-figure load; 32–35% vs 37% at 60) — no
  dense-source fallback is banked; chunking is the only route
- **Chunked pipeline: loses at stage 1** (E162/E169, closure final from
  both sides) — and the merge loop is barred on its finals
- **The coverage line is load-bearing at 12B too** (E175: removing it
  costs eleven facts, 30/30 → 19/30) — for summaries the line is a
  selection instruction, not scaffolding

## Verdict

**ADOPTED: gemma3:12b is the summary QUALITY-FALLBACK OF RECORD** —
short sources only, adopted brief verbatim, temp 0.3. **Production
routing stays qwen3:8b.** Pipeline roles are per-regime, not per-model.
