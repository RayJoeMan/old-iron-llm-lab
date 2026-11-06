# Platform — Mint (settled)

The fleet's laboratory: portable recipes (briefs, contracts, temperatures,
extraction rules) are proven here first, and a second machine's confirmation
run is still required before a recipe is adopted there.

## Fingerprint (as of 2026-11-06)

- **Machine:** ASUS ROG GL752VW laptop
- **CPU:** Intel i7-6700HQ (the fleet's only AVX2 CPU)
- **GPU:** NVIDIA GTX 960M, 2 GB — Maxwell, compute capability 5.0 (sm_50)
- **Driver:** NVIDIA 580.178.04 (the last driver branch supporting Maxwell)
- **OS:** Linux Mint
- **Serving:** Ollama 0.40.13, user-space systemd service
- **Service environment (load-bearing):**
  - `OLLAMA_FLASH_ATTENTION=1` — **required**: the q8_0 KV cache below makes
    llama-family models fail to load without it (found 2026-11-01, when the
    quick lane was silently broken until the fix)
  - `OLLAMA_KV_CACHE_TYPE=q8_0`
  - `OLLAMA_KEEP_ALIVE=30m`
- **Models on box:** qwen3:8b · llama3.2:3b · phi4-mini (phi-4-mini) ·
  gemma3:12b · qwen2.5vl:3b · nomic-embed-text
  - qwen3:4b is **retired** from every job class (measured, repeatedly —
  see the structured-drafting record in the working ledger)

## Measured baselines (GPU offload, driver 580 era)

| Model | Eval rate |
|---|---|
| llama3.2:3b | ~12.8 tok/s |
| qwen3:4b (retired) | ~9.2 tok/s |
| qwen3:8b | ~5.2 tok/s |

CPU-only baselines for the 8B were 1.56–2.72 tok/s before the GPU driver
landed — the driver/offload change, not any sampler setting, was the unlock.

## Run discipline (part of the fingerprint)

- **One heavy job at a time** — the box has one effective runner slot under
  queue load; a second model's request can queue indefinitely behind
  back-to-back generations.
- Load guardrails and an idle-box window for vision work are part of every
  run protocol; contention state is logged with results.
- Non-sensitive, fixed text only for experiments; everything a local model
  produces is a draft until the checker pass.
