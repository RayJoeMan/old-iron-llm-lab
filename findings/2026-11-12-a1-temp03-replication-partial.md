# Temp-0.3 replication: PARTIAL — both target inputs omit, as one draw counted twice (F-70)

- **Date:** 2026-11-12 (certified)
- **Platform:** Fortress — Windows/Vulkan Ollama lane, the
  :11435 (serve-second) instance only; see
  `platforms/fortress-provisional.md` for the machine
- **Source record:** FORTRESS-BACKLOG-2026-11-12.md item A1;
  on-box RESULTS, run `backlog-a-2026-11-12` (3,911 records)

## Question

Does Qwythos's brief-pool omission behavior at its original
condition (temp 0.3, seed 42, num_predict 900) replicate —
and is the B07/B20 pair one draw counted twice?

## Method

Full 24-input brief pool ×2 in-session reps at the original
condition; omissions scored per card, rep hashes compared.

## Measured result

- Omissions: exactly **B07 and B20, in both reps** (4
  omissions across 48 cards; the other 22 inputs clean in
  both reps) — the bar's omission pattern itself.
- **B07 hash = B20 hash**: the pair is one draw counted
  twice, confirmed.
- Seeded determinism at temp 0.3 confirmed for B07 (rep
  hashes equal).
- The chain's scored read is nevertheless **PARTIAL —
  "omission pattern differs"**: the replication matches on
  which inputs omit, and the record files the pattern as
  differing from the original observation in kind. The
  qualifier is the record's own and is published as
  recorded.

## Verdict

**CERTIFIED as PARTIAL.** The omission pair replicates and
is a single draw; the battery's remaining Qwythos items
(A12–A15) price the omission itself.
