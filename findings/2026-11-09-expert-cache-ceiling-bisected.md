# The expert-cache ceiling on 8 GB cards is bisected to (5120, 6144] MiB — on both cards

- **Date:** 2026-11-09 (certified)
- **Platform:** Fortress — see `platforms/fortress-provisional.md`
  (2026-11-08 fingerprint)
- **Source record:** FORTRESS-TUNING.md **F-61**; experiment R16-T3
  (on-box results `r16_t3.json`)

## Question

F-44 bounded the expert-cache init failure to (4096, 6144]
MiB. Where inside that interval does the ceiling sit — and
does it differ between the Turing and Maxwell cards?

## Method

ud-qwen3-30b-a3b on one card, `-cmoe`, ctx 8192, B3 probe,
cache arms at 5120 MiB on both cards and 6144 MiB on the
M4000 (the RTX 6144 failure is F-44's certified record).

## Measured result

- RTX + 5120 MiB cache **loads**, eval **29.88** (vs 17.71
  at 4096, +69%).
- M4000 + 5120 MiB **loads**, eval **10.18** (vs 7.83 at
  4096, +30%).
- M4000 + 6144 MiB **fails to load**.

## Verdict

**CERTIFIED.** Combined with F-44's RTX 6144 failure, the
interval narrows to **(5120, 6144] MiB on both cards**. The
5120 operating point is worth real decode on the RTX —
cache sizing belongs in the MoE serving recipe.
