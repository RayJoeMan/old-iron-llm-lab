# Platform — Fortress — ⚠️ PROVISIONAL / PRE-BUILD

> **Do not cite numbers from this page as findings.** Fortress's hardware is
> not settled: a CPU swap (v1 → v2 Xeons, parts acquired, not installed) and
> multiple GPU installs are scheduled, and the pre-build tuning chain (r6,
> 150 jobs) was **still running** when this scaffold was staged
> (2026-11-06). This page records platform *facts* so future findings have
> their context ready; the fleet's rule is that Fortress gets full findings
> treatment only when its hardware is settled and its experiment record has
> been synthesized.

## Fingerprint (pre-build state, 2026-11-06)

- **Machine:** HP Z820 workstation ("Fortress")
- **CPUs (current):** 2× Xeon E5-2609 v1 — AVX-only, no AVX2, dual-socket NUMA.
  *(Acquired, awaiting install: E5-2660 v2 pair — memory speed also rises
  when they land, which is why pre-build numbers will not carry over.)*
- **RAM:** 128 GB DDR3 ECC (running at 1066 MT/s under the v1 CPUs)
- **GPU (current):** Quadro M4000, 8 GB — Maxwell, sm_52, driver 582.78.
  A second card (Quadro K2000) is installed but dark (driver error) and is
  slated for removal at build time.
  *(Inbound at staging: two Turing workstation cards and one Pascal card,
  each to be tested on arrival under a hard gate — the first card is fully
  tested before any fleet conclusions are drawn.)*
- **Host / lane:** Windows 11 host; the work lane is WSL2 (Ubuntu), with
  Ollama 0.40.14 as a system service. WSL memory cap raised to 110 GB
  (the lane sees ~108 GB).
- **Backend fact (corrected on the record):** the GPU lane runs on Ollama's
  bundled **CUDA v12** backend — *not* Vulkan, as an earlier fleet record
  stated. The bundled CUDA v13 server skips Maxwell entirely (its compiled
  architectures start at Turing); CUDA v12 carries sm_52. The correction is
  evidenced from service logs and a live runner's environment, and it also
  makes Pascal (sm_61) CUDA-v12-eligible in stock Ollama.

## Pre-build baseline reads (context only — will be superseded)

- GPU-era classification-benchmark eval rates: llama3.2:3b **21.40 tok/s** ·
  qwen3:8b **11.01 tok/s** · qwen3:14b **3.52 tok/s** (the 14B is split-bound:
  ~63% of layers GPU-resident in 8 GB VRAM)
- Memory bandwidth calibration (STREAM triad): **9.75 / 19.76 / 34.17 /
  37.22 GB/s at 1 / 2 / 4 / 8 threads** — saturating past 4 threads, against a
  ~68.3 GB/s dual-socket DDR3-1066 theoretical ceiling
- A 30B-class mixture-of-experts model (Qwen3-30B-A3B) runs resident on this
  box via a llama.cpp CPU-MoE lane — adopted in a narrow role
  (classification + long-context), not as a general drafter

## Known platform hazards (measured, pre-build)

- The serving stack's internal `--numa distribute` mode **wedges generation**
  on this dual-socket box (zero tokens; external NUMA placement works fine).
  This is the subject of a drafted upstream bug report — see
  `contributions/`.
- ubatch 4096 aborts mid-ingest on the M4000; ub ≤ 2048 is the safe region.
- q8_0 KV cache fails to start at context 16384 on sm_52 (loads at 8192;
  f16 loads at 16384).
- The vision model's GPU runner faults (HTTP 500s) on this backend; the
  same model works CPU-only. Production vision stays on the Mint.

*All of the above moves to `findings/` — or is superseded — only after the
post-build replay re-measures the identical experiment set on settled
hardware and the completion synthesis is filed.*
