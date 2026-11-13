# Independent checker certification: phi4-mini delivers the ruler, not a check — BAR NOT MET, slot closed

- **Date:** 2026-11-12 (closed — bar not met)
- **Platform:** Mint — see `platforms/mint.md`
- **Source record:** TUNING #277 (experiment E263);
  design pre-registered in the run's DESIGN.md before
  any call

## Question

Can phi4-mini — a different model family — take the
summary merge loop's checker slot, breaking the adopted
qwen3:8b self-check exception (adoption #1) without its
standing false-positive habit?

## Method

One variable: the checker model. phi4-mini ran the E151
checker brief verbatim (prompt md5s verified) over
(a) the two banked qwen3:8b finals in the 6-call mirror
protocol and (b) two planted-error finals built from
them before any call, every planted figure swap logged
in advance; a qwen3:8b self-check control ran in-session
on the same planted prompts at the same settings (temp
0.3, num_predict 4096). Bar: catch rate within 5 points
of the self-check record with false-flags no worse is
proposed; a catch-rate miss closes the slot.

## Measured result

- On all 20 delivered attempts, phi4-mini returned a
  single comma-separated line listing 22–24 of the 25
  ruler values — an echo of the brief's ruler, not a
  diff against the summary. Under the delivery parse
  the merge loop consumes, catch is **0/18** on the
  banked finals and **0/24** on the planted finals —
  a 100-point miss against the self-check record.
- The failure is not format-only: a lenient comma-split
  diagnostic "catches" everything only because a
  near-complete echo contains the missing set by
  construction, at **122 false-flag listings** across
  the 6 original calls (vs the record's 12) and 67
  across the planted calls (vs the in-session control's
  7) — the false-flag clause fails by an order of
  magnitude under any parse.
- Side finding, filed with the result: the 8b checker's
  own planted-*new*-value catch was **2/12** (its
  banked missing-three were caught 12/12) — the E185
  "biased-but-calibrated" record is fixture-specific,
  and planted-value recall is the honest instrument for
  any future checker work.
- phi's decode rate (9.24–9.49 tok/s) was never the
  problem; the slot fails on task performance.

## Verdict

**BAR NOT MET — SLOT CLOSED.** phi4-mini is not
proposed as the checker and stays metadata-only. The
qwen3:8b self-check exception stands as priced, now
with its fixture-specificity named on the record; the
mandatory independent figure check remains the
backstop, as the bar provided either way.
