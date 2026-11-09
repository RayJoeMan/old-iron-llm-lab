# Findings — index

Seeded 2026-11-06. Every entry below is **ADOPTED or CERTIFIED** in the
fleet's working program and exported from its private ledger (cited per
entry by experiment id + tuning entry number). The 2026-11-04 →
2026-11-06 batches were measured on the **Mint** platform; the
2026-11-08 batch was measured on **Fortress** (each Fortress entry
says so, and cites its platform page).

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

## 2026-11-08 — Fortress R10 (mixed-GPU split battery)

Measured on **Fortress** (M4000 sm_52 + RTX 4000 sm_75, llama.cpp
b12136) — see `platforms/fortress-provisional.md` for the settled
fingerprint and the B3 probe definition. All seven certified the same
day by the program's certification review.

| Finding | One-line result |
|---|---|
| [Solo baselines: RTX 4000 vs M4000](2026-11-08-fortress-solo-baselines-rtx4000-m4000.md) | RTX wins every solo class — 8B decode 55.29 vs 11.4 tok/s, long-prompt prefill 1,441 vs 99; tensor cores are a prefill multiplier (14.5×), not just decode (4.85×) |
| [F-24's M4000 rate NOT REPRODUCED](2026-11-08-f24-m4000-rate-not-reproduced.md) | Correction: the earlier M4000 8B ≈35.3 tok/s figure does not reproduce — four independent reads agree at ≈11.0–11.6; F-24's residency and prefix-cache results stand |
| [Layer-split policy on mixed GPUs](2026-11-08-layer-split-policy-mixed-gpus.md) | Splitting a fittable 8B loses 74%; the 14B split weighted ts 2,1 toward the fast card hits 12.43 tok/s (+43% over even); tensor split runs and validates but is ~2.2× slower |
| [MoE placement: dual-GPU split](2026-11-08-moe-placement-dual-gpu-split.md) | The 13.8 GB 30B MoE split across both cards is fastest (22.57) *and* lightest on RAM (784 MiB RSS); best one-card placement is RTX + full CPU offload + 4 GiB expert cache (17.71) |
| [Expert cache capacity cliff](2026-11-08-moe-expert-cache-capacity-cliff.md) | Decode vs cache size: 4.65 → 2.70 at 1 GiB (−42%) → 6.30 at 2 GiB → 17.71 at 4 GiB; no prefill tax; cache cannot combine with partial `-ncmoe` offload in this build; hit rate not instrumented, none claimed |
| [Two cards are two lanes](2026-11-08-two-cards-two-lanes-replicas.md) | Concurrency and same-model replicas run at ~101% of the sequential sum; replicas beat the best single card +22% and the split of the same model 4.7× |
| [NUMA is a no-op under WSL](2026-11-08-numa-noop-dual-socket-wsl.md) | Placement is flat (±2.6%) on both the GPU split and the CPU-offload path; the F-29 `distribute` wedge is scoped as surface-specific |

## Not seeded (deliberately)

- **Fortress findings outside the R10 battery** — the pre-build rounds
  (F-01 → F-34) are not exported as standalone findings; the two that
  the R10 certification directly touched appear above (the F-24
  correction, F-36) or are cited inside the R10 entries. The platform
  page is `platforms/fortress-provisional.md` (filename kept;
  contents now the settled 2026-11-08 fingerprint).
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
