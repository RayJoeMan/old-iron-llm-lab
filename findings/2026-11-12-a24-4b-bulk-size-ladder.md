# The 4B failure is bulk-induced: clean at chunk 5, collapsed at 15 and 30 (F-93)

- **Date:** 2026-11-12 (certified)
- **Platform:** Fortress — Windows/Vulkan Ollama lane, the
  :11435 (serve-second) instance only; see
  `platforms/fortress-provisional.md` for the machine
- **Source record:** FORTRESS-BACKLOG-2026-11-12.md item
  A24; on-box RESULTS, run `backlog-a-2026-11-12`

## Question

Is qwen3:4b's classification failure a bulk-size
phenomenon (a trainable discipline problem) or present
at every input size (a capability floor)?

## Method

qwen3:4b, think-off, plain titles in chunks of 5 (1
chunk), 15 (4 chunks), 30 (2 chunks), strict-scored per
chunk. Bar: threshold = the largest size at which every
chunk is ≥95% strict.

## Measured result

- Chunk 5: **5/5**.
- Chunks of 15: **14, 0, 15, 0** — two chunks near-clean,
  two at zero.
- Chunks of 30: **0, 0**.
- Recorded threshold: **5**.

## Verdict

**CERTIFIED.** The 4B's failure is bulk-induced and
bimodal at size 15 — the model can do the task at
chunk 5 and falls off a cliff somewhere above it. That
shape (a discipline cliff, not a floor) is what makes
the failure a training target at all; the training
itself is a separate program decision.
