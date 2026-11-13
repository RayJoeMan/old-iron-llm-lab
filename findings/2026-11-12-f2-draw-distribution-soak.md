# The 732-cycle soak: under KV-prefix cycling the trap draw is a constant — 47 / 49 (F-100)

- **Date:** 2026-11-12 (certified)
- **Platform:** Fortress — Windows/Vulkan Ollama lane, the
  :11435 (serve-second) instance only; see
  `platforms/fortress-provisional.md` for the machine
- **Source record:** FORTRESS-BACKLOG-2026-11-12.md
  filler F2; on-box RESULTS (Soak cycles section), run
  `backlog-a-2026-11-12`

## Question

What does the empirical distribution of a Trap-60 draw
look like over a long soak — the per-model distribution
the certification power table (B31) will be built from?

## Method

Repeat [apply F* → 3B trap → 8B trap] until the chain's
18:20 CT stop, where F* is the first CHANGES factor in
the pre-registered priority order (A28 > A5 > A6 >
A3). A28, A5 and A6 changed nothing; A3 did — so F* is
the **KV-prefix** factor (F-72), applied every cycle.

## Measured result

- **732 cycles**, numbering contiguous, all under the
  kv_prefix factor.
- Cycle 1: 3B **52**, 8B **49**.
- Cycles 2–732 (**731 cycles**): 3B **47**, 8B **49** —
  no other value pair occurs. The distribution the soak
  was built to measure has, on this lane, essentially
  one point per model after the opening cycle.

## Verdict

**CERTIFIED.** Under repeated application of the one
factor that measurably selects draws, the draws do not
wander: 47 (3B) and 49 (8B) are constants of this lane
across 731 consecutive cycles. Certification power
planning can treat the trap scores as fixed points with
an opening-cycle exception, not as samples from a wide
distribution.
