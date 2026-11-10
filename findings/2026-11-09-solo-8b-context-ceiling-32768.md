# The solo-8B context ceiling on 8 GB is 32768 tokens — q8_0 KV only

- **Date:** 2026-11-09 (certified)
- **Platform:** Fortress — see `platforms/fortress-provisional.md`
  (2026-11-08 fingerprint)
- **Source record:** FORTRESS-TUNING.md **F-59**; experiment R16-T1
  (on-box results `r16_t1.json`)

## Question

How deep a context can the solo 8B hold on an 8 GB card,
and what does the KV quantization ladder cost or permit?

## Method

qwen3:8b solo on the RTX 4000, llama.cpp b12136, context
ladder at 32768 and 65536 under f16, q8_0, and q4_0 KV.

## Measured result

- ctx 32768 with f16 KV **fails to load** (weights + f16 KV
  exceed the card).
- ctx 32768 with q8_0 KV (K+V) **loads at 7,417 MiB** and
  holds a 29,681-token fill: prompt median 827.9 tok/s,
  **decode median 19.66 tok/s** at that depth.
- ctx 65536 **fails under both q8_0 and q4_0 KV**.

## Verdict

**CERTIFIED.** The 8 GB ceiling for this model is 32768
tokens, and only with quantized KV.
