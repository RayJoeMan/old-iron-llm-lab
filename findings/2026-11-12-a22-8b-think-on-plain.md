# Think-on leaves 8B plain at 60/60 in all cycles (F-91)

- **Date:** 2026-11-12 (certified)
- **Platform:** Fortress — Windows/Vulkan Ollama lane, the
  :11435 (serve-second) instance only; see
  `platforms/fortress-provisional.md` for the machine
- **Source record:** FORTRESS-BACKLOG-2026-11-12.md item
  A22; on-box RESULTS, run `backlog-a-2026-11-12`

## Question

Is think-on's cost to the 8B visible on the plain
(unamended) classification set, cross-session?

## Method

3 reload cycles of plain-60 under think-on. Bar: the
cost is stable iff all 3 cycles score ≤58 with a COMEDY
deficit; any 60/60 reads as draw noise under the bar's
terms.

## Measured result

- Stricts: **60, 60, 60** — per-label **12/12 in every
  label in every cycle**. No cycle at or below 58; no
  COMEDY deficit anywhere.

## Verdict

**CERTIFIED.** Think-on's 8B damage is specific to the
trap contract (F-89: 0/60 ×3); on the plain set it costs
exactly nothing across three sessions. The think
question on this lane is a contract question, not a
model question.
