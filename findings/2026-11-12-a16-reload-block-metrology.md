# Reload-block metrology: Qwythos unmoved; the 14B's trap drops 55 → 45 under reload (F-85)

- **Date:** 2026-11-12 (certified)
- **Platform:** Fortress — Windows/Vulkan Ollama lane, the
  :11435 (serve-second) instance only; see
  `platforms/fortress-provisional.md` for the machine
- **Source record:** FORTRESS-BACKLOG-2026-11-12.md item
  A16; on-box RESULTS, run `backlog-a-2026-11-12`

## Question

Under a paired reload-block protocol (unload → fixed
prewarm → plain-60 → trap-60, 4 blocks, AB/BA, two
immediate repeats per arm), is there a reload
intervention effect on the two trap leaders — Qwythos
and qwen3:14b?

## Method

As specified in the item; an intervention effect counts
only if hashes change in ≥2/4 blocks with unchanged
immediate repeats. Strength clauses: Qwythos plain
60/60 and trap ≥55 every block; 14B trap ≥54.

## Measured result

- **Qwythos — no effect (`met = false` for the
  intervention bar).** All 4 blocks byte-identical:
  trap hash `5250910b…`, trap strict **57**, plain
  strict **60**, immediate repeats identical in every
  block, 0 pair changes. Both strength clauses hold in
  every block (60 plain, 57 ≥ 55 trap).
- **qwen3:14b — effect present (`met = true`).** Reload
  blocks change the draw in 2 of 4 pairs: reload-arm
  trap hash `12517cb8…` at strict **45** vs control
  `bf1494f2…` at **55**; plain 60 in all runs. Reload
  costs the 14B 10 trap points and breaks its ≥54
  strength clause; the control condition holds 55.

## Verdict

**CERTIFIED.** Reload is model-specific as a session
variable: nothing for Qwythos (and nothing for the
3B/8B in F-74/F-79), a real 10-point trap cost for the
14B. Any 14B trap read must declare its reload state.
