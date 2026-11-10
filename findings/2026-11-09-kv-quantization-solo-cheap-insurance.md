# KV quantization at ctx 16384 is cheap insurance solo — the kvq8 failure was a split effect

- **Date:** 2026-11-09 (certified)
- **Platform:** Fortress — see `platforms/fortress-provisional.md`
  (2026-11-08 fingerprint)
- **Source record:** FORTRESS-TUNING.md **F-60**; experiment R16-T2
  (on-box results `r16_t2.json`)

## Question

An earlier split-era run failed at context init under
quantized KV. Is the quantization itself defective, or was
the failure a property of the split placement?

## Method

qwen3:8b solo on the RTX 4000, ctx 16384, B3 probe, three
KV arms: f16, K-only q8_0, K+V q8_0.

## Measured result

| KV arm | Eval (tok/s) | Δ vs f16 | VRAM |
|---|---|---|---|
| f16 | 53.38 | — | 7,185 MiB |
| K-only q8_0 | 51.97 | −2.6% | −532 MiB |
| K+V q8_0 | 50.82 | −4.8% | −1,072 MiB |

All three arms load and run clean.

## Verdict

**CERTIFIED.** The split-era kvq8 context-init failure does
**not** reproduce in solo placement — it was a
split-footprint effect, not a quant defect. KV quant is the
sanctioned lever when a solo placement needs the headroom
(see F-59).
