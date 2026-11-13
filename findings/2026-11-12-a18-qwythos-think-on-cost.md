# Think-on costs Qwythos the classification set: plain 13/60, trap 0/60 (F-87)

- **Date:** 2026-11-12 (certified)
- **Platform:** Fortress — Windows/Vulkan Ollama lane, the
  :11435 (serve-second) instance only; see
  `platforms/fortress-provisional.md` for the machine
- **Source record:** FORTRESS-BACKLOG-2026-11-12.md item
  A18; on-box RESULTS, run `backlog-a-2026-11-12`

## Question

What does think-on cost Qwythos on the classification
instruments?

## Method

First-15 gate (≥14/15 parse required to proceed to the
full arms), then plain-60 and Trap-60 under think-on.
Bar: no think cost iff plain 60/60 and trap ≥57; cost
if plain ≤58 or trap ≤55.

## Measured result

- The gate **passed 15/15** — think-on parses fine at
  small bulk.
- Full arms: **plain strict 13/60** (13 parsed),
  **trap strict 0/60** (0 parsed, 68 non-format
  outputs). The chain's read is recorded verbatim:
  **"think cost"**.
- Against think-off's standing plain 60 / trap 57
  (F-86), think-on does not tax this model — it breaks
  the format the classifier depends on, at bulk.

## Verdict

**CERTIFIED.** For Qwythos classification, think-on is
not a quality lever; at 60-title bulk it is a format
collapse. The gate passing at 15 is exactly why the
gate is not the measurement.
