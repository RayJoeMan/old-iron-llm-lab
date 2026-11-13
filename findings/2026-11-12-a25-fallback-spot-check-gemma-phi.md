# Fallback spot-check: Gemma clears the bar twice; phi4-mini has NO DATA — the arm is void (F-94)

- **Date:** 2026-11-12 (certified; phi arm void — no
  measurement exists)
- **Platform:** Fortress — Windows/Vulkan Ollama lane, the
  :11435 (serve-second) instance only; see
  `platforms/fortress-provisional.md` for the machine
- **Source record:** FORTRESS-BACKLOG-2026-11-12.md item
  A25; on-box RESULTS + Errors section, run
  `backlog-a-2026-11-12`

## Question

On the amended classification contract, is gemma3:4b a
viable fallback (plain ≥59 in both of 2 reload sessions
and trap ≥50, the 8B-parity bar) — and how does
phi4-mini read against its provisional drift
certificate?

## Measured result — gemma3:4b arm

- Session 1: plain **60**, trap **51**. Session 2:
  plain **60**, trap **51**. Both bar clauses hold in
  both sessions — and the trap read (51) sits at the
  8B's own level (49–50).

## Measured result — phi4-mini arm: NO DATA

- All three calls (warm, plain, trap) failed with
  **HTTP 404** — the run's entire error list is these
  three lines:
  `a25__phi__warm: HTTP Error 404: Not Found`,
  `a25__phi__plain: HTTP Error 404: Not Found`,
  `a25__phi__trap: HTTP Error 404: Not Found`.
- Cause as recorded: phi4-mini is **absent from the
  :11435 store** (it lives in the other instance's
  store). No generation ran; no score exists; the
  E258-certificate comparison this arm was specified
  to make was not made.

## Verdict

**Gemma arm CERTIFIED:** gemma3:4b is a viable fallback
on the amended contract at 8B parity. **Phi arm VOID —
published as void**, in the same form as the R16 void
arms entry: the question was asked, the arm
produced nothing, and the reason is on the record. It
is re-runnable wherever the model is actually served;
nothing about phi4-mini's classification quality can
be concluded from this battery.
