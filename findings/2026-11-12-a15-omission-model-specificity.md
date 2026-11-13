# The omission is Qwythos-specific: the 8B omits 0/30 on the same input (F-84)

- **Date:** 2026-11-12 (certified)
- **Platform:** Fortress — Windows/Vulkan Ollama lane, the
  :11435 (serve-second) instance only; see
  `platforms/fortress-provisional.md` for the machine
- **Source record:** FORTRESS-BACKLOG-2026-11-12.md item
  A15; on-box RESULTS, run `backlog-a-2026-11-12`

## Question

Is the Source-URL omission a Qwythos behavior or a
property of the B07 input that any model would trip on?

## Method

qwen3:8b, target input B07, seeds 1–30 at temp 0.3 —
the A12 protocol with the model swapped. Bar:
Qwythos-specific iff the 8B shows 0/30 while A12 showed
≥3/30.

## Measured result

- **8B: 0/30 omissions** (0 omissions, 0 structure flags
  on the card readout), against Qwythos's **15/30**
  (F-81). The bar is met exactly as registered.

## Verdict

**CERTIFIED.** The omission is model-specific
(Qwythos), not input-specific: the input is innocent,
and — combined with F-82 — the behavior is best stated
as *Qwythos omits on some inputs at high rate; the 8B
does not omit on the worst of them at all*.
