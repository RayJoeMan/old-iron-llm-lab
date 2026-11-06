# DRAFT — NOT SENT

> Contribution draft C1. Prepared 2026-11-06 from the fleet record.
> **Not posted anywhere.** Posting under RayJoeMan requires the owner's
> per-item OK. Before any posting: re-check the upstream tracker for an
> existing equivalent report.

## Target

llama.cpp (`ggml-org/llama.cpp`) — bug report: the server's internal
`--numa distribute` mode wedges generation on a dual-socket WSL2 host.

## Summary of the measured behavior

- **Platform:** dual-socket Xeon (2 NUMA nodes exposed to WSL2), GPU
  Quadro M4000 (sm_52), llama.cpp server lane, CPU-MoE configuration.
  *(Full fingerprint to be attached from the platform record at send time,
  marked pre-build.)*
- **Failure:** with `--numa distribute`, the server accepts the task and
  produces **zero tokens in 14 minutes** (GPU 0%); the arm was killed.
  The server log was captured; by design the arm has no result row.
- **Controls (same box, same run):** external placement works —
  `numactl`-wrapped interleave, bind-to-node-0, bind-to-node-1, and a
  taskset socket-bind arm all generate normally. `numactl --hardware`
  shows 2 real nodes, so topology is visible to the process; only
  llama.cpp's own distribute mode is unusable in this environment.

## Why this is worth upstream's time

Upstream NUMA data is bare-metal Linux. A WSL2 dual-socket wedge with a
working external-placement control arm is a configuration upstream cannot
easily reproduce without this hardware — and the failure is silent
(accepted task, no error, no tokens), so affected users have nothing to
search for.

## Attachments at send time

- Captured server log for the wedged arm
- Topology output (`numactl --hardware`)
- The working control arms' results from the same run

## Status

**DRAFT — NOT SENT.** Evidence state: records complete in the fleet's
pre-build tuning record (r6 chain family, NUMA arms + Addenda). The draft
may be finalized either from the pre-build record or held for the
post-build replay's identical NUMA arms — that choice is part of the
owner's per-item review.
