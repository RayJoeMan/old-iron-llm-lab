# Long decode costs KV depth, not thermals — 43.54 tok/s over 4× 8,192 tokens

- **Date:** 2026-11-09 (certified)
- **Platform:** Fortress — see `platforms/fortress-provisional.md`
  (2026-11-08 fingerprint)
- **Source record:** FORTRESS-TUNING.md **F-56**; experiment R15-S4
  (on-box results `r15_s4.json`, telemetry recomputed from all
  79 samples)

## Question

What does a genuinely long generation cost on the solo 8B —
does the rate decay with KV depth, with heat, or both?

## Method

qwen3:8b solo on the RTX 4000, ctx 16384, 4,241-token prompt,
4 consecutive 8,192-token generations, per-pass and windowed
rates with full card telemetry.

## Measured result

- Per-pass eval: 44.32 / 43.65 / 43.43 / 43.08 — median
  **43.54 tok/s**, a gentle ~2.8% decline across passes, no
  cliff. Within each pass the windowed rate decays
  ~48.5 → ~41 tok/s (≈ −15%) as the KV cache grows.
- Telemetry: temp mean 83.2 °C, **peak 85 °C** (the card rode
  at the harness's abort line without tripping it; all 4
  passes completed), power mean 112.4 W / max 125.2 W,
  util mean 86.3%, SM clock mean 1479 MHz.

Long-generation decode (43.54) sits ~21% under the short-B3
rate (55.29). Thermal context: this soak ran with the rear
slot covers off; the covers-off replicate is F-66.

## Verdict

**CERTIFIED.** Depth, not thermal collapse, is the cost of
long generations on this lane — the rate follows the KV
cache, not the thermometer.
