# Metadata routing — phi-4-mini + a hook-reminder final line

- **Date:** 2026-11-04 (adopted)
- **Platform:** Mint — see `platforms/mint.md`
- **Source record:** TUNING #97(c); experiments E89, E90

## Question

Title+description pairs came back well-formed but with titles that weren't
hooks (the house rule: every title is a question or an imperative hook).
Is that a model problem or a brief problem?

## Method

The E81 protocol (8 fixed batch prompts × 5 pairs = 40 pairs), scored on
pairs delivered, Title:/Description: label compliance, hook-form rate, and
word limits. Challenger: phi-4-mini with a hook-reminder restated as the
brief's final line (the restatement law applied to format).

## Measured result

- **E89:** hook-form **0/40 → 32/40**; pairs, both label axes, and word
  limits all held at **40/40**; wall unchanged.
- **E90 (fresh-set confirmation):** phi + reminder — pairs 20/20, labels
  20/20 + 20/20, hook-form 18/20; the incumbent 3B arm on the same fresh
  set scored labels 0/20 + 0/20 and hook-form 11/20.

## Verdict

**ADOPTED:** metadata routing moves to **phi-4-mini** (temp 0.3) with the
hook-reminder final line mandatory in every metadata brief;
llama3.2:3b becomes the fallback. Two standing cautions ride with this
lane in the working record: briefs on this lane carry **no exemplars**
(measured harmful in later experiments — examples leak into output and
cost ~11 hook-form points), and the fallback's own label weakness is a
separate defect with its own fix (see the 2026-11-06 Description:-line
finding).
