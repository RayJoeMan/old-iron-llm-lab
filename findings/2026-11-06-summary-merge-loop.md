# Summary merge loop — check-and-repair fixes the chunked merge stage

- **Date:** 2026-11-06 (adopted; certified 2026-11-06)
- **Platform:** Mint — see `platforms/mint.md`
- **Source record:** Nov 6 adoption filing #1; experiments E151 (bar met),
  E167 (fresh-seed certification), E174 (cost audit); stage-1 from E136;
  rejected alternatives E138, E150; checker pricing E185; scope limit E177

## Question

Long sources are summarized by chunking (~500-word chunks), then merging
the chunk summaries. The chunk stage was provably lossless (union coverage
25/25), but the **merge stage compressed by echoing** — 32 bullets against
12 briefed, near-verbatim carry, facts lost. Can a check-and-repair loop
fix the merge without a bigger model?

Failed attempts first (all rejected with measurements): select-then-write
alone cured compression but dropped a whole fact cluster (22/25); a
verbatim-carry ban line was inert (the model doesn't experience its echo
as copying); per-chunk quota selection turned merging into a lottery
(22/25 vs 25/25 across replicates).

## Method

The loop: **select-then-write merge → a ruler-checker call** (diff the
final against the 25-value ruler) **→ one append-only targeted repair**
from the chunk summaries, only if the missing list is non-empty.
Adoption required a fresh-seed replication under a harder design (a seed
passes only if *both* its finals pass).

## Measured result

- **E151:** post-repair **25/25 coverage in both replicates**, 17/16 final
  bullets (bar ≤18), **zero inventions, zero verbatim carry**
- **E167 (certification):** all four checker calls returned the identical
  missing list; all four post-repair finals **25/25 at 16–17 bullets**
- **E174 (cost):** the loop reaches 25/25 at **0.48–0.64× the plain
  merge's wall**, with the best retained-fact rate measured — it is not a
  quality-at-a-price trade

## The exception, priced in the open

⚠️ The loop's checker is **the same model that wrote the finals**
(qwen3:8b checking qwen3:8b), against this fleet's rule that the checker
is never the worker. The adoption was made knowingly, after an audit
(E185) priced the instrument: on its own model's finals it is
**biased-but-calibrated** — a known false-positive pair appears in 6/6
calls while recall holds at 3/3 — and its recall is **provenance-dependent**
(3/3 on 8b finals → 1/5 on another model's finals). Consequences carried
with the adoption:

- The loop is **barred on gemma finals** (E177: post-repair 20/25 + 21/25
  vs a ≥24/25 reopening bar — rejected, do not reopen)
- If the upstream generator ever changes, the checker must be
  **re-certified before the loop is trusted**
- Attempts to brief the bias away are **closed** (E184: the fix destroyed
  cross-seed stability instead)
- An independent editorial figure check remains **mandatory** on every
  summary — that is the backstop

## Verdict

**ADOPTED** as the merge stage of the chunked long-source summary
pipeline. The earlier standing caveat ("merge finals remain
editorial-rebuild items") is lifted **for this pipeline only**. Caveat:
repair bullets are coverage-grade, not editorial-grade — the editorial
pass remains where that is fixed — and the inventions-0 record is
6 finals, not a guarantee.
