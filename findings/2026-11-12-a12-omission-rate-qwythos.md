# Qwythos omits the Source-URL line on B07 in 15 of 30 seeds (F-81)

- **Date:** 2026-11-12 (certified)
- **Platform:** Fortress — Windows/Vulkan Ollama lane, the
  :11435 (serve-second) instance only; see
  `platforms/fortress-provisional.md` for the machine
- **Source record:** FORTRESS-BACKLOG-2026-11-12.md item
  A12; on-box RESULTS, run `backlog-a-2026-11-12`

## Question

How often does Qwythos's known omission — dropping the
`Source-URL:` line on the target input B07
(comp-violent-gentlemen) — actually fire under seed
resampling at temp 0.3?

## Method

Target input, seeds 1–30 at temp 0.3, omission counted
per draw. Pre-registered read: ≥3/30 = a real stochastic
mode; 1–2/30 = rare; 0/30 = absent (upper bound ≈11%).

## Measured result

- **15/30 omissions** — a 50% rate, far past the ≥3/30
  clause. The omission is a coin-flip stochastic mode of
  this input under this model, not an edge case.

## Verdict

**CERTIFIED.** The B07 omission is a real, high-rate
stochastic mode. Whether it is specific to the input
(F-82) and to the model (F-84) is measured separately;
whether the fix line survives temp 0.3 is F-83.
