# Pool-wide omission rate: 14 of 120 cards (F-99)

- **Date:** 2026-11-12 (certified)
- **Platform:** Fortress — Windows/Vulkan Ollama lane, the
  :11435 (serve-second) instance only; see
  `platforms/fortress-provisional.md` for the machine
- **Source record:** FORTRESS-BACKLOG-2026-11-12.md
  filler F1; on-box RESULTS, run `backlog-a-2026-11-12`

## Question

What is Qwythos's omission rate across the whole brief
pool — not just the known target inputs — under seed
variation?

## Method

Seeds 1–5 × all 24 pool inputs (120 cards) at the
original condition; omissions counted per card on the
on-box readout. Bar: report the pool rate; flag any
non-target input with ≥2/5 omissions.

## Measured result

- **120 cards: 14 omissions (11.7%)**, 0 inexact URLs,
  14 structure flags (the readout's structure count
  tracks its omission count here, as in A1's readout).
- Read together with the per-input pricing (F-81,
  F-82): the pool's omissions are concentrated, not
  uniform — B07 omits at 15/30 across seeds and B01 at
  10/30, while other inputs (B02: 0/30; the 8B anywhere:
  0/30) do not omit at all.

## Verdict

**CERTIFIED.** The pool-wide headline is 11.7%, and it
is the wrong number to plan around: the omission risk
is per-input and per-model, and the per-input rates in
F-81/F-82/F-84 are the operative figures.
