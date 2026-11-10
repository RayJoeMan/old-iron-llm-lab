# Chunk-fuse: 17–18/20 facts survive a 47k-char source where single-pass gets 4/20

- **Date:** 2026-11-09 (adopted)
- **Platform:** Mint — see `platforms/mint.md`
- **Source record:** TUNING #234 (E232); baseline
  comparator TUNING #233 (E231, banked measurement on the
  identical fixture)

## Question

A ~47,000-char source exceeds the context a small model
can attend to in one pass. Does chunk-then-fuse —
summarize per chunk under a coverage brief, then fuse the
chunk summaries — preserve the planted facts where a
single pass cannot?

## Method

Fixture: 47,004 chars / 8,155 words, 20 planted facts, no
other digit tokens (inventions exactly scorable).
Chunk stage: natural line-boundary chunks ≤550 words
(16 chunks, no overlap), per-chunk brief = exactly 3
bullets + a coverage line ("list every number stated in
this chunk with what it counts"), stated and restated
verbatim. Fuse stage: baseline brief shape (≤10 bullets +
coverage line) over the chunk summaries. qwen3:8b,
temp 0.3, seeds 42 + 123.

## Measured result

- **Stage 1:** all 32 chunk calls emitted exactly 3
  bullets, zero inventions; per-chunk coverage perfect
  except chunk 13 in **both** seeds — the planted fact
  "goalies rotate through **7** shot stations" is a
  deterministic chunk-stage loss under the 3-bullet
  budget. Stage-1 union **19/20 in both seeds**.
- **Fuse:** coverage **17/20** (seed 42) and **18/20**
  (seed 123), **zero inventions in both**. The "6
  volunteer coaches" fact dropped in both seeds at the
  fuse stage.
- **Baseline (single pass, E231 on the identical
  fixture): 4/20** — the prompt truncated to 2,050
  tokens. (This experiment's own baseline re-run timed
  out at 1,800 s unscored; that is recorded here rather
  than hidden — the comparator is E231's banked
  measurement.)
- Wall: 972.4 s of scored generation — 17 scored calls
  in less wall than the single truncated baseline call
  (1,284.4 s).

Scope limit, stated in the adoption: the fused finals ran
23 / 26 bullets against the ≤10 brief — **plain fuse is
not adopted as a production final.** Production finals
continue through the check-and-repair merge (E151/E167 —
see the merge-loop finding).

## Verdict

**ADOPTED** as the long-source coverage contract: chunk
at ~550 words, summarize per chunk under the coverage
line, fuse — with finals still finished by the
check-and-repair merge.
