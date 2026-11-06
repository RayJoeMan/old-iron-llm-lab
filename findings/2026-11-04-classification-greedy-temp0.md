# Classification at temperature 0 — greedy decoding locks the lane

- **Date:** 2026-11-04 (adopted)
- **Platform:** Mint — see `platforms/mint.md`
- **Source record:** TUNING #97(e); experiments E77, E34, E80, E87

## Question

A 5-label classification lane showed run-to-run wobble under sampled
decoding, and two newer models wanted the job. Does greedy decoding plus
the incumbent model beat both challengers?

## Method

Fixed title sets with fixed keys (deterministic scoring — the key is the
checker; no model grades this lane). Champion: llama3.2:3b. Challengers:
phi-4-mini and gemma3:12b (4B-class/12B arms as recorded).

## Measured result

- The 3B's semantic record — **29/30** (E34) — stands unchallenged:
  phi-4-mini **17/30** (E80) and gemma **18/30** (E87) fail identically
  on the same tone boundaries.
- E77's greedy (temp 0) arm is the clear-win candidate the batch confirms:
  deterministic output at the champion's accuracy.

## Verdict

**ADOPTED:** classification runs **llama3.2:3b at temperature 0**, locked.
Routing was declared closed unless a new model family landed on the box —
a clause that mattered: when gemma3:12b later posted much stronger
numbers, it entered through the full adoption process as a *fallback*
(see the 2026-11-06 gemma classification finding), not by quietly
replacing a locked champion. Determinism support in the later record:
four consecutive replicates of the adopted profile in one warm session
are byte-identical (55/60 on the hard set, identical miss set).
