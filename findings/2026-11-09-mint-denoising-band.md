# The Mint de-noising band: ±2% on eval tok/s — and at a pinned seed there are exactly two draws

- **Date:** 2026-11-09 (adopted)
- **Platform:** Mint — see `platforms/mint.md`
- **Source record:** TUNING #236 (E233, two sessions);
  adopted in the 2026-11-09 adoption review as the
  standing Mint measurement constant (the Fortress lane
  applies the same band — see F-65/F-66)

## Question

How much can an eval-rate reading move between sessions
before the move means something — and what actually
selects which reading you get?

## Method

Three fixed instruments (B1/B2/B3 prompt files, md5-verified
copies), pinned seed 42, blocked series per session,
two full sessions plus a post-unload probe pair.

## Measured result

- Session 2 reproduced session 1: cross-session mean
  shifts **−0.19% / +0.34% / +0.37%** across the three
  instruments; the widest within-session range across
  both sessions was 1.03%. Every in-protocol reading
  (**44/44 series calls**) sits inside **±2%** — adopted
  as the band.
- **Output identity:** all 22 session-2 series outputs
  were **byte-identical** to session 1, position for
  position.
- **The two-draw rule:** after a full model unload, both
  probe calls reproduced the session-1/session-2 first
  outputs byte-for-byte — a third sighting of each. At a
  pinned seed each instrument has exactly **two draws —
  the uncached draw and the cached draw — selected by
  prompt-cache state**, not by session or thermal state.
- Hygiene rules adopted with the band: **discard or
  separately label first outputs** in any seed-pinned
  comparison series; **never compare prompt-eval or wall
  figures across cache states** (uncached prompt_eval
  37.6–139.0 vs cached 637–5,250 tok/s on identical
  prompts).
- One named out-of-band reading, kept out of the band's
  calibration: a solo-resident post-unload probe decoded
  at +2.96% over its series mean — filed as an n=1
  residency effect, not a band revision.

## Verdict

**ADOPTED** as the standing measurement constant: a delta
inside ±2% on eval tok/s is noise; a delta outside it is a
signal worth investigating. Any seed-pinned comparison
that ignores the two-draw rule is measuring the prompt
cache, not the model.
