# Gemma as classification fallback — certified on both instruments; champion swap declined

- **Date:** 2026-11-06 (adopted as fallback; champion question closed the same day)
- **Platform:** Mint — see `platforms/mint.md`
- **Source record:** Nov 6 adoption filing #2; experiments E149, E152,
  E164, E166, E183 (the warning: E176); champion record E34, E120

## Question

A 12B model (gemma3:12b) posted classification numbers above the locked
3B champion's. Six experiments later, the picture looked contradictory:
a perfect score on one instrument, a collapse on another. Which brief
was each number measured under?

## Measured result — it was never a contradiction

Under the **anchored brief** (the production brief: four worked anchor
examples prepended), gemma is **replicate-certified on both instruments**:

| Instrument | gemma3:12b (anchored) | Champion (llama3.2:3b) |
|---|---|---|
| Hard set (60 irregular titles) | **59/60**, ×5 byte-identical calls, sole miss #3 | 55/60 |
| Standard set (30 pattern-built titles) | **30/30**, ×2, every family 6/6 | 29/30 |

It fixes all five champion misses, including a phrase family no brief
intervention had ever moved — at **~3.6× the wall** (187 s vs ~52 s per
60-set).

**The collapse, and what it actually proves:** with anchors *removed*,
gemma scores 60/60 on the irregular hard set (×5, certified) but
**24/30 ×4 byte-identical** on the pattern-built standard set — it rides
a positional cycle and **never emits one entire label family**. Anchors
are not small-model scaffolding; on patterned inputs they are
**cycle-breakers at every scale**. Gemma's failure mode under brief
perturbation is catastrophic and family-wide, where the 3B's is graded
(52–55/60 under the same perturbations, never a family collapse).

## Verdict

**ADOPTED: gemma3:12b is the classification FALLBACK OF RECORD**, under
the anchored brief on both instruments. The zero-anchor variant is
certified **only** for irregular sets and is **prohibited on
pattern-built sets**. Any future brief change on a gemma lane must be
re-certified on **both** instruments.

**The champion swap was considered on complete evidence and DECLINED**
(owner ruling, 2026-11-06: "keep Gemma as fallback only"). The trade was
fully measured — +4/60 and +1/30 quality against 3.6× wall on every call
plus a re-certification tax on every future brief change, at low lane
volume where the champion's miss family is known and editorially handled.
llama3.2:3b remains the production classification champion.
