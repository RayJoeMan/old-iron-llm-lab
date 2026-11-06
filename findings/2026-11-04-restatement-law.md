# The restatement law — a brief's key requirement, restated verbatim as its final line

- **Date:** 2026-11-04 (adopted)
- **Platform:** Mint — see `platforms/mint.md` (Ollama 0.40.13, GTX 960M sm_50)
- **Source record:** TUNING #97(a); experiments E75, E85, E89, E96 (boundaries: E94, E99)

## Question

Across unrelated job classes, briefs kept failing on the *one requirement that
mattered most* (a length, a coverage demand, a format rule) while satisfying
everything else. Does restating that requirement — verbatim, as the brief's
final line — fix it, and where does the trick stop working?

## Method

The same intervention measured independently in four places: three models
(qwen3:8b, phi-4-mini, gemma3:12b), three job classes (long-form length
compliance, summary coverage, metadata hook-form), each against its own
frozen eval and pre-registered scoring.

## Measured result

| Experiment | Axis | Without restatement | With restatement |
|---|---|---|---|
| E75 (blog length) | Mean word-count error | 60.8 | **7.3** |
| E85 (summary coverage) | Facts covered | 14/18 | **18/18** |
| E89 (phi metadata hooks) | Hook-form compliance | 0/40 | **32/40** |
| E96 (gemma metadata hooks) | Hook-form compliance | 6/40 | **20/40** |

**Measured boundaries (part of the rule, not footnotes):**

- **Never inflate the restated figure.** Restating a *larger* number than the
  brief itself specified collapsed the gain entirely (E94: in-range 0/4,
  mean error back up to 28.5). The restatement must be the brief's own
  requirement, exactly as stated.
- **The line cannot outvote contradictory source text.** When the task text
  itself was written in the wrong domain's vocabulary, bleed measured 2/5
  before and after (E99) — a restatement is not a counterweight to the
  assignment's own wording.

## Verdict

**ADOPTED as a standing brief-writing rule for all Mint briefs:** a brief's
most important requirement is restated verbatim as its final line, exactly
as stated. Several later findings in this repo are applications of this law
(the coverage line, the hook reminder, the Description: label line) — and
its limits are findings too (a second label restatement does not stack;
see the metadata fallback entry).
