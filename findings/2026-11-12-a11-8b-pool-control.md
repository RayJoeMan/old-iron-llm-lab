# 8B pool control on :11435: 24/24 clean — the instance is not the confound (F-80)

- **Date:** 2026-11-12 (certified)
- **Platform:** Fortress — Windows/Vulkan Ollama lane, the
  :11435 (serve-second) instance only; see
  `platforms/fortress-provisional.md` for the machine
- **Source record:** FORTRESS-BACKLOG-2026-11-12.md item
  A11; on-box RESULTS, run `backlog-a-2026-11-12`

## Question

Is the :11435 instance itself clean for brief work — if
qwen3:8b also failed the brief pool here, A1's Qwythos
read would be confounded by the instance.

## Method

qwen3:8b, full 24-input brief pool ×1 at the original
condition (temp 0.3, seed 42, num_predict 900). Bar:
clean iff 24/24, matching its bench result.

## Measured result

- **24/24 clean, 0 omissions, 0 structure flags** on the
  on-box card readout.

## Verdict

**CERTIFIED (control).** The instance is clean for the
8B; A1's Qwythos behavior (F-70) belongs to Qwythos, not
to the serving instance.
