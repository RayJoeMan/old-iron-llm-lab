# Restate-then-label: a ≤8-word reason before the label fixes the champion's misses — the gain is a copy effect, not an explanation

- **Date:** 2026-11-09 (adopted; experiment 2026-11-07,
  fresh-set replication 2026-11-09)
- **Platform:** Mint — see `platforms/mint.md`
- **Source record:** TUNING #221 (E220, held) closed by
  TUNING #237 (FF-1 fresh-set replication); adoption
  ratified in the 2026-11-09 adoption review

## Question

The classification contract (llama3.2:3b, temp 0,
label-only) sat at 55–56/60 on hard title sets. Does
making the model emit a brief reason *before* the label —
`N. <≤8-word reason> :: LABEL` — beat it, and does the
gain survive a fresh set?

## Method

Two hard 60-title sets (fixed, blinded-label scoring, two
replicates per arm per set). Base = champion label-only
contract. Challenger = restate-then-label, same model,
temp 0.

## Measured result

**E220 (first set):** base strict **55/60** both replicates
(misses {6,7,27,28,48}); challenger **58/60** both
replicates (misses {8,12}, both SEASONAL-boundary titles),
all five champion misses fixed, zero parse failures.
Cost: 1,082 vs 429 eval tokens (**2.52×**), wall 118.5 /
112.5 s vs 54.1 / 42.5 s.

**FF-1 (fresh 60-title replication):** base **56/60** both
replicates (byte-identical); challenger **59/60** both
replicates; sole miss {37 COMEDY→GRAPHIC-NOVEL ACTION} in
both; 976 / 953 eval tokens (**2.16×**).

**Mechanism, measured and named honestly:** in E220, 59/60
of the reason fields were the classified item's own title
echoed back, not a paraphrase or rationale. The gain is a
**copy-then-label effect** — restating the input before
committing — not an explanation effect. The contract is
adopted for what it measures, not for the story one might
tell about it. Corroboration: a later routing experiment
(E234) used the adopted contract throughout; all three of
its draws returned the identical 59/60 label vector.

## Verdict

**ADOPTED** as the standing classification contract
(restate-then-label, llama3.2:3b, temp 0) — and the
contract the Fortress lane inherits. The ~2.16× token/wall
cost is accepted: a 60-title batch still runs ~100 s.
