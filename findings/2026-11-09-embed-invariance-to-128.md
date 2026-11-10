# Embedding batch-invariance extends to 128: 17.02 / 17.09 docs/s

- **Date:** 2026-11-09 (certified at export; battery audited
  Nov 9, 2026 — two independent audit passes agree)
- **Platform:** Fortress — see `platforms/fortress-provisional.md`
  (2026-11-08 fingerprint)
- **Source record:** experiment R17-4, R17 run ledger
  (audited results; on-box results `r17_4.json`)

## Question

F-64 showed nomic-embed throughput flat from batch 1 to
32 on the standing Ollama lane. Does the invariance hold
at production-scale batch sizes?

## Method

`/api/embed` on the standing Ollama instance,
nomic-embed-text resident on the M4000 (945 MiB per
`/api/ps`), batch 64 and 128, 1 warmup + 3 reps, medians.

## Measured result

| Batch | Reps (docs/s) | Median |
|---|---|---|
| 64 | 17.02 / 17.02 / 17.34 | **17.02** |
| 128 | 17.32 / 17.07 / 17.09 | **17.09** |

Against the F-64 controls (b1 16.67 / b8 16.67 / b32
17.02): batch 64 exactly matches the b32 control, batch
128 is +0.4% above it.

## Verdict

**CERTIFIED.** Throughput on this lane is batch-invariant
from 1 through 128 — still latency-bound at every tested
size.
