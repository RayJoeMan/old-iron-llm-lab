# A mostly-one-card 14B can host a draft (ngl 28) — and decodes at 1.33 tok/s, the worst 14B configuration measured on this host

- **Date:** 2026-11-09 (certified)
- **Platform:** Fortress — see `platforms/fortress-provisional.md`
- **Source record:** FORTRESS-TUNING.md **F-52**; experiment
  R115-4 (on-box results `r115_4.json`, including the
  load-probe record)

## Question

F-43 showed the dual-GPU layer split cannot host a draft at
all — a split target leaves no VRAM for an on-card draft
context. Can a *mostly-one-card* 14B do it instead: the model
on the RTX with partial CPU offload, and the draft placed
across the link on the M4000?

## Method

llama.cpp b12136, ud-qwen3:14b on the RTX 4000 with partial
`-ngl`, qwen3:0.6b draft on the M4000
(`--spec-draft-device CUDA1`, `-ngld all`), ctx 8192, B3
probe, medians. The offload was found by a load ladder: each
probe verified with a real B3 completion, not just a
successful load.

**Load ladder:** `-ngl 32` **fails to load**; `-ngl 28`
**loads** — 28 of 40 layers on the GPU is the maximal offload
that fits with the draft attached (after load: RTX 6,929 MiB,
M4000 1,788 MiB, RSS 4,065 MiB).

## Measured result

| Draft n-max | Prompt tok/s | Eval tok/s | Acceptance |
|---|---|---|---|
| 8 | 95.86 | **1.33** | 0.3345 |
| 16 | 121.33 | **0.79** | 0.173 |

That is **9.4× (n-max 8) and 15.7× (n-max 16) slower** than
the dual split's plain, draftless 12.43 (F-35). Prefill stays
split-class (95.86 / 121.33) because it is GPU-parallel; only
decode dies.

Three stacked causes, each already measured separately in
this program: 12 of 40 layers decode on the AVX-only CPU at
`-t 4`; the 0.6b tracks the 14B target poorly, and worse with
draft length (acceptance 0.33 → 0.17 — the F-43 pattern); and
the draft itself sits across the PCIe link (F-51's poisoned
path).

## Methodology note — channel integrity

Mid-run, an interim completion notice reported this arm as
finished with figures (eval 9.41 at n-max 8, 8.97 at n-max
16) that matched nothing on the box: at that moment the
n-max 8 server had been up ~90 seconds and its own timing
log read ≈1.35 tok/s. The notice was discarded, the arm was
re-audited against the on-box harness outputs, server logs
and results JSONs, and the figures above are the
JSON-verified medians (1.33 / 0.79). Only figures traced to
on-box artifacts are ledgered in this program; the incident
is recorded here as part of that honesty rule (the same rule
applied to the R10-3c interruption in the R10 battery).

## Verdict

**CERTIFIED.** The open question is answered: a
mostly-one-card 14B *can* host a draft (ngl 28 is the load
ceiling with one attached) — and the result is the worst 14B
configuration measured on this host. Partial offload +
speculative decoding does not rescue the 14B; for 14B work
here, the dual layer split remains the only sane placement,
draftless.
