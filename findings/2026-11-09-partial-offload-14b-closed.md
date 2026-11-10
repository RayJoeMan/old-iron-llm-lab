# Draftless partial offload of the 14B is closed — the split remains the only sane placement

- **Date:** 2026-11-09 (certified)
- **Platform:** Fortress — see `platforms/fortress-provisional.md`
  (2026-11-08 fingerprint)
- **Source record:** FORTRESS-TUNING.md **F-62**; experiment R16-T4
  (on-box results `r16_t4.json`)

## Question

F-52 showed the 14B partial offload *with* a draft decoding
at 1.33 tok/s. How much of that collapse was the draft —
what does the same placement do draftless?

## Method

ud-qwen3:14b solo on the RTX 4000, `-ngl` sweep, NO draft,
B3 probe.

## Measured result

| Offload | Eval (tok/s) |
|---|---|
| ngl 20 | 2.10 |
| ngl 24 | 2.53 |
| ngl 28 | 3.14 |
| ngl 32 | fails to load |

## Verdict

**CERTIFIED.** The draftless ngl-28 arm (3.14) beats F-52's
with-draft figure (1.33) — the draft itself was a net drag
on this placement. Even draftless, partial offload decodes
at ~¼ of the dual split's 12.43: **partial offload is
closed as a 14B lane; the dual layer split stands.**
