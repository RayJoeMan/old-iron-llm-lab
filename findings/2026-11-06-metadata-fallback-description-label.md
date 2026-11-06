# Metadata fallback: one restated label line — and restatements don't stack

- **Date:** 2026-11-06 (adopted; certified)
- **Platform:** Mint — see `platforms/mint.md`
- **Source record:** Nov 6 adoption filing #3; experiments E163, E172
  (the non-stacking result: E171)

## Question

The metadata lane's fallback model (llama3.2:3b) drops the `Description:`
label on most lines (the champion doesn't — its labels are 40/40 without
help). Can one restated final line repair the fallback, per the
restatement law?

The adopted line, appended after the existing hook-reminder (which stays):

> "Begin every description line with 'Description:'"

## Measured result

- **E163:** label compliance **5/40 → 39/40** on the first try, hooks
  untouched
- **E172 (certification):** labels **40/40 in all three replicates** vs
  the fresh base's 10/40; zero truncation. (Hook variance across
  replicates was shown to be the fallback's own batch texture — the
  repair was never on the hook axis.)

## The boundary

**Exactly one label restatement.** Adding a second restated line for the
`Title:` label collapsed compliance instead (5/40 in one batch, 0/40 in
the rest — E171): restatements do not stack like-for-like. The fallback
brief carries the one line, and the stacking question is closed.

## Verdict

**ADOPTED (certified ×3):** the fallback metadata brief gains the
Description: line. Champion (phi-4-mini) untouched.
