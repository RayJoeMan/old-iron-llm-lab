# Filler-fact scanner — adopted as a triage checklist, never a drop gate

- **Date:** 2026-11-05 (adopted)
- **Platform:** Mint program (summary QA)
- **Source record:** TUNING #139; experiments E135, E126

## Question

Summaries accumulate *filler facts* — plausible filler that isn't in the
source. A two-stage scanner (stage-1 flag + verifier stage) looked
promising. Is it accurate enough to *drop* flagged content automatically,
or only to *flag* it for review?

## Method

Rescored against a **definition-built gold set** — the ground truth is a
definition of "filler," applied by hand, not another model's opinion.
Metrics: definition-precision, definition-recall, and dropped-instance
recall, each against its pre-registered bar.

## Measured result

- Verifier-confirmed set = **exactly** the gold filler set:
  definition-precision **11/11 (1.00)** vs bar ≥0.7; definition-recall
  **11/11**
- The verifier stage converts stage-1 precision **0.50 → 1.00 at zero
  recall cost**; dropped-instance recall unchanged at 8/9
- Separately, a *drop-based* use of scanner output measured precision
  **5/11** (E126) on its own metric — the reason the gate use fails

## Verdict

**ADOPTED as a standing triage checklist for summary QA** — scanner output
is a review checklist, full stop. **Mechanical dropping on scanner output
alone is explicitly NOT adopted.** The distinction is the finding: the
same instrument is exact as a flagger and unsafe as a gate.
