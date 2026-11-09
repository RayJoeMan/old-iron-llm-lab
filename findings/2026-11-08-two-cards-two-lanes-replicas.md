# Two cards are two lanes: concurrency and replicas run at ~101% of the sequential sum

- **Date:** 2026-11-08 (certified)
- **Platform:** Fortress — see `platforms/fortress-provisional.md`
- **Source record:** FORTRESS-TUNING.md **F-40**; experiments R10-4,
  R10-6, R10-6b (on-box results `r10_4.json`, `r10_6.json`,
  `r10_6b.json`)

## Question

If splitting a model that fits one card is a loss (F-37), what *is*
the second card for? Measured directly: run two models at once (one
per card), run the *same* model as two independent replicas, and run
parallel streams on the dual-split server — and compare each
aggregate against the sum of the solo rates.

## Method

llama.cpp b12136, B3 probe conventions. Concurrency arms run two
`llama-server` instances, one pinned per card (`-dev CUDA0/CUDA1`,
separate ports), with identical B3 workloads fired simultaneously,
2 rounds. The sequential-sum comparator is the solo medians from
R10-1 (F-35). The split-server arm runs the dual-split MoE config
(F-38 arm a) with `-np 4` and 4 concurrent B3 streams.

## Measured result

> **CORRECTION (2026-11-08, certified as F-45):** the
> split-server parallelism figure below — the dual-split MoE
> server at `-np 4` serving "36.15 tok/s aggregate = 1.60× its
> single-stream rate" — is a **timings-sum** figure (the sum of
> the per-stream eval rates in the server timings). R11
> re-measured the same configuration by **wall clock**: total
> eval tokens ÷ batch wall = 22.45 tok/s against the 22.57
> single-stream rate, i.e. **wall-clock scaling ≈1.0×** — the
> MoE split is already compute-saturated single-stream, and
> parallel slots only subdivide it. The original measured text
> below is unchanged; read the "1.60×" as timings-sum only.
> The dual-model concurrency and replica findings in this file
> were measured with separate instances on separate cards and
> are **unaffected** (and reproduce under a different harness —
> see the F-48 cross-check). Full treatment:
> [Split-server parallelism is metric-sensitive](2026-11-08-split-parallelism-wall-clock-correction.md).

**Dual-model concurrency (R10-4)** — llama3.2:3b on the M4000 +
qwen3:8b on the RTX, simultaneous:

| Round | 3B (M4000) | 8B (RTX) | Aggregate |
|---|---|---|---|
| 1 | 22.21 | 55.90 | **78.11** |
| 2 | 22.22 | 55.77 | **77.99** |

Sequential sum of solos: 77.38. **No measurable contention** — each
card delivers its full solo rate while the other works.

**Replicas (R10-6, research config 12)** — the same qwen3:8b on both
cards concurrently: aggregate **67.49 / 67.38** tok/s (RTX 55.9 +
M4000 11.5, both at full solo rate) vs the 66.69 sequential sum —
~101% efficiency, lossless. Replicas beat the best single card by
**+22%**; layer-splitting that same model across both cards scored
14.27 (F-37) — **replicas are 4.7× the split** for any model that
fits one card.

**Split-server parallelism (R10-6b):** the dual-split MoE server at
`-np 4` serves 4 concurrent B3 streams at **36.15 tok/s aggregate =
1.60× its single-stream rate** (22.57) — sub-linear, because both
cards' pipeline stages are shared across slots, but real: the split
config is a small-fleet server, not a single-user artifact.

## Verdict

**CERTIFIED operating picture:** RTX 4000 = primary lane; M4000 =
independent second lane (small models, replicas, overflow).
Concurrency and replicas cost nothing against the sequential sum.
Splitting is reserved for models that fit neither card alone (the
14B class, the 30B MoE) — it is the only losing arrangement for
anything else.
