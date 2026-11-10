# R19 INTERIM — 128 GB runs a 120B: gpt-oss-120b at ~6.7 tok/s from system RAM

> **INTERIM ENTRY — battery still running.** This page
> covers only the arms of battery R19 that had completed
> when it was written (2026-11-10). **No F-numbers are
> assigned**; certification happens at the battery audit,
> after the final arm. The Flash-Next arm (UD-IQ3_XXS fit
> + B3) had not run — its model download was in progress.
> The battery straddles a hardware change: arm r19_0 is a
> pre-swap control on the previous CPUs; every other arm
> below ran on the current fingerprint (see
> `platforms/fortress-provisional.md`).
>
> All figures are traced to the on-box result files
> (`r19_*.json`); medians are llama.cpp B3 medians unless
> a wall figure is named.

- **Date:** 2026-11-10 (interim)
- **Platform:** Fortress — see `platforms/fortress-provisional.md`
- **Source record:** experiment battery R19, on-box results
  `r19_0.json` → `r19_vl.json`

## The question the battery answers

The fleet's 512 GB RAM upgrade case rests on an unproven
premise: that system RAM far beyond a model's size is a
usable serving tier. R19 proves or kills the premise at
128 GB first, with a model no installed GPU can hold:
**gpt-oss-120b, MXFP4 build, 63,387,346,208 bytes on disk
(sha256
582bd40f6886200101f4c4ed9f25f3fe80cc14c86e9e2b37746cd8904a0c622d)**,
staged on the 1 TB NVMe model drive.

## Pre-swap control (r19_0)

qwen3:8b, CPU-only, on the previous CPU pair (labeled
PRE-SWAP v1 CONTROL in the result file): eval median
**2.42 tok/s** (reps 2.42 / 2.43 / 2.39), prompt median
50.0, RSS 6,679 MiB.

## Fit sweep (r19_1) — how the 120B is served at all

Four fit configurations, llama.cpp server, 8 threads:

| Arm | Configuration | Result |
|---|---|---|
| `fit_ngl0` | RAM only (`-ngl 0`) | loads; **eval 6.60**; load 950.9 s; RSS 61,701 MiB |
| `fit_cmoe_rtx_cache6144` | RTX-pinned, `-cmoe`, 6144 MiB expert cache | **server failed to start** — `cudaMalloc failed: out of memory` allocating the 6,139.52 MiB MoE cache buffer on the 8 GB card (the F-61 ceiling, met again) |
| `fit_cmoe_rtx_cache0` | RTX-pinned, `-cmoe`, cache 0 | loads; **eval 6.71** — the sweep's best config; load 1053.1 s; RSS 60,549 MiB |
| `fit_cmoe_dual_cache4096` | dual-device, `-cmoe`, cache 4096 | **TimeoutError** — the health wait expired while the preceding arm's ~59 GB server was still tearing down and holding the port (chain-log diagnosis); no measurement |

Load times run ~950–1050 s per arm through the current
storage path; the result file itself notes load_s is not
comparable across arms (page cache warms).

## B3 at the survivable configurations (r19_2)

- ngl0 baseline: eval reps 6.79 / 6.76 / 6.77 → **median
  6.77 tok/s** (prompt median 6.52; load 1009.1 s).
- The at-best-config arm (`b3_best`, the cache-0 config)
  **failed to start** — the same port/teardown collision
  as the dual fit arm. It is recorded here as lost, not
  smoothed over; whether it is re-run is an audit
  decision.

## Prefill and depth (r19_3, r19_4 — cache-0 config)

| Arm | Prompt tokens | Prompt tok/s (median) | Eval (tok/s) |
|---|---|---|---|
| `pf_4k` | 4,049 | **19.19** (reps 19.43 / 18.94) | 7.0 |
| `pf_17k` | 16,193 (ctx 20480) | **26.86** (reps 26.98 / 26.74) | 7.74 |
| `ctx32k_fill` | **28,337** (ctx 32768) | **28.09** | 7.16 |

A 28,337-token fill at ctx 32768 completes and decodes at
7.16 tok/s. Decode rate is flat (~6.6–7.7) across every
completed configuration — the tier's speed is set by
memory bandwidth, not by placement.

## Quality spot-check (r19_5) — NO VERDICT

All five fixed prompts generated tokens (eval 5.43–6.38
tok/s; 88–635 eval tokens each), but the harness captured
**`content: null` on all five outputs** — the generations
landed in the model's analysis channel and no visible
content was recorded. **No quality claim is made from
this arm.** The capture defect is an audit item for the
battery close-out.

## VL survival on the M4000 (r19_vl)

F-69 left the M4000's VL runner dead by CUDA launch
timeout at full configuration. At a reduced configuration
(pinned instance, `num_ctx` 2048), the verdict of record
in the result file is:

> **"VL SURVIVES on the M4000 at the reduced config."**

- Survival attempt: **HTTP 200**, correct content ("a
  vibrant, gradient background with a red square in the
  center"), placement verified on the M4000.
- Per-image set: the probe image completes — 3/3 reps
  HTTP 200, correct content, **eval median 111.98 tok/s**.
  The three larger JPEGs were rejected in every rep
  (**HTTP 400**: 4,024- and 4,078-token requests exceed
  the 2048-token context), and batch-of-4 likewise
  (13,104 tokens > 2048) — context-size rejections at the
  reduced config, not crashes. No JPEG medians exist from
  this arm.
- Honesty note: the intended ≤256 px probe resize did
  not apply (no PIL on-box); the original 320×240 probe
  image was used.

## What this establishes so far

**Capacity: proven at 128 GB.** A 120B-parameter model
that no installed card can hold loads from system RAM and
serves at ~6.7 tok/s decode with a 28k-token context —
usable for batch and offline work, not interactive chat.
**Speed: bounded by the memory tier, as suspected** —
every placement lands in the same ~6.6–7.7 band. Whether
more RAM buys more than headroom is precisely what the
completed half of this battery cannot yet say; the
Flash-Next arm and the audit close the question.
