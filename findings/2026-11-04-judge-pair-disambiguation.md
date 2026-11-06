# Judge-pair protocol — two disambiguations in the rubric text

- **Date:** 2026-11-04 (adopted)
- **Platform:** Mint program; the judges are two external guest models
  (DeepSeek + Muse Spark) run as a pair — checker lane, not a worker lane
- **Source record:** TUNING #97(f); experiments E78, E49 (bounds: E116, E125)

## Question

Two guest models used as QA judges disagreed with the gold key and with
each other — mostly, it turned out, over two *ambiguous rubric points*,
not over the content. Does folding disambiguations into the rubric text
(no worked examples) make the pair trustworthy enough to pre-clear work?

The two disambiguations: a multi-beat single play counts as **one**
action; a deliberately planted mistake in a spot-the-mistake item is
**deliberate**, not a defect.

## Measured result (20-entry QA set, vs rubric-only baseline)

| Metric | Rubric only | Disambiguated rubric |
|---|---|---|
| Guest agreement | 15/15 of 20 scored | **18/18 of 20** |
| Combined false positives | 9 | **1** |
| Safely pre-clearable entries | 6 | **10** |
| Two-guest-PASS breaches | — | **0** |
| Union recall | — | **9/9** |

**Bounds (part of the adoption):**

- **Pair use only.** Per-judge recall *slips* under the same text
  (8/9 → 7/9 and 9/9 → 8/9 individually), and a local 8B judge regresses
  outright (13/20; recall 4/9 → 2/9; an earlier audit found only 1 of 6
  local-judge flags fully correct). The disambiguated rubric is never
  used for single-judge or local-judge runs.
- **Validated range is drafting QA.** Confirmed on a fresh constructed
  corpus (E125); explicitly *out* of range for metadata QA (E116: both
  guests pass nearly everything there). Model judging is not a checker
  outside its measured range.

## Verdict

**ADOPTED as the fleet's judge-pair protocol:** two different-lineage
guest judges, the disambiguated rubric verbatim, pair agreement required,
and an independent verification pass before any flag is acted on. Guest
lanes remain triage/judge lanes — never production drafters.
