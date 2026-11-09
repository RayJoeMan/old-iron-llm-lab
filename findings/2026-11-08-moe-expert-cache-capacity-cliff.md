# The MoE expert cache is a capacity cliff: 1 GiB hurts, 2 GiB helps a little, 4 GiB pays 3.8×

- **Date:** 2026-11-08 (certified)
- **Platform:** Fortress — see `platforms/fortress-provisional.md`
- **Source record:** FORTRESS-TUNING.md **F-39**; experiments R10-3c,
  R10-3 arm b2 (on-box results `r10_3c.json`, `r10_3.json`)

## Question

llama.cpp's GPU expert cache (`--moe-cache-mib`, an LRU VRAM cache
for host-resident MoE experts) is documented in the web literature as
paying only at high cache hit rates (≳75%), with a prefill penalty
around 0.73×. On this host — one RTX 4000 holding attention while all
experts of a 13.83 GB MoE sit in RAM (`-cmoe`) — how does decode
actually move with cache size, and does the cache combine with
partial offload (`-ncmoe`)?

## Method

llama.cpp b12136, ud-qwen3-30b-a3b-2507, RTX-only, `-cmoe`, ctx 8192,
B3 probe; longprobe (4,241-token) arms carry the prefill side. Cache
sizes 1024 / 2048 MiB (R10-3c) against the no-cache arm and the
4096 MiB arm (R10-3 b2) on the identical config.

**Hit rate is NOT instrumented, and no hit-rate figure is claimed:**
build 12136 at default verbosity emits no expert-cache hit-rate lines
(the server log contains no `moe_cache` / hit lines under any grep
pattern tried; the result JSONs' `log_hits` arrays are empty). The
capacity curve below is inferred from decode deltas alone. This is
the capacity mechanism *under* the published "pays only at ≳75%
hits" rule — the two accounts agree on shape, but the hit rate
itself was not measured here.

**Interruption + audit note (R10-3c):** the first 3c pass was
interrupted mid-arm by an SSH disconnect and resumed; worse, the
execution channel's completion notice for the dead pass reported
exit 0 with numbers that did **not** match the on-box artifacts. On
discovery, *every* R10 results file was re-audited against the run
ledger (per-arm median dump): `r10_0b/0c/1/2/3/3b` matched exactly;
only the 3c channel notice was corrupt. All figures in this finding
were re-verified against the on-box result JSONs (the resume pass
re-measured the 1024 arms; first-pass reads 45.55 / 2.82 and
109.32 / 2.75 agree within run variance). From that point in the
battery, figures were taken from on-box JSON artifacts, never from
channel output.

## Measured result

**Decode eval by cache size — a cliff, not a slope:**

| `--moe-cache-mib` | Eval tok/s | vs no cache |
|---|---|---|
| none | 4.65 | — |
| 1024 MiB | 2.70 | **−42%** |
| 2048 MiB | 6.30 | +35% |
| 4096 MiB | 17.71 | **+281%** |

A too-small cache thrashes against the 13.8 GB expert pool and costs
more than no cache at all; the return is superlinear once the cache
can hold the prompt's working set.

**No prefill tax on this rig:** B3 prompt tok/s across the same sizes
runs 43.2 (none) → 42.62 → 48.24 → 60.57 — the cache serves the
prompt pass too, and the published ~0.73× prefill penalty did **not**
reproduce. Longprobe prefill: 106.53 (1024) / 116.5 (2048) tok/s,
with longprobe decode tracking the B3 arms (2.76 / 6.22). (No
no-cache longprobe baseline exists on this config — a noted gap.)

**Cache × partial offload is not a legal combination in build
12136:** `-ncmoe 28` + `--moe-cache-mib {1024, 2048}` fails context
initialisation — `failed to allocate buffer for MoE cache` — on all
four arms tried.

## Verdict

**CERTIFIED.** Size the expert cache to the working set or don't
enable it: at 1 GiB it is a −42% liability, at 4 GiB it is the
biggest one-card lever in the battery (F-38). And on this build,
one-card MoE placement is an exclusive choice — full offload + cache
(17.71) **or** partial offload without cache (≤ 9.03), never both.
