# Findings — index

Seeded 2026-11-06. Every entry below is **ADOPTED or CERTIFIED** in the
fleet's working program and exported from its private ledger (cited per
entry by experiment id + tuning entry number). The 2026-11-04 →
2026-11-06 batches were measured on the **Mint** platform; the
2026-11-08 batches were measured on **Fortress** (each Fortress entry
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
| [Two cards are two lanes](2026-11-08-two-cards-two-lanes-replicas.md) | Concurrency and same-model replicas run at ~101% of the sequential sum; replicas beat the best single card +22% and the split of the same model 4.7× (np4 figure corrected by F-45 — timings-sum; wall ≈1.0×) |
| [NUMA is a no-op under WSL](2026-11-08-numa-noop-dual-socket-wsl.md) | Placement is flat (±2.6%) on both the GPU split and the CPU-offload path; the F-29 `distribute` wedge is scoped as surface-specific |

## 2026-11-08 — Fortress R11 (speculative decoding + ceilings)

Measured on **Fortress** (same settled fingerprint and B3 probe as
the R10 batch above), extending the certified R10 controls:
speculative decoding, the expert-cache and context ceilings,
split-server parallelism re-measured by wall clock, MoE prefill,
and a harness cross-check of F-40. All seven certified the same
day by the program's certification review.

| Finding | One-line result |
|---|---|
| [Speculative decoding: draft length](2026-11-08-speculative-decoding-draft-length.md) | On the solo 8B, a 0.6b draft at n-max 4 *loses* 14% despite 95% acceptance; n-max 16 wins **+42%** — draft length, not acceptance, is the deciding variable; attaching a draft costs ~20% of prefill at every length |
| [Speculative decoding fails on splits](2026-11-08-speculative-decoding-splits-fail.md) | GPU draft on the 14B split cannot allocate (896 MiB MTP context, OOM at all lengths); CPU draft collapses −70…−90%; the MoE split loses 77% at n-max 4 and **crashes 2/2 at n-max 8** (`ggml-cuda.cu:111: CUDA error: out of memory` in decode) — with the substituted 0.6b draft declared (qwen3:4b absent from the store, download cap) |
| [Expert-cache ceiling on 8 GB](2026-11-08-expert-cache-ceiling-8gb.md) | RTX cache init fails at 6144 MiB — the legal range ends between 4096 (works) and 6144; on the M4000 the 4096 cache pays **+57%** (4.98 → 7.83), so F-38's ordering stands |
| [Split parallelism: wall-clock correction](2026-11-08-split-parallelism-wall-clock-correction.md) | Both metrics reported: the MoE split is timings-sum 36.15 / **wall 22.45** at np4 and ≈single-stream at np8 — F-40's "1.60×" corrected to **wall ≈1.0×**; the 14B split at np4 scales a real **2.02× by wall** (25.09 vs 12.43) |
| [14B split context ceiling](2026-11-08-14b-split-context-ceiling.md) | ctx 32768 fails at init (`failed to allocate buffer for kv cache`); KV sized by per-card VRAM deltas (≈993 MiB per +8192 tokens — no KV log line at default verbosity); at 16384 B3 is unchanged and decode at 4,241-token depth pays only −14% |
| [MoE prefill: cache convergence](2026-11-08-moe-prefill-cache-convergence.md) | Longprobe (4,241 tok): dual split prefill 154.58 vs one-card cache arm 136.52 (+13%, decode +41%, 1/18th the RAM) — but the gap collapses from +73% at B3 as prompts grow; one-card prefill is monotone in cache size (106.53 → 116.5 → 136.52) |
| [Concurrency cross-check](2026-11-08-concurrency-cross-check.md) | F-40's lossless concurrency reproduces through CUDA_VISIBLE_DEVICES-masked replica instances: 77.99 / 77.74 vs the 77.42 sequential sum (≈101%) — with the substituted 3B+8B pair declared and the specified qwen3:4b hetero-replica measurement explicitly **NOT RUN** (closed by F-49, 2026-11-09) |

## 2026-11-09 — Fortress R11.5 (speculative-decoding closure)

Measured on **Fortress** (same settled fingerprint and B3 probe as
the R10/R11 batches above), an overnight closure battery between
the CPU-swap hardware sessions — deliberately GPU-side only, so
every result stays valid across the swap. It finishes the three
questions the R11 battery left open: the far side of the
draft-length curve, draft placement across devices, whether a
mostly-one-card 14B can host a draft at all — and it runs the one
measurement F-48 had to leave NOT RUN. All four certified by the
program's certification review.

| Finding | One-line result |
|---|---|
| [Heterogeneous replicas as specified](2026-11-09-heterogeneous-replicas-as-specified.md) | The pair F-48 had to substitute away from — qwen3:4b (M4000) + qwen3:8b (RTX) — runs concurrently at **98–99% of its sequential sum** (71.42 / 71.95 vs 72.69); closes F-48's NOT RUN item, the last open arm of the R11 battery |
| [Draft-length plateau at 16](2026-11-09-speculative-decoding-draft-length-plateau.md) | The F-42 curve is flat from 16 to 32 (79.02 / 78.56 / 80.11; acceptance 0.82 → 0.65): the n16 control reproduces F-42 exactly (79.02 vs 78.69, acceptance identical at 0.8194), and F-42's n-max 16 rule stands bounded on both sides |
| [Cross-device draft is harmful](2026-11-09-cross-device-draft-harmful.md) | Draft on the M4000, target on the RTX (VRAM-verified placement): eval 30.7 — **−61% vs same-card drafting and −44% vs no draft at all**; on this host speculative decoding is a same-card technique |
| [14B partial offload + spec: collapse](2026-11-09-14b-partial-offload-spec-collapse.md) | A mostly-one-card 14B *can* host a draft — load ladder ngl 32 fails, ngl 28 loads — but decodes at **1.33 / 0.79 tok/s**, the worst 14B configuration measured; the file also records the run's channel-integrity incident (a phantom completion notice, discarded; only JSON-verified figures ledgered) |

## 2026-11-09 — Fortress R15 (serving & depth)

Measured on **Fortress** (same settled fingerprint and B3 probe as
the R10/R11 batches above). All concurrency figures are wall-clock
aggregates (the F-45 rule). All six certified by the program's
certification review; last battery recorded before the CPU swap —
pre-swap v1 controls.

| Finding | One-line result |
|---|---|
| [14B split serving flattens after np4](2026-11-09-14b-split-serving-flattens-np4.md) | Wall aggregate 11.62 → 18.07 → 24.99 → 26.96 across np1/2/4/8 — np4 replicates the F-45 control (25.09); +8% only to np8 (F-53) |
| [Solo-8B serving peaks at np4](2026-11-09-solo-8b-serving-peak-np4.md) | 52.46 → 83.25 → **107.68** → 101.44: aggregate peaks at 4 slots, **2.05×** single-stream, and recedes at np8 (F-54) |
| [MoE split saturation; timings overstate ~1.9×](2026-11-09-moe-split-saturation-timings-overstate.md) | Wall saturates by np4 (23.56) while timings sums reach 43.71 — the widest wall-vs-timings gap in the program (F-55) |
| [Long decode: KV depth, not thermals](2026-11-09-long-decode-kv-depth-not-thermals.md) | 4× 8,192-token generations: median **43.54**, ~2.8% decline across passes, windowed decay ~48.5 → ~41 with KV growth; RTX peak 85 °C, no cliff (F-56) |
| [Coder-30B first baseline](2026-11-09-coder-30b-first-baseline.md) | ud-qwen3-coder:30b dual split: prompt 108.0 / eval **22.18** — statistically tied with the instruct MoE in the same placement (F-57) |
| [Spec decoding collapses on the 4B; sub-1B drafts](2026-11-09-spec-decoding-4b-collapse-sub1b-drafts.md) | The 0.6b draft that wins +42% on the 8B **loses ~75–80% on the 4B** (acceptance 0.10–0.20 vs 0.8194) — the 4B runs draftless; on 8 GB at ctx 8192, same-card drafts are sub-1B only (F-58) |

## 2026-11-09 — Fortress R16 (headroom & ceilings)

Measured on **Fortress** (same fingerprint and probe). F-59 → F-64
certified by the program's certification review; T6 and T7 produced
no measurement and are filed as void, per the honesty rules.

| Finding | One-line result |
|---|---|
| [Solo-8B context ceiling: 32768](2026-11-09-solo-8b-context-ceiling-32768.md) | ctx 32768 loads **only with q8_0 KV** (7,417 MiB; 29,681-token fill, decode 19.66 at depth); f16 fails; 65536 fails under both quants (F-59) |
| [KV quantization: cheap insurance solo](2026-11-09-kv-quantization-solo-cheap-insurance.md) | At ctx 16384: f16 53.38 → K-only q8_0 51.97 (−2.6%, −532 MiB) → K+V 50.82 (−4.8%, −1,072 MiB); the split-era kvq8 failure was a split effect, not a quant defect (F-60) |
| [Expert-cache ceiling bisected](2026-11-09-expert-cache-ceiling-bisected.md) | 5120 MiB loads on **both** cards (RTX eval 29.88, +69% vs 4096; M4000 10.18, +30%); 6144 fails on both — ceiling ∈ (5120, 6144] MiB (F-61) |
| [Partial offload of the 14B: closed](2026-11-09-partial-offload-14b-closed.md) | Draftless ngl 20/24/28 → 2.10 / 2.53 / 3.14 (ngl 32 fails); beats F-52's with-draft 1.33 but sits at ~¼ of the split — the dual split stands (F-62) |
| [Solo-8B prefill at 8,481 tokens](2026-11-09-solo-8b-prefill-8481.md) | **1270.29 tok/s** at 8,481 tokens; the ~17k and ~34k arms failed to load — no deeper rates exist, certification scoped to the loadable arm (F-63) |
| [Embed batch-invariance](2026-11-09-embed-batch-invariance.md) | nomic-embed on the standing Ollama lane: 16.67 / 16.67 / 17.02 docs/s at batch 1 / 8 / 32 — batching buys nothing (F-64) |
| [R16 void arms (T6, T7)](2026-11-09-r16-void-arms-t6-t7.md) | **VOID — no numbers claimed.** T6: all draft-variety arms died at draft-load VRAM OOM, question open. T7: VL baseline voided by a harness defect (symlinked Ollama manifests rejected); repaired and produced in R17 (F-69) |

## 2026-11-09 — Fortress R17 (replication & audit battery)

Measured on **Fortress** (same fingerprint and probe). R17 was the
standing ungated filler battery: replicate the certified controls
under fresh seeds, extend the embed range, and produce the VL
baseline R16-T7 voided. The battery was audited by **two
independent audit passes that agree**; F-numbers were assigned at
this export.

| Finding | One-line result |
|---|---|
| [Fresh-seed replicates: controls hold](2026-11-09-fresh-seed-replicates-controls-hold.md) | Solo 8B 54.44 vs 55.29 (**−1.54%, in band**); 14B split 12.44 vs 12.43 (**+0.08%**); MoE split 21.99 vs 22.57 (**−2.57%, outside the ±2% band, low**) — with the 54-token early-EOS caveat on every MoE rep (F-65) |
| [Soak replicate: thermal baseline](2026-11-09-soak-replicate-thermal-baseline.md) | F-56's soak replicates: median **42.75 vs 43.54 (−1.81%, in band)**; **RTX peak 85 °C — exact match** to the control; the covers-OFF baseline (F-66) |
| [Dual-card co-soak, one hour](2026-11-09-dual-card-co-soak.md) | Full 3600.6 s, no abort; peaks RTX 85 °C / 124.43 W, M4000 79 °C / 97.94 W; combined wall **65.98 tok/s** — with the JSON-vs-stdout tally discrepancy published, not smoothed (F-67) |
| [Embed invariance to 128](2026-11-09-embed-invariance-to-128.md) | Batch 64 → **17.02**, batch 128 → **17.09** docs/s: F-64's batch-invariance extends 1 → 128 (F-68) |
| [VL baseline: RTX only; M4000 launch timeout](2026-11-09-vl-rtx-baseline-m4000-launch-timeout.md) | **PARTIAL.** RTX per-image medians 96.68 / 90.51 / 85.90 / 81.37 — the first Fortress VL control; batch-of-4 arm HTTP 400; M4000 set HTTP 500, cause established: ggml-cuda **launch timeout** in the Maxwell runner, store exonerated (F-69) |

## 2026-11-09 — Mint adoptions (#221 / #234 / #236)

Measured on the **Mint** platform (see `platforms/mint.md`),
adopted in the 2026-11-09 adoption review. These three complete
the Mint seed alongside the Nov 4–6 batches.

| Finding | One-line result |
|---|---|
| [Restate-then-label classification](2026-11-09-restate-then-label-classification.md) | A ≤8-word reason before the label: **58/60 vs 55/60** (E220), **59/60 vs 56/60** on a fresh set (FF-1) — at 2.16× tokens; the gain is a copy-then-label effect (59/60 reasons were title echoes), adopted as the standing contract (TUNING #221 + #237) |
| [Chunk-fuse long-source coverage](2026-11-09-chunk-fuse-long-source-coverage.md) | 47k-char fixture: fused coverage **17/20 and 18/20, zero inventions**, stage-1 union 19/20 both seeds — vs single-pass 4/20 truncated; plain fuse is *not* a production final (TUNING #234) |
| [Mint de-noising band ±2%](2026-11-09-mint-denoising-band.md) | Cross-session shifts ≤0.37%, 44/44 readings in band; at a pinned seed each instrument has exactly **two draws** (cached / uncached) selected by prompt-cache state — the standing measurement constant (TUNING #236) |

## 2026-11-10 — Fortress R19 (INTERIM — battery still running)

| Finding | One-line result |
|---|---|
| [R19 INTERIM — 128 GB runs a 120B](2026-11-10-r19-interim-128gb-proof.md) | **INTERIM, no F-numbers.** gpt-oss-120b MXFP4 from system RAM: fit best **6.71**, B3 ngl0 median **6.77**, prefill 19.19 @4k / 26.86 @16k, **28,337-token fill at ctx 32768**; VL **survives on the M4000** at reduced config; r19_5 quality arm captured no content — no verdict claimed; Flash-Next arm pending |

## 2026-11-12 — Fortress Tranche A (session-variable battery, Windows lane)

Measured on **Fortress** — the Windows/Vulkan Ollama
lane (the :11435 serve-second instance), a different
serving stack from the WSL llama.cpp batteries above;
each entry carries its own lane fingerprint. The battery
asked one question 30 ways: *what actually moves a
draw?* — pre-registered items A0–A29 plus fillers F1/F2
from FORTRESS-BACKLOG-2026-11-12.md, scored from the
on-box RESULTS (3,911 records, 18:30 CT hard stop). The
A0 preflight gate passed: 23 models in the store incl.
Qwythos, the serve manifest captured, 3 Trap-60
permutations frozen. The run's **entire error list is 3
lines** — the A25 phi4-mini 404s (F-94). All 31 findings
certified in the 2026-11-12 scoring review; F-numbers
assigned at this export.

| Finding | One-line result |
|---|---|
| [Temp-0.3 replication: PARTIAL](2026-11-12-a1-temp03-replication-partial.md) | B07 and B20 omit in both reps and share one hash — one draw counted twice; the chain's read files the pattern as PARTIAL (F-70) |
| [Determinism anchor: two draws](2026-11-12-a2-determinism-anchor-two-draws.md) | Three reps, two hashes (`b6db…`, `3c06…`, `3c06…`): the identical-hash premise fails as stated; each draw is itself stable (F-71) |
| [KV-prefix state changes the draw](2026-11-12-a3-kv-prefix-changes-draw.md) | Call history selects which draw a call lands on — changes = true; became the soak factor (F-72) |
| [Seed at temp 0](2026-11-12-a4-seed-at-temp0.md) | Seeds 43/1/1234/42 all produce one hash; returning to 42 does not restore the opening draw (F-73) |
| [Reload draw test, 3B](2026-11-12-a5-reload-draw-test-3b.md) | 6 unload/reload cycles: one hash, strict 47, span 0 — reload is not a session variable (F-74) |
| [Load history, 3B](2026-11-12-a6-load-history-3b.md) | Eviction-by-14B history: same hash, same 47, span 0 (F-75) |
| [Co-residency changes the draw](2026-11-12-a7-coresidency-changes-draw.md) | A resident 0.6b beside the 3B moves the session to the second draw — changes = true (F-76) |
| [num_ctx: no effect](2026-11-12-a8-num-ctx-no-effect.md) | 8192 / 16384 / default: one hash throughout (F-77) |
| [Prompt-order permutation](2026-11-12-a9-prompt-order-permutation.md) | 3B baseline misses recur 8/7/8 of 8 (item-intrinsic); 8B's recur 2/2/1 (not) (F-78) |
| [Reload draw test, 8B](2026-11-12-a10-reload-draw-test-8b.md) | 5 cycles at strict 49, span 0 — the 8B's 49 is not reload-borne (F-79) |
| [8B pool control](2026-11-12-a11-8b-pool-control.md) | 24/24 clean on :11435 — the instance is not A1's confound (F-80) |
| [Omission rate, Qwythos B07](2026-11-12-a12-omission-rate-qwythos.md) | 15/30 seeds omit the Source-URL line — a 50% stochastic mode (F-81) |
| [Omission input-specificity](2026-11-12-a13-omission-input-specificity.md) | Bar NOT met: control B01 omits 10/30, so the omission is not B07-specific (F-82) |
| [Fix line at temp 0.3](2026-11-12-a14-fix-line-temp03.md) | 0/30 omissions with the fix line (vs 15/30 without); card-readout structure caveat filed (F-83) |
| [Omission model-specificity](2026-11-12-a15-omission-model-specificity.md) | The 8B omits 0/30 on the same input — the behavior is Qwythos's (F-84) |
| [Reload-block metrology](2026-11-12-a16-reload-block-metrology.md) | Qwythos unmoved across 4 paired blocks (60/57 throughout); the 14B's trap drops 55 → 45 under reload (F-85) |
| [Qwythos cross-session: CONFIRMED](2026-11-12-a17-qwythos-cross-session-confirmed.md) | Plain 60 ×4, trap 57 ×4 — confirmed as **1 effective draw**, decisive test deferred to B4 (F-86) |
| [Qwythos think-on cost](2026-11-12-a18-qwythos-think-on-cost.md) | Gate passes 15/15, then plain 13/60 and trap 0/60 — the record's read: "think cost" (F-87) |
| [Qwythos per-label isolation](2026-11-12-a19-qwythos-per-label-isolation.md) | Of the 3 baseline misses: titles 49 and 11 are item-intrinsic, title 23 is context-induced (F-88) |
| [8B think-on trap collapse](2026-11-12-a20-8b-think-on-trap-collapse.md) | Strict 0/60 in all 3 cycles, every label 0/12 — think-on breaks the trap contract (F-89) |
| [The COMEDY dip is not real](2026-11-12-a21-comedy-dip-not-real.md) | Isolated COMEDY-12: think-off 3/12, think-on 3/12 ×3 — identical; dip_real = false (F-90) |
| [8B think-on plain](2026-11-12-a22-8b-think-on-plain.md) | 60/60 in all 3 cycles, every label 12/12 — think-on's damage is trap-specific (F-91) |
| [14B think-on (diagnostic)](2026-11-12-a23-14b-think-on.md) | Plain 60, trap 58 (above the think-off 55–56) — the 14B does not collapse (F-92) |
| [4B bulk-size ladder](2026-11-12-a24-4b-bulk-size-ladder.md) | Chunk 5: 5/5; chunks of 15: 14/0/15/0; chunks of 30: 0/0 — threshold 5, failure is bulk-induced (F-93) |
| [Fallback spot-check: Gemma + phi void](2026-11-12-a25-fallback-spot-check-gemma-phi.md) | gemma3:4b plain 60 / trap 51 in **both** sessions (bar met); phi4-mini arm **VOID — no data**: 3× HTTP 404, model absent from the :11435 store (F-94) |
| [14B brief pool parity](2026-11-12-a26-14b-brief-pool-parity.md) | 24/24 clean, 0 leaks — indistinguishable from the 8B control (F-95) |
| [Endpoint envelope equivalence](2026-11-12-a27-endpoint-equivalence.md) | /api/generate vs /api/chat: strict 60/60 and hash-equal in both blocks; 0 brief diffs in 6 pairs (F-96) |
| [Instance restart: not a variable](2026-11-12-a28-instance-restart-not-a-variable.md) | Guarded :11435 restart serves the same hash as the reload cycles (F-97) |
| [Device pinning: stable](2026-11-12-a29-device-pinning-stable.md) | Pinned hashes stable, restore verified; the two-draw selection is session history's, not placement's (F-98) |
| [Pool-wide omission rate (F1)](2026-11-12-f1-pool-omission-rate.md) | 14 omissions in 120 cards (11.7%) — concentrated per-input, not uniform (F-99) |
| [Draw-distribution soak (F2)](2026-11-12-f2-draw-distribution-soak.md) | **732 cycles** under KV-prefix cycling: cycle 1 at 52/49, then 731 cycles locked at 3B 47 / 8B 49 (F-100) |

## 2026-11-12 — Mint rulings & certifications (#277 / #278)

Measured on the **Mint** platform (see
`platforms/mint.md`), from the 2026-11-12 sessions and
the main-chat rulings the record reserved to it.

| Finding | One-line result |
|---|---|
| [Independent checker certification: BAR NOT MET](2026-11-12-e263-phi-checker-bar-not-met.md) | phi4-mini echoes the ruler instead of checking: delivery-parse catch 0/18 and 0/24, false-flags an order of magnitude worse under any parse — slot closed, phi stays metadata-only (TUNING #277) |
| [phi4-mini drift certificate: CERTIFIED](2026-11-12-e258-phi4mini-drift-certificate.md) | Every structural axis exact, eval in band; the hook axis filed as a **range (30–36)** on a non-deterministic lane, byte-identity expectation dropped (TUNING #278) |
| [E259-F: SUBSUMED by W8](2026-11-12-e259f-subsumed-by-w8.md) | Closed unrun: its rebalance already is W8's P1 arm on a fresh hash-frozen set at stricter bars; the E259 set is development evidence only (TUNING #278) |

## Not seeded (deliberately)

- **Fortress findings outside the exported batteries** — the pre-build rounds
  (F-01 → F-34) are not exported as standalone findings; the two that
  the R10 certification directly touched appear above (the F-24
  correction, F-36) or are cited inside the R10 entries. Batteries
  R12–R14 have produced no certified findings yet, and R18 is
  unaudited — nothing from them is seeded. R19 appears above as a
  single explicitly INTERIM page with no F-numbers; its findings
  wait for the battery audit. The platform
  page is `platforms/fortress-provisional.md` (filename kept;
  contents now the settled 2026-11-10 fingerprint — the R10–R17
  entries cite the 2026-11-08 fingerprint state recorded on that
  page).
- **PROPOSED-but-unadopted Mint results** (TUNING #238 think-on,
  #239 Mint-scale MoE offload, #241/#242 chunk-budget follow-ons,
  #246 7B VL lane, #247 pin-description contract) — measured and
  ledgered, but adoption reviews are still owed; per the repo's
  rule they are not findings and stay out until adopted.
- **E264 — speculative decoding for block drafting** (TUNING
  #279): **bar MET and PROPOSED, not adopted** — outputs
  byte-identical to the non-speculative control in both
  replicates on the Mint's ik llama-server lane, validator
  compliance exactly equal, wall −25.4% uncached / −30.7%
  cached (mean 1.386×), draft acceptance 70.3%. It resolves
  the #225 exception (speculation certified for exactly one
  shape — block drafting on the server lane; still barred
  for metadata, coverage, classification), but per the
  repo's rule a bar-met proposal is not a finding until the
  adoption review rules. Scope note, as recorded: the
  proposal covers the ik CPU server lane only; production
  drafting runs on the Ollama GPU lane, which E264 neither
  measured nor displaces.
- **The W8 fresh edge set** (TUNING #280) is an instrument
  filing, not a result: the hash-frozen 40-item set that
  unblocks the decisive W8 run is described in
  `evals/README.md`. No W8 result is seeded; its ruling is
  still owed in the working program.
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
