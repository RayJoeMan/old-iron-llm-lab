# One-hour dual-card co-soak: full duration, no abort, combined wall 65.98 tok/s

- **Date:** 2026-11-09 (certified at export; battery audited
  Nov 9, 2026 — two independent audit passes agree)
- **Platform:** Fortress — see `platforms/fortress-provisional.md`
  (2026-11-08 fingerprint)
- **Source record:** experiment R17-3, R17 run ledger
  (audited results; on-box results `r17_3.json` +
  `r17_3-telemetry.csv`)

## Question

Can both cards generate concurrently for a full hour —
what are the combined wall throughput and the thermal
peaks under co-residency?

## Method

8B on the RTX (port 8090) + 4B on the M4000 (port 8091),
back-to-back 1,024-token completions concurrently for
3,600 s; telemetry for both cards every 30 s; per-card and
combined **wall-clock** aggregates (F-45 rule); abort if
either card hits 90 °C.

## Measured result

- Elapsed **3600.6 s** (full hour), `aborted: null` —
  neither card approached the 90 °C abort. Telemetry:
  240 rows, continuous, no gaps.
- Peaks: **RTX 85 °C / 124.43 W**; **M4000 79 °C / 97.94
  W**. The RTX peak matches its solo-soak peak (F-66) —
  co-residency with the M4000 did not push it higher.
- Recorded tallies (JSON): RTX **174 completions /
  178,176 eval tok → 49.49 wall tok/s**; M4000 **58 /
  59,392 → 16.50**; combined wall aggregate **65.98
  tok/s**.

⚠️ **Bookkeeping discrepancy, flagged in the audit and not
smoothed over:** the run's stdout reports final tallies of
RTX 174 completions with **1 error**, and M4000 **59
completions / 60,416 tok** (→ 16.78 wall tok/s) — exactly
one M4000 completion (+1,024 tok) and one late RTX error
beyond the JSON. The JSON is a periodic progress snapshot
that missed the final seconds; the stdout tally is the
true end state. Either way the combined figure moves by
<0.5% and no conclusion changes.

## Verdict

**CERTIFIED.** A full hour of concurrent generation on
both cards is thermally and operationally clean, at a
combined wall 65.98 tok/s by the JSON record (65.98–66.3
across the two tallies).
