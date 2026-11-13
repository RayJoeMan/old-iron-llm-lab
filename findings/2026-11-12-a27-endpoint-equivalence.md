# Endpoint envelope equivalence: /api/generate ≡ /api/chat on everything tested (F-96)

- **Date:** 2026-11-12 (certified)
- **Platform:** Fortress — Windows/Vulkan Ollama lane, the
  :11435 (serve-second) instance only; see
  `platforms/fortress-provisional.md` for the machine
- **Source record:** FORTRESS-BACKLOG-2026-11-12.md item
  A27; on-box RESULTS, run `backlog-a-2026-11-12`

## Question

Do the two Ollama endpoint envelopes (/api/generate vs
/api/chat) produce different results for the same work —
a difference that would have to be attributed to
endpoint/template treatment rather than the model?

## Method

Qwythos plain-60 + brief pool, 2 paired blocks, roles
mapped explicitly between the envelopes. Bar: Q0 — no
new failures vs the paired control.

## Measured result

- Plain blocks: generate strict **60**, chat strict
  **60**, **hashes equal** — in both paired blocks.
- Brief pairs: 6 pairs checked, **0 differences**.

## Verdict

**CERTIFIED.** On this lane the endpoint envelope is
not a variable: identical hashes, identical scores,
identical briefs. Endpoint choice can be made on
client convenience alone.
