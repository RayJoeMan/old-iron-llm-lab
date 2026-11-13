# The omission is not B07-specific: control input B01 omits 10/30 (F-82)

- **Date:** 2026-11-12 (certified)
- **Platform:** Fortress — Windows/Vulkan Ollama lane, the
  :11435 (serve-second) instance only; see
  `platforms/fortress-provisional.md` for the machine
- **Source record:** FORTRESS-BACKLOG-2026-11-12.md item
  A13; on-box RESULTS, run `backlog-a-2026-11-12`

## Question

Is Qwythos's Source-URL omission specific to the B07
target input, or does it fire on control inputs too?

## Method

Same protocol as A12 (seeds 1–30, temp 0.3) on the two
control inputs (the pool's first two slots excluding
B07/B20). Bar: input-specific iff the target rate is
≥3× the control rate **and** controls total ≤1/60
omissions.

## Measured result

- B01: **10/30 omissions**. B02: **0/30**. Controls
  total **10/60** — the ≤1/60 clause fails outright.
- The rate ratio (15/30 vs 10/60 pooled) is beside the
  point once the control clause fails: a second pool
  input omits at a 33% rate.

## Verdict

**CERTIFIED — bar NOT met.** The omission is not a
B07-only pathology; it is a Qwythos behavior that at
least two dissimilar pool inputs trigger at high rate.
Any fix has to be priced pool-wide, not per-input.
