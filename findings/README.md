# Findings — index

Seeded 2026-11-06. Every entry below is **ADOPTED or CERTIFIED** in the
fleet's working program and exported from its private ledger (cited per
entry by experiment id + tuning entry number). All were measured on the
**Mint** platform unless an entry says otherwise.

## 2026-11-04 — the TUNING #97 adoption batch

| Finding | One-line result |
|---|---|
| [Restatement law](2026-11-04-restatement-law.md) | Restating a brief's key requirement verbatim as its final line is the single highest-yield brief rule measured — across 3 models and 3 job classes |
| [Summary coverage line](2026-11-04-summary-coverage-line.md) | One coverage sentence takes summary fact-coverage 14/18 → 18/18; qwen3:8b confirmed as the summary model on a fresh set (27/30) |
| [Metadata routing: phi-4-mini + hook reminder](2026-11-04-metadata-phi-hook-reminder.md) | Hook-form compliance 0/40 → 32/40 at unchanged wall; fresh-set confirmation 18/20 |
| [Flex bullet budget](2026-11-04-flex-bullet-budget.md) | Fact-dense summaries need "3 or 4 bullets," not a hard 3: coverage 9/12 → 12/12 on both models tested |
| [Classification at temperature 0](2026-11-04-classification-greedy-temp0.md) | Greedy decoding locks the classification lane; the 3B's 29/30 stands against both challengers (17/30, 18/30) |
| [Judge-pair disambiguated rubric](2026-11-04-judge-pair-disambiguation.md) | Two text disambiguations in the rubric: guest agreement 18/18 of 20, false positives 9 → 1 — pair use only |

## 2026-11-05 — adoptions #138 / #139

| Finding | One-line result |
|---|---|
| [B4 stack brief](2026-11-05-b4-stack-brief.md) | Gold example + hook-reminder stack: sport-bleed ~0, editorial edits 4.67/5 → 2.0/5 — at temp 0.3 only, B4 class only |
| [Filler-fact scanner as triage checklist](2026-11-05-filler-fact-scanner-triage.md) | Two-stage scanner hits precision/recall 11/11 against a definition-built gold set — adopted as a checklist, explicitly *not* a drop gate |

## 2026-11-06 — adoption filings (review of TUNING #140–#185)

| Finding | One-line result |
|---|---|
| [Summary merge loop](2026-11-06-summary-merge-loop.md) | Select-then-write → ruler-check → append-only repair: chunked-merge coverage 25/25, certified on fresh seeds, at ~half the plain merge's wall — with a named checker-independence exception |
| [Gemma = classification fallback](2026-11-06-gemma-classification-fallback.md) | Anchored brief: 59/60 hard + 30/30 standard, replicate-certified — adopted as fallback of record; the champion swap was considered and *declined* |
| [Metadata fallback Description: label line](2026-11-06-metadata-fallback-description-label.md) | One restated final line: label compliance 5/40 → 39/40, certified 40/40 ×3 — and a second restatement does *not* stack |
| [VL sport-context line](2026-11-06-vl-sport-context-line.md) | One opening line in a supervised vision brief: cross-sport confusion 3 → 0 at a clean-count tie |
| [Gemma = summary quality fallback](2026-11-06-gemma-summary-quality-fallback.md) | The program's first perfect summary score (30/30, zero inventions) — adopted for short sources only; production routing unchanged |

## Not seeded (deliberately)

- **Fortress findings** — none. The platform is pre-build and its tuning
  chain was still running at staging; only platform facts appear, in
  `platforms/fortress-provisional.md`.
- **Other adopted Mint results outside the tasked seed set** (e.g. the
  long-input chunking rule, the classification anchor package, the
  structured-drafting model adoption, embedding-dedupe calibration) —
  adopted in the working ledger and referenced inside seeded entries
  where a seeded finding depends on them, but not yet exported as
  standalone entries in this v0.1 scaffold.
- **Bar-met-but-not-adopted and pending-decision results** (e.g. a
  B4 blind-repair stage that met every clause and awaits the owner's
  pipeline decision; a hook temperature declined on judgment) — not
  findings until adopted, per the repo's own rule.
- **Raw eval text and ruler values** — excluded on sensitivity grounds;
  see `evals/README.md`.
