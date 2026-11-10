# Fresh-seed replicates: the certified controls hold — the MoE split drifts low, outside the ±2% band

- **Date:** 2026-11-09 (certified at export; battery audited
  Nov 9, 2026 — two independent audit passes agree)
- **Platform:** Fortress — see `platforms/fortress-provisional.md`
  (2026-11-08 fingerprint)
- **Source record:** experiment R17-1, R17 run ledger
  (audited results; on-box results `r17_1.json`)

## Question

Do the certified R10 controls reproduce under fresh seeds —
and how much of any delta is seed noise vs silent drift?

## Method

B3 probe with seeds 7 / 1234 / 2026 (median-of-3 per seed),
one arm per (config, seed): solo 8B on the RTX (control
55.29, F-35) · 14B layer split ts 2,1 (control 12.43,
F-37) · MoE dual split ts 1,1 (control 22.57, F-37).
Deltas read against the fleet's ±2% de-noising band (see
the Mint band finding, TUNING #236).

## Measured result

| Config | Seed eval medians | Median-of-seeds | Δ vs control |
|---|---|---|---|
| Solo 8B RTX | 55.09 / 54.44 / 53.79 | 54.44 | **−1.54% — in band** |
| 14B split ts 2,1 | 12.43 / 12.44 / 12.44 | 12.44 | **+0.08% — dead on** |
| MoE dual split | 21.99 / 22.72 / 18.60 | 21.99 | **−2.57% — OUTSIDE the band, low** |

Prompt medians track the same shape (solo 1260.98 /
1242.17 / 1224.98 vs control 1262.31; 14B ~102–105 vs
102.59; MoE 106.96 / 108.85 / 109.35 vs 104.73, slightly
high). The MoE spread is 18.74%, driven by the seed-2026
arm (reps 18.60 / 22.57 / 18.05). Caveat of record: every
MoE rep stops at 54 eval tokens (early EOS), so those
medians rest on very short generations and are
intrinsically noisier than the 256-token arms.

## Verdict

**CERTIFIED.** Two of three controls replicate inside the
band, the 14B essentially exactly. The MoE −2.57% headline
is real as measured but should not be read with the same
confidence as the other two arms — the short-generation
caveat is part of the finding.
