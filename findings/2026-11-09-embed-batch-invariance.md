# nomic-embed throughput on the standing Ollama lane is batch-invariant

- **Date:** 2026-11-09 (certified)
- **Platform:** Fortress — see `platforms/fortress-provisional.md`
  (2026-11-08 fingerprint)
- **Source record:** FORTRESS-TUNING.md **F-64**; experiment R16-T8
  (on-box results `r16_t8.json`)

## Question

Does batching embedding calls buy throughput on the
standing Ollama lane, or is the lane latency-bound?

## Method

`/api/embed` on the standing Ollama instance,
nomic-embed-text resident on the M4000 (962 MiB), batch
sizes 1 / 8 / 32.

## Measured result

| Batch | Throughput |
|---|---|
| 1 | 16.67 docs/s |
| 8 | 16.67 docs/s |
| 32 | 17.02 docs/s |

Flat across the tested range: on this lane, batching buys
nothing and single-doc calls cost nothing. (Scope note:
this is the Ollama-lane serving figure; the F-21 batch
result — 36.86 docs/s at 5,000 texts — was measured on the
llama.cpp-era lane configuration and stands as its own
record.) Extended to batch 128 by F-68.

## Verdict

**CERTIFIED.** Embedding callers on this lane should batch
for their own convenience only; there is no throughput
reason to.
