# Platform — Fortress — SETTLED (dual-GPU fingerprint, 2026-11-08)

> **This page supersedes the provisional / pre-build page of the same
> filename (dated 2026-11-06).** The second GPU (Quadro RTX 4000) is
> installed and verified, and the R10 mixed-GPU battery (2026-11-08)
> was run and certified against this fingerprint — the Fortress
> findings in `findings/` (2026-11-08 batch) cite this page. The
> pre-build baseline reads on the old page do not carry over.
>
> Per this repo's versioning rule, any change to CPU, driver,
> serving-stack version, or service environment is a fingerprint
> change: a CPU swap (E5-2660 v2 pair, parts on hand) remains
> scheduled, and when it lands the fingerprint changes and the
> affected numbers must be re-measured.

## Fingerprint (settled, 2026-11-08)

- **Machine:** HP Z820 workstation ("Fortress")
- **CPUs:** 2× Xeon E5-2609 v1 @ 2.40 GHz — 8 cores / 8 threads,
  **AVX only (no AVX2)**, dual-socket NUMA (node0: CPUs 0–3,
  node1: CPUs 4–7; distance 10 local / 20 remote), `numa_balancing` 0
- **RAM:** 128 GB DDR3 ECC (1066 MT/s under the v1 CPUs); WSL sees
  108 GB (+28 GB swap)
- **GPUs:** Quadro M4000 8 GB (Maxwell, sm_52) + Dell OEM Quadro
  RTX 4000 8 GB (Turing, sm_75); driver **582.78**
  - GPU↔GPU topology (`nvidia-smi topo -m`): **SYS** — the cards hang
    off different sockets' PCIe root complexes; cross-card traffic
    crosses the inter-socket link. No NVLink.
  - **llama.cpp device order is reversed vs nvidia-smi:** CUDA0 =
    RTX 4000, CUDA1 = M4000 (confirmed by `--list-devices` and by
    VRAM records; `CUDA_VISIBLE_DEVICES` follows the same order).
    Bus IDs: M4000 = 05:00.0, RTX 4000 = 06:00.0.
  - A third card (Quadro K2000) is installed but dark (driver error)
    and is not part of the lane.
- **Host / lane:** Windows 11 host; WSL2 Ubuntu 26.04.1
  (kernel 6.18.54.1-microsoft-standard). Ollama 0.40.14 as a systemd
  system service (localhost:11434 in-WSL). Experiment lane:
  llama-server on separate ports, service config untouched.
- **Serving stack:** llama.cpp **0.9.0-dev b12136** (commit
  2c192444c), **CUDA 12.1 build**. The GPU lane runs on the CUDA v12
  backend generation — the bundled CUDA v13 server skips Maxwell
  entirely (its compiled architectures start at Turing), a correction
  established on the record during the pre-build rounds (service logs
  + a live runner's environment), superseding an earlier Vulkan
  attribution.
- **Models of record for the R10 battery** (Ollama-store GGUF blobs):
  qwen3:8b (stock Q4_K_M) · ud-qwen3:14b (UD Q4_K_XL) ·
  ud-qwen3-30b-a3b-2507 (UD Q3_K_XL, 13.83 GB) · llama3.2:3b

## Probe of record (B3)

169-token prompt · np 256 · ctx 8192 · temp 0.3 · seed 42 · `-t 4` ·
cache_prompt off · 1 warmup + 3 reps, medians · prompt-eval and eval
tok/s always reported separately (prompt figures on repeated
identical prompts are prefix-cache-affected — see F-24/F-36).
Prefill isolation uses the longprobe prompt (4,241 tokens, np 48).

## Standing platform notes (from the certified record)

- **Expert cache exists in this build** (`--moe-cache-mib`, verified
  in `--help`) but emits no hit-rate logging at default verbosity —
  no hit-rate figure is claimed anywhere in the R10 findings.
- **`-dev` + `-lm none` hangs at load** on this stack; the same flag
  under a device mask loads fine (F-36 side finding).
- **`--numa distribute` wedges generation on the Ollama-lane
  surface** (F-29, confirmed three times there) but completed
  cleanly under llama-server direct in R10 — the wedge is
  surface-specific (F-41). NUMA placement itself is a measured no-op
  on this host (F-41).
- **Vision on GPU:** the vision path faults under flash attention on
  this backend (runner OOM at image time); an FA-off profile runs it
  (F-30, pre-build record). Production vision stays on the Mint.
- **Row split is not attempted:** removed from CUDA builds upstream
  (see `methodology/multi-gpu-split-background.md`); layer and tensor
  are the split modes that exist on this build.
