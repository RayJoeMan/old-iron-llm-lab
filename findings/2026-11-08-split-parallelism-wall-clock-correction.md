# Split-server parallelism is metric-sensitive — and F-40's np4 "1.60×" is a timings-sum figure: by wall clock the MoE split scales ≈1.0×, the 14B split a real 2.02×

- **Date:** 2026-11-08 (certified)
- **Platform:** Fortress — see `platforms/fortress-provisional.md`
- **Source record:** FORTRESS-TUNING.md **F-45**; experiment
  R11-3 plus a re-read of the R10-6b artifacts (on-box results
  `r11_3.json`, `r10_6.json` arm `np4-moe-dual`)

## Question

F-40 reported the dual-split MoE server at `-np 4` serving 4
concurrent streams at "36.15 tok/s aggregate = 1.60× its
single-stream rate." That aggregate was computed as the **sum of
the per-stream eval rates in the server timings**. Does the
split server actually deliver 1.60× the *throughput* — total
tokens per wall-clock second — and what happens at `-np 8` and
on the 14B split?

## Method

llama.cpp b12136, B3 streams, both aggregates computed for every
config:

- **Timings-sum:** Σ per-stream eval tok/s — the convention
  behind F-40's np4 figure (recomputed from the original R10
  artifacts for the np4 MoE arm: 216 eval tokens over a 9.62 s
  batch wall).
- **Wall:** total eval tokens ÷ batch wall time — the honest
  fleet throughput.

MoE B3 streams generate 54 tokens each; 14B streams the full
256. Configs: MoE dual split at `-np 4` (R10, re-measured) and
`-np 8` (two batches), 14B layer-split ts 2,1 at `-np 4` (two
batches), against the certified single-stream controls (MoE
22.57, 14B split 12.43).

## Measured result

| Config | Timings-sum agg | Wall agg | Single-stream |
|---|---|---|---|
| MoE dual split `-np 4` (R10) | 36.15 | **22.45** | 22.57 |
| MoE dual split `-np 8` (2 batches) | 33.12 / 34.32 | **21.08 / 21.88** | 22.57 |
| 14B split ts 2,1 `-np 4` (2 batches) | 28.24 / 28.24 | **25.09 / 24.85** | 12.43 |

**The MoE split does not scale with slots by wall clock** —
np8 ≈ np4 ≈ single-stream. It is already compute-saturated
single-stream, and parallel slots only subdivide it (per-stream
~4.3 tok/s at np8).

**The 14B split scales for real: np4 ≈ 2.02× by wall clock**
(25.09 vs 12.43). Batching hides the layer-split pipeline
latency that caps its single-stream rate. Parallelism pays
exactly where the single-stream configuration is latency-bound,
and not where it is compute-bound.

## What this corrects in F-40 — stated exactly

F-40's split-server-parallelism bullet reads: *"the dual-split
MoE server at `-np 4` serves 4 concurrent B3 streams at
36.15 tok/s aggregate = 1.60× its single-stream rate —
sub-linear (shared pipeline stages) but real; the split config
is a small-fleet server, not a single-user artifact."*

The 36.15 figure is a **timings-sum**; the wall-clock aggregate
for the same run is 22.45, i.e. **wall-clock scaling ≈1.0×**.
The sentence's scaling claim ("1.60×… but real") does not hold
by wall clock, and the published F-40 file now carries this
correction at the top of its Measured result. **Nothing else in
F-40 is affected:** its dual-model concurrency and replica
findings were measured with separate server instances on
separate cards (and reproduce under a different harness — see
F-48), not by summing streams inside one split server.

## Verdict

**CERTIFIED.** Quote split-server throughput by wall clock.
Spend `-np` headroom on the 14B split (a real 2× serving win),
not on the MoE split (saturated; slots only subdivide it). And
as a methodology rule for this program: any aggregate computed
by summing per-stream rates inside one server must be labeled
timings-sum and paired with its wall-clock figure before it is
cited as scaling.
