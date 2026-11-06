# VL sport-context line — one opening line cures cross-sport confusion

- **Date:** 2026-11-06 (adopted as a brief amendment)
- **Platform:** Mint — vision lane (qwen2.5vl:3b), supervised first-pass only
- **Source record:** Nov 6 adoption filing #4; experiment E144
  (transfer confirmation: E168)

## Question

A supervised vision lane drafts alt text for cover images (≤30 words,
describe-only). Its signature error was **cross-sport confusion** —
objects from the wrong sport substituted into descriptions. Does one
context line at the top of the brief move it?

The adopted line, opening the existing brief (nothing else changed):

> "These are lacrosse book covers."

## Measured result (fixed 20-cover set, human-verified ground truth)

- **Sport confusion: 3 → 0** — the first brief change on this lane to
  move the confusion axis at all
- Clean count **tied at 11/20** on a five-for-five exchange (five new
  minor slips against five cures)
- Length compliance **18/20** — best of the series
- The lane's standing signature error was absent for the first time
- **Transfer check:** the same line on the larger 7B sibling also cured
  confusion (2 → 0, E168) — the cure is a **brief property, not a model
  property** (the 7B still did not replace the 3B; its clean count
  missed the bar, and VL model work is closed until the hardware changes)

## Why a tie was adoptable here

This lane is **supervised by definition**: every output is verified
against its image before any use, so it is never run unattended. Inside
that frame the trade is asymmetric — confusion is the one error class
the lane calls never-acceptable, while generic slips are exactly what
supervision exists to catch.

## Verdict

**ADOPTED** as a brief amendment inside the supervised lane. The
supervision rule is unchanged.
