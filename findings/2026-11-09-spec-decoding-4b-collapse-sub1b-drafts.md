# Speculative decoding collapses on the 4B target — and same-card drafting on 8 GB is a sub-1B game

- **Date:** 2026-11-09 (certified)
- **Platform:** Fortress — see `platforms/fortress-provisional.md`
  (2026-11-08 fingerprint)
- **Source record:** FORTRESS-TUNING.md **F-58**; experiments
  R15-S6 (on-box results `r15_s6.json`) and R16-T6
  (`r16_t6.json`, load-level observation)

## Question

The 0.6b draft is a certified +42% win on the 8B target
(F-42/F-50). Does the same pairing transfer to the smaller
4B target — and how large a draft can share an 8 GB card
with the 8B at ctx 8192?

## Method

qwen3:4b solo on the RTX 4000, draft-simple with the
qwen3:0.6b draft on-card at n-max 8 and 16, B3 medians;
companion load test attempting 3B and 4B drafts beside the
8B target at ctx 8192.

## Measured result

- 4B draftless baseline: **prompt 2010.83 / eval 85.71**
  tok/s.
- With the 0.6b draft: n8 → eval **21.64**, acceptance
  **0.2036** (471/2313); n16 → eval **17.30**, acceptance
  **0.1012** (465/4596) — net decode **~75–80% below** the
  draftless baseline, against acceptance 0.8194 for the
  same draft on the 8B target (F-50).
- Companion limit (certified as a limit, not a rate): at
  ctx 8192 the 8B target leaves insufficient room on the
  8 GB card for a 3B or 4B draft beside it — all three
  larger-draft arms failed to load (`cudaMalloc failed:
  out of memory` on a 1,918.35 MiB allocation).

## Verdict

**CERTIFIED.** The 4B lane runs draftless; draft/target
pairing is empirical, not assumable. Same-card speculative
drafting on this card at this context is limited to sub-1B
drafts. The draft-variety question itself (can a larger
draft beat the 0.6b on the 8B?) remains OPEN — answerable
at reduced target context or cross-device (F-51's penalty
notwithstanding).
