# A cross-device draft is functional in b12136 and strictly harmful: the draft must live on the target's card

- **Date:** 2026-11-09 (certified)
- **Platform:** Fortress — see `platforms/fortress-provisional.md`
- **Source record:** FORTRESS-TUNING.md **F-51**; experiment
  R115-3 (on-box results `r115_3.json`)

## Question

F-42's winning configuration keeps the 0.6b draft on the same
card as the 8B target, where it shares compute and VRAM with
the model it serves. b12136 can place the draft on the second
GPU instead (`--spec-draft-device`). Does moving the draft off
the target's card — freeing its compute and memory — beat
same-card drafting, or does the cross-device verify traffic
eat the gain?

## Method

llama.cpp b12136, `--spec-type draft-simple`, target
qwen3:8b `-dev CUDA0` (RTX 4000), draft qwen3:0.6b
`--spec-draft-device CUDA1` (Quadro M4000), `-ngld all`,
n-max 16, B3 probe, medians. Controls: the same-card n-max 16
arm from the same run (79.02, F-50) and the no-draft solo
control (55.29, F-35).

**Placement evidence (VRAM-verified):** after load, the
M4000 carries 1,788 MiB vs its 382 MiB desktop baseline — the
draft verifiably resides on the second card; the RTX carries
the target alone at 6,025 MiB, vs 7,369 MiB with the draft
on-card. The draft-device flag targets the second GPU in this
build without complaint.

## Measured result

Prompt 706.24 / eval **30.7**, acceptance 0.773 — **−61% vs
the same-card control (79.02)** and **−44% vs not drafting at
all (55.29)**. Acceptance also sags vs same-card placement
(0.773 vs 0.8194).

Freeing the target card of draft compute and VRAM is worth
nothing against the per-step cross-device verify traffic and
synchronization over this host's SYS PCIe link.

## Verdict

**CERTIFIED.** The placement works and is strictly harmful.
Extending F-43: on Fortress, speculative decoding is a
**same-card** technique — the draft lives on the target's own
GPU (F-42's configuration) or not at all.
