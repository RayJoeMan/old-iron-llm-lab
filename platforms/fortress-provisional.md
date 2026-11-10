# Platform — Fortress — SETTLED (post-hardware-change fingerprint, 2026-11-10)

> **This page supersedes the dual-GPU fingerprint of 2026-11-08
> (kept below as the historical state).** On 2026-11-09 the CPU pair
> was swapped (E5-2609 v1 → E5-2660 v2), a second Quadro RTX 4000
> was installed, the Quadro K2000 was removed, and two NVMe drives
> on PCIe carriers went live. **The R10–R17 findings cite the
> 2026-11-08 fingerprint** — their numbers were measured under it.
> Battery R19 straddles the change (its r19_0 arm is a pre-swap
> control; all other arms ran on the current fingerprint). A
> post-swap re-baseline of the dual-GPU numbers is queued; until it
> runs, treat the R10–R17 GPU figures as measured under the v1 CPU
> pair.
>
> Per this repo's versioning rule, any change to CPU, driver,
> serving-stack version, or service environment is a fingerprint
> change and is recorded here with its date.

## Fingerprint (settled, 2026-11-10)

- **Machine:** HP Z820 workstation ("Fortress")
- **CPUs:** 2× Xeon E5-2660 v2 @ 2.20 GHz — 20 cores / 40 threads
  total, **AVX only (no AVX2)**, dual-socket NUMA
- **RAM:** 128 GB DDR3 ECC at **1333 MT/s** (the v2 memory
  controller unlock; 1066 MT/s under the v1 pair); WSL sees
  108 GB (+28 GB swap)
- **GPUs:** **2× Quadro RTX 4000 8 GB (Turing, sm_75) + Quadro
  M4000 8 GB (Maxwell, sm_52)**; driver **582.78**
  - nvidia-smi device order (verified 2026-11-10): **0 = RTX
    4000, 1 = M4000, 2 = RTX 4000**. In the two-card era the
    llama.cpp device order matched: CUDA0 = RTX 4000,
    CUDA1 = M4000.
  - The Quadro K2000 was **removed from the machine**
    (2026-11-09); it is not part of the lane.
- **Storage:** Windows boots from a 2.5″ SATA SSD (the Z820
  cannot boot NVMe); a SATA bulk HDD; two NVMe drives on
  single-drive PCIe carrier cards — a 512 GB drive (Fanxiang
  S501Q) and a **1 TB model drive (Predator GM7)**. The
  oversized-model store (R19) lives on the 1 TB NVMe.
- **Host / lane:** Windows 11 host; WSL2 Ubuntu 26.04.1
  (kernel 6.18.54.1-microsoft-standard). Ollama 0.40.14 as a
  systemd system service (localhost:11434 in-WSL). Experiment
  lane: llama-server on separate ports, service config
  untouched.
- **Serving stack:** llama.cpp **0.9.0-dev b12136** (commit
  2c192444c), **CUDA 12.1 build**. The GPU lane runs on the
  CUDA v12 backend generation — the bundled CUDA v13 server
  skips Maxwell entirely (its compiled architectures start at
  Turing), a correction established on the record during the
  pre-build rounds (service logs + a live runner's
  environment), superseding an earlier Vulkan attribution.
- **Models of record for the R10 battery** (Ollama-store GGUF
  blobs): qwen3:8b (stock Q4_K_M) · ud-qwen3:14b (UD Q4_K_XL) ·
  ud-qwen3-30b-a3b-2507 (UD Q3_K_XL, 13.83 GB) · llama3.2:3b

## Probe of record (B3)

169-token prompt · np 256 · ctx 8192 · temp 0.3 · seed 42 · `-t 4` ·
cache_prompt off · 1 warmup + 3 reps, medians · prompt-eval and eval
tok/s always reported separately (prompt figures on repeated
identical prompts are prefix-cache-affected — see F-24/F-36).
Prefill isolation uses the longprobe prompt (4,241 tokens, np 48).

## Historical fingerprint (2026-11-08 — cited by R10–R17)

- **CPUs:** 2× Xeon E5-2609 v1 @ 2.40 GHz — 8 cores / 8 threads,
  AVX only (no AVX2), dual-socket NUMA (node0: CPUs 0–3, node1:
  CPUs 4–7; distance 10 local / 20 remote), `numa_balancing` 0
- **RAM:** 128 GB DDR3 ECC at 1066 MT/s; WSL 108 GB (+28 GB swap)
- **GPUs:** Quadro M4000 8 GB (sm_52) + Dell OEM Quadro RTX 4000
  8 GB (sm_75); driver 582.78. GPU↔GPU topology
  (`nvidia-smi topo -m`): **SYS** — the cards hang off different
  sockets' PCIe root complexes; cross-card traffic crosses the
  inter-socket link. No NVLink. llama.cpp device order:
  CUDA0 = RTX 4000, CUDA1 = M4000. A third card (Quadro K2000)
  was installed but dark (driver error) and not part of the lane.
- Everything else (host, WSL, serving stack, probe) as above.

## Standing platform notes (from the certified record)

- **Expert cache exists in this build** (`--moe-cache-mib`,
  verified in `--help`) but emits no hit-rate logging at default
  verbosity — no hit-rate figure is claimed anywhere in the
  findings.
- **`-dev` + `-lm none` hangs at load** on this stack; the same
  flag under a device mask loads fine (F-36 side finding).
- **`--numa distribute` wedges generation on the Ollama-lane
  surface** (F-29, confirmed three times there) but completed
  cleanly under llama-server direct in R10 — the wedge is
  surface-specific (F-41). NUMA placement itself is a measured
  no-op on this host (F-41).
- **Vision on GPU:** the pre-build record (F-30) had the vision
  path faulting under flash attention, production vision on the
  Mint. Superseded in part: F-69 establishes an RTX VL baseline
  and names the M4000's full-config failure as a ggml-cuda
  **launch timeout**; the R19 interim entry records VL
  **surviving on the M4000 at a reduced configuration**
  (num_ctx 2048, small images).
- **Row split is not attempted:** removed from CUDA builds
  upstream (see `methodology/multi-gpu-split-background.md`);
  layer and tensor are the split modes that exist on this build.
