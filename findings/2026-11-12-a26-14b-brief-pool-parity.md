# 14B brief pool: 24/24 clean — parity with the 8B (F-95)

- **Date:** 2026-11-12 (certified)
- **Platform:** Fortress — Windows/Vulkan Ollama lane, the
  :11435 (serve-second) instance only; see
  `platforms/fortress-provisional.md` for the machine
- **Source record:** FORTRESS-BACKLOG-2026-11-12.md item
  A26; on-box RESULTS, run `backlog-a-2026-11-12`

## Question

Does qwen3:14b match the 8B's brief-pool cleanliness at
the original condition?

## Method

Full 24-input brief pool ×1 at the original condition
(temp 0.3, seed 42, num_predict 900). Bar: parity iff
24/24 clean with 0 leaks.

## Measured result

- **24/24 clean**, 0 omissions, 0 structure flags on
  the card readout — identical to the 8B control
  (F-80).

## Verdict

**CERTIFIED (control).** On brief work the 14B and the
8B are indistinguishable on this lane; brief quality is
not a reason to pay the 14B's serving cost.
