# NUMA placement is a no-op on this dual-socket WSL host — on the GPU split and on the CPU-offload path

- **Date:** 2026-11-08 (certified)
- **Platform:** Fortress — see `platforms/fortress-provisional.md`
- **Source record:** FORTRESS-TUNING.md **F-41**; experiments R10-5,
  R10-5b (on-box results `r10_5.json`, `r10_5b.json`)

## Question

The web literature (see `methodology/multi-gpu-split-background.md`)
says NUMA placement on a dual-socket host can be worth tens of
percent exactly where the CPU touches weights — and Fortress's two
GPUs sit on different sockets' root complexes (`nvidia-smi topo -m`:
GPU↔GPU **SYS**, cross-socket; per-GPU NUMA affinity is not exposed
under WSL). Does any placement — llama.cpp's `--numa` modes or
external `numactl` pinning/interleave — move either the dual-GPU
split or the CPU-offload MoE config on this host?

## Method

llama.cpp b12136, B3 probe, 2 reps per arm. Two configs: the
dual-GPU MoE layer split (VRAM-resident, RSS ~0.7 GB) and the
RTX + `-cmoe` offload config (13.4 GB of experts resident in RAM —
the config where NUMA should matter most). `--numa distribute` arms
ran under a 180 s watchdog (the F-29 wedge watch).

## Measured result

**On the dual-GPU MoE split (R10-5):**

| Arm | Eval tok/s |
|---|---|
| default | 22.59 |
| `--numa distribute` | 22.27 |
| `--numa isolate` | 22.44 |
| numactl pin node0 | 23.04 |
| numactl pin node1 | 22.01 |

**On RTX + `-cmoe`, 13.4 GB of experts in RAM (R10-5b):**

| Arm | Prompt tok/s | Eval tok/s |
|---|---|---|
| default | 41.02 | 4.84 |
| `--numa distribute` | 40.02 | 4.75 |
| `--numa isolate` | 41.90 | 4.80 |
| `--numa numactl` (interleave=all) | 35.62 | 4.60 |
| numactl pin node0 | 40.19 | 4.75 |
| numactl pin node1 | 39.28 | 4.72 |

Both configs sit in a **±2.6% decode band** — no actionable delta.
The only mover anywhere is interleave on the offload config, and it
moves *down* (eval 4.60, prefill −13%). Two grounded reasons: at
~5 tok/s the expert-read traffic is nowhere near either node's
bandwidth — the bind is AVX-only v1 Xeon compute, not memory
placement — and WSL2's hypervisor-managed memory gives guest NUMA
policy little real locality to exploit. The bare-metal cross-socket
penalty (~38% of local bandwidth in the background literature) does
not bind at these rates.

**Scope note on the F-29 wedge:** `--numa distribute` completed
cleanly on both R10 configs (llama-server run directly). The F-29
wedge — `distribute` hanging generation, confirmed three times on
the Ollama-lane surface — is therefore **surface-specific, not a
blanket property of distribute under WSL**. It is flagged here
rather than silently generalised in either direction.

**Accounting footnote:** the `--numa` arms report RSS 6,217 MiB vs
13,377 MiB for default/pins — recorded as observed (a
page-accounting difference under those policies), **not** a memory
saving.

## Verdict

**CERTIFIED.** NUMA placement is a no-op on this host, on both the
GPU-resident split and the CPU-offload path. Leave it at default;
NUMA tuning is closed for this host unless the CPU or the WSL layer
changes materially.
