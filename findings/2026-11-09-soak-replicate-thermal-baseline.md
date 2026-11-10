# Soak replicate: 42.75 vs 43.54 (−1.81%, in band) — and the RTX peaks at exactly 85 °C again

- **Date:** 2026-11-09 (certified at export; battery audited
  Nov 9, 2026 — two independent audit passes agree)
- **Platform:** Fortress — see `platforms/fortress-provisional.md`
  (2026-11-08 fingerprint)
- **Source record:** experiment R17-2, R17 run ledger
  (audited results; on-box results `r17_2.json` + telemetry)

## Question

Does the R15-S4 long-decode soak (F-56) replicate — on
speed and on temperature — as the pre-covers thermal
baseline for the slot-blank cooling experiment?

## Method

F-56's exact shape: qwen3:8b solo on the RTX 4000,
ctx 16384, 4,241-token prompt, 4 consecutive 8,192-token
streaming passes, windowed rates + RTX telemetry every
10 s. Rear slot covers OFF, as in the control run.

## Measured result

- Pass eval tok/s: **44.08 / 43.04 / 42.46 / 42.38** →
  median **42.75 vs the F-56 control median 43.54 =
  −1.81% — inside the ±2% band**.
- Windowed decay replicates: first-window ~48.3 →
  last-window ~40.8 (pass 1), flattening to ~46.0 → ~40.1
  by pass 4 (control shape ~48.5 → ~41). Depth, not heat,
  remains the cost.
- **RTX temp peak 85 °C — an exact match to the control's
  85 °C** (SM clock settles ~1,410–1,480 MHz at 85 °C from
  an initial 1,680 MHz boost; power ~102–124 W).

## Verdict

**CERTIFIED.** The soak replicates on both axes. This is
the covers-OFF baseline the covers-on repeat is compared
against.
