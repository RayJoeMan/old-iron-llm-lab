# Fortress VL baseline exists — on the RTX only; the M4000 runner dies by CUDA launch timeout

- **Date:** 2026-11-09 (certified at export as a PARTIAL;
  battery audited Nov 9, 2026 — two independent audit
  passes agree, the second establishing the M4000 cause)
- **Platform:** Fortress — see `platforms/fortress-provisional.md`
  (2026-11-08 fingerprint)
- **Source record:** experiment R17-5, R17 run ledger
  (audited results; on-box results `r17_5.json`); repairs
  the void R16-T7 arm (see the R16 void-arms entry)

## Question

With the manifest store repaired (dereferenced manifests;
R16-T7's failure), what does qwen2.5vl:3b measure on each
card — the cross-card VL comparison two batteries have
owed?

## Method

qwen2.5vl:3b via pinned per-card Ollama instances on the
repaired store; per-image eval medians (3 reps each) over
a fixed 4-image set (one synthetic probe PNG + three eval
JPEGs), plus a batch-of-4-images arm on the RTX.
Placement verified per arm via `/api/ps` + GPU snapshot.

## Measured result

**RTX per-image set — COMPLETE; the first Fortress VL
control of record:**

| Image | Eval median (tok/s) |
|---|---|
| probe.png | 96.68 |
| ArtificialAnalysis jpeg | 90.51 |
| TTS_Spaces_Arena jpeg | 85.90 |
| TTS_Arena jpeg | 81.37 |

All content heads correct/sensible. No VL control existed
before (R16-T7 failed outright), so there is no drift
call — these ARE the baseline. (The pre-flight smoke read
64.47 on probe.png as a single cold call; 96.68 here is a
warm median — different measurement contexts, not a
contradiction. Prompt-eval figures in this arm are
cache-contaminated on reps 2–3 and are not quoted as
throughput.)

**Two sub-arms produced no data:**

- ❌ **Batch-of-4 arm (RTX): FAILED — HTTP 400 Bad
  Request**, raised after the per-image sets completed;
  no batch data exists.
- ❌ **M4000 per-image set: FAILED — HTTP 500 Internal
  Server Error** before any image (`per_image: {}`); no
  M4000 VL data exists. The repaired store fixed the RTX
  instance; the M4000-pinned instance still 500s. Cause,
  established by the audit's second pass from the shared
  instance log: at 10:43:40 CT a ggml-cuda error — **"the
  launch timed out and was terminated"** — followed by
  llama-server termination (signal: aborted). The 500's
  cause class is a **CUDA kernel launch timeout in the
  M4000 runner**, not the store or manifests (the log's
  only other error is a non-fatal "couldn't remove unused
  layers: permission denied" on a symlinked blob).

## Verdict

**CERTIFIED AS PARTIAL.** The RTX VL baseline stands as
the control of record. The cross-card VL comparison
remains unproduced for the second battery in a row — now
with a named cause on the Maxwell card: under this
backend, full-configuration VL on the M4000 dies by CUDA
launch timeout. (A reduced configuration later survived
on the M4000 — see the R19 interim entry.)
