# KV-prefix state changes the trap draw (F-72)

- **Date:** 2026-11-12 (certified)
- **Platform:** Fortress — Windows/Vulkan Ollama lane, the
  :11435 (serve-second) instance only; see
  `platforms/fortress-provisional.md` for the machine
- **Source record:** FORTRESS-BACKLOG-2026-11-12.md item A3;
  on-box RESULTS, run `backlog-a-2026-11-12`

## Question

Is call history — specifically the KV prefix a session
carries into a call — a variable that moves the 3B's
Trap-60 draw?

## Method

llama3.2:3b Trap-60 after [plain-60 ×3] vs after [a short
unrelated prompt ×2], prompt_eval_count logged; the
record's verdict flag is `changes`.

## Measured result

- Base sequence hashes: `b6db228d…`, `3c06f862…`,
  `3c06f862…`; treatment sequence: `3c06f862…`,
  `3c06f862…`.
- Recorded verdict: **changes = true**. Prefix history
  selects which of the session's two draws (F-71) a call
  lands on — with a plain-60 history the session settles
  to the second hash and stays there.
- This was the battery's first CHANGES factor in the
  pre-registered priority order, so it became the soak
  factor F* for the F2 draw-distribution soak (F-100).

## Verdict

**CERTIFIED.** Call history (prefix-reuse depth) is a
real session variable on this lane: it does not add
noise, it selects the draw.
