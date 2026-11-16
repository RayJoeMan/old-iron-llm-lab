# Fleet Bus v2 — A/B Results (COMPLETE — all four scored runs executed)

**Design:** `design/DESIGN.md` (pre-registered Nov 14, 2026, before any run). **Independent checks:** `design/OPUS-CHECK.md`, `design/ASTRA-CHECK.md`; adjudication: `design/ADJUDICATION.md` (29 substantive issues; 20 fixed in code before any run, 7 carried as disclosed amendments A-1…A-5). **Build/run record:** `results/RUN-LEDGER.md`. **Metrics:** `results/metrics/` (per-run metrics JSON + call logs for all four scored runs, gate-results2.json).

**History:** this file was first filed Nov 14, 2026 as a PARTIAL record (one valid run; the C2 runs deferred by a measured environment failure). On Joe's Nov 14 ~18:17 CT directive ("Finish out the testing on swarmbus v2"), the three deferred runs were executed the same evening under the filed window protocol (§4 of the partial filing). The Nov 14 partial record is preserved in §8. Two later rulings from Joe apply to this completion: the **metric addendum** (Nov 14, 20:57 CT — headline efficiency metric is *tokens per error-free job*, per task class; raw tok/s is a diagnostic footnote) and the **expanded mandate** (Nov 14, 20:51 CT — the program continues as an iterate-until-working loop; v3 follows from this analysis in its own folder).

## Verdict, up front

**NO WIN. The v2 win bar fails on one leg of eight: wall.** C2 aggregate wall 5,467.0 s vs the filed cap of 1.25 × Arm B's 3,673.1 s = 4,591.4 s (measured ratio **1.488×**). Every other leg passes, several decisively: **zero lost, zero duplicated, 36/36 accounted, shipped-wrong 0 vs B's 7**, coordination tokens exactly 0, interventions 0 ≤ 0, mechanics gate PASS. Under the filed rules a split result is a fail, so **Fleet Bus v2 is not adoption-justified as measured** — the gate delivers exactly the correctness it promised, at a wall (and token) price above the filed price of the gate.

On Joe's headline metric, **tokens per error-free job** (all tokens — prompt processing + generation, all attempts — ÷ jobs verified correct): **B 1,337.5 vs C2 1,645.2** in aggregate. C2 spends 40% more tokens overall (54,292 vs 38,787) and, because its three dead-lettered VERIFY tasks burned 11,538 tokens for zero clean jobs, it is *more* expensive per clean job than the incumbent despite shipping nothing wrong. Per class the picture splits: C2 is **cheaper** per clean DRAFT job (1,840.3 vs 2,047.4 — B wastes its DRAFT spend on wrong deliveries) and **more expensive** on CLASSIFY (869.3 vs 591.8) and VERIFY (2,419.6 vs 1,700.8). Full tables in §5.

Adoption remains Joe's ruling. Per the expanded mandate, this analysis is the design input to v3 (`~/workspace/your_files/fleet-bus-v3-2026-11-14/`), which attacks the two measured cost centers: the 1,600-token leak-burn multiplier on short-answer task classes, and the full-price four-attempt burn on persistently-misjudged VERIFY tasks.

## 1. Run inventory

| Run | Status | Wall (s) | Done | DLQ | Lost | Dup | Shipped-wrong |
|---|---|---|---|---|---|---|---|
| B run 1 (Nov 14 AM) | Complete + valid | 1,746.5 | 18 | — | 0 | 0 | **4** (d4, d5, d6, v1) |
| C2 run 1 attempts 1–3 (Nov 14) | Aborted/deferred pre-score (environment, §8) | — | — | — | — | — | — |
| C2 run 1 (Nov 14 eve, attempt 4) | **Complete + valid** | 2,358.1 | 17 | 1 (v6) | 0 | 0 | **0** |
| C2 run 2 (Nov 14 eve) | **Complete + valid** | 3,108.9 | 16 | 2 (v1, v6) | 0 | 0 | **0** |
| B run 2 (Nov 14 eve) | **Complete + valid** | 1,926.6 | 18 | — | 0 | 0 | **3** (d1, v1, v6) |

Run order as filed (counterbalanced): run 1 = B then C2; run 2 = C2 then B. All attempts preserved on-box under `~/fleet-bus-ab2/runs/` (`.bak-*` dirs for the Nov 14 unscored attempts). Full narrative with timestamps: RUN-LEDGER.md.

## 2. Per-run results

### 2.1 Arm B run 1 (control) — Nov 14 AM

18/18 done, 0 lost, 0 duplicated. Wall 1,746.5 s. Work 20,980 tokens (prompt+eval) / 18 logged calls, failed_calls 0, coordination tokens 0. Kill test: worker b1 SIGKILLed holding v2 → recovered, latency **300.1 s**, no duplication. First-attempt validator pass 14/18 (collection re-score). **Shipped-wrong 4: d4, d5, d6, v1.** Calibration qwen3:4b 10.21 tok/s (GPU-resident runner, 7.2 GB VRAM). Conditions: pre-load l1 4.49; load trace heated l1 26→55 (lane-b tranche + Gemma trial) — a contention wall, reported as such. The killed in-flight v2 generation never reached the call log (adjudication #16's uncountable case, live): real generations 19, logged 18. Budget-burned calls 6 (call-level context, amendment A-1).

### 2.2 Arm C2 run 1 — Nov 14 evening (attempt 4; the scored run)

Launched 18:28:49 CT under the filed window: pre-load l1 8.20, DRAFT probe **131.6 s** (< 240), qwen3:4b fully GPU-resident (size_vram 7,220,326,563). Tenancy at launch: tranche-b-chain + tranche-b-lane41 active (the run's load trace records the consequence: l1 min 18.6 / mean 41.4 / max 62.6 — Tranche B CPU blocks surged mid-run; the endpoint never wedged: **failed_calls 0 across all 24 calls**, the decisive difference from the morning's attempts).

- **17 done + 1 deadletter (v6) = 18/18 accounted. Lost 0, duplicated 0, shipped-wrong 0.**
- Wall **2,358.1 s**. Work **24,110 tokens / 24 calls** (21 × qwen3:4b, 3 × qwen3:8b), coordination tokens **0**, coordination calls 0.
- First-attempt validator pass **15/18**. Validator failures recovered by the ladder: d4 (passed attempt 3, rung 2) and d1 (passed attempt 2).
- **Kill test:** worker c2 SIGKILLed holding v2 after the 6th completion → **recovered, latency 478.4 s**, no duplication (v2's killed in-flight generation is unlogged/uncountable per the filed accounting; its successful retry logged 1 call).
- DLQ: v6 — 4 attempts (4b: WRONG_VERDICT_1, UNPARSEABLE-leak; 8b: WRONG_VERDICT_3 ×2), priced at **3,834 tokens** (§6).
- Leak-flagged attempts (§4.2 definition): d4 a2, v6 a2 (both qwen3:4b).
- Mirror (SwarmChat durable log): **116/116 events posted, 0 errors**, channel `fleet-bus-v2-c2-run1`.
- Calibration: qwen3:8b 2.14 tok/s (96 eval, cold), qwen3:4b 10.89 tok/s.

### 2.3 Arm C2 run 2 — Nov 14 evening

Launched 19:18:47 CT: pre-load l1 8.13, DRAFT probe **133.4 s**, 4b fully GPU-resident (7,220,326,563 B VRAM); 8b partially resident at launch (1.77 GB VRAM). Load trace l1 mean 39.1 / max 43.6 (Tranche B tenancy again; endpoint healthy throughout, failed_calls 0).

- **16 done + 2 deadlettered (v1, v6) = 18/18 accounted. Lost 0, duplicated 0, shipped-wrong 0.**
- Wall **3,108.9 s**. Work **30,182 tokens / 27 calls**, coordination tokens **0**.
- First-attempt validator pass **13/18**. Ladder recoveries: d6, d2, c3 passed on attempt 2.
- DLQ: v1 — 4 attempts, **WRONG_VERDICT_3 on all four** across both models (the persistent-misjudgment pattern from v1, now priced and parked instead of lost or shipped), 3,870 tokens; v6 — 4 attempts (UNPARSEABLE, WRONG_VERDICT_1+2, WRONG_VERDICT_3 ×2), 3,834 tokens. DLQ total **7,704 tokens** (§6).
- Leak-flagged attempts: v6 a1, d2 a1 (both qwen3:4b).
- Mirror: **126/126 events, 0 errors**, channel `fleet-bus-v2-c2-run2`.
- Calibration: qwen3:8b 2.84 tok/s, qwen3:4b 12.77 tok/s.

### 2.4 Arm B run 2 (control) — Nov 14 evening

Launched 20:53:44 CT, after Joe parked the Tranche B lanes (20:47 CT) and Fortress became exclusive to this program: pre-load l1 6.48, DRAFT probe **194.6 s**. Runner condition, recorded as filed: qwen3:4b mostly CPU-resident (1.26 GB VRAM — the placement the production service chose under the day's VRAM pressure; not altered by the coordinator). Calibration qwen3:4b **8.22 tok/s**. Load trace l1 mean 20.2 / max 20.8 — the run's own CPU-side generation work on an otherwise exclusive box.

- **18/18 done, 0 lost, 0 duplicated.** Wall **1,926.6 s**. Work **17,807 tokens / 18 calls**, failed_calls 0, coordination tokens 0.
- First-attempt validator pass 15/18 (collection re-score). **Shipped-wrong 3: d1, v1, v6** — the incumbent again delivered validator-failing artifacts as completed work, including both VERIFY tasks that C2's gate refused in its run 2.
- Budget-burned calls 3 (call-level context, amendment A-1). No kill test (run 1 of the arm carried it, per §7 of the design).

## 3. Win-bar scorecard (design §9 — all legs on the aggregate of 2 runs / 36 tasks per arm)

| # | Leg (as filed) | Measured | Verdict |
|---|---|---|---|
| 1 | **Hard gate:** C2 lost = 0 and duplicated = 0, each run | Run 1: lost 0, dup 0 · Run 2: lost 0, dup 0 | **PASS** |
| 2 | **Accounted:** C2 = 18/18 each run; C2 aggregate ≥ B aggregate | C2 18/18 + 18/18 = 36 · B 36 | **PASS** |
| 3 | **Shipped-wrong:** C2 aggregate < B aggregate | C2 **0** · B **7** (4 + 3) | **PASS** |
| 4 | **DLQ cap:** C2 aggregate ≤ 4/36 and ≤ 3/run | Aggregate **3** (v6 ×2, v1 ×1) · runs 1, 2 | **PASS** |
| 5 | **Wall:** C2 aggregate ≤ 1.25 × B aggregate | C2 5,467.0 s · cap 1.25 × 3,673.1 = 4,591.4 s · ratio **1.488×** | **FAIL** |
| 6 | **Coordination tokens:** C2 = 0 exactly | 0 (0 coordination calls in both runs; mirror is transport, 242/242 events, 0 generations) | **PASS** |
| 7 | **Interventions:** C2 ≤ B | C2 0 · B 0 (in-run, scored runs; the Nov 14 attempt aborts were coordinator actions on unscored attempts under the filed defer/abort protocol, ledgered in RUN-LEDGER.md) | **PASS** |
| 8 | **Mechanics gate** passes in full before numbers count | PASS — 5/5 legs incl. the v2 policy-ladder leg (§8.1) | **PASS** |

**Result: 7 of 8 legs pass; leg 5 fails → split → the bar FAILS, exactly as filed.** Fleet Bus v2 is not adoption-justified on this evidence. The failure is narrow and priced: the correctness the gate buys (legs 1–4, 6) costs 1.488× the wall against a filed price of 1.25×.

## 4. The gate's value, on the record (counterfactual, design §3.3)

Of Arm B's 7 shipped-wrong task-instances, C2's handling of the same task IDs in the paired run: **actively caught 3** (run 1: d4 failed attempt 1, passed on the ladder; run 2: v1 and v6 deadlettered rather than shipped) and **4 were right on C2's first attempt** (d5, d6, v1 in run 1; d1 in run 2 — first attempts are identical in construction across arms but are separate draws, so these four are reported as "not wrong in C2" rather than gate catches). No task that B shipped wrong was shipped wrong by C2 in either run. The v1 A/B's central pathology — the bus losing tasks it correctly refused (5 lost) while the queue shipped the same wrong answers — is gone: refusal now terminates in a priced dead-letter (3) or a corrected delivery (the ladder recovered 5 first-attempt failures across the two runs), never in a loss and never in a silent wrong shipment.

## 5. Headline metric — tokens per error-free job (Joe's addendum, Nov 14 20:57 CT)

Definition as ruled: total tokens consumed — prompt processing (`prompt_eval_count`) + generation (`eval_count`), across **all** attempts including retries and escalations — divided by jobs **verified correct** (delivered artifact passes the shared validator at collection). Checker passes in this harness are deterministic code (0 generations, 0 tokens). Killed in-flight generations are unlogged and uncountable (filed accounting, both arms). Per task class, from the call logs joined to the collection re-scores; B's per-class split uses the prompt-length attribution validated in §7 (exact at class level; totals cross-check to the metrics files to the token).

### 5.1 Per run

| Run | CLASSIFY | DRAFT | VERIFY | All classes |
|---|---|---|---|---|
| B run 1 | 4,182 tok / 6 correct = **697.0** | 8,916 / 3 = **2,972.0** | 7,882 / 5 = **1,576.4** | 20,980 / 14 = **1,498.6** |
| B run 2 | 2,919 / 6 = **486.5** | 7,463 / 5 = **1,492.6** | 7,425 / 4 = **1,856.2** | 17,807 / 15 = **1,187.1** |
| C2 run 1 | 3,633 / 6 = **605.5** | 10,981 / 6 = **1,830.2** | 9,496 / 5 = **1,899.2** | 24,110 / 17 = **1,418.2** |
| C2 run 2 | 6,799 / 6 = **1,133.2** | 11,103 / 6 = **1,850.5** | 12,280 / 4 = **3,070.0** | 30,182 / 16 = **1,886.4** |

### 5.2 Aggregate (36 tasks per arm)

| Class | B tokens / correct | B tok per clean job | C2 tokens / correct | C2 tok per clean job | Cheaper |
|---|---|---|---|---|---|
| CLASSIFY | 7,101 / 12 | **591.8** | 10,432 / 12 | **869.3** | B |
| DRAFT | 16,379 / 8 | **2,047.4** | 22,084 / 12 | **1,840.3** | **C2** |
| VERIFY | 15,307 / 9 | **1,700.8** | 21,776 / 9 | **2,419.6** | B |
| **All** | 38,787 / 29 | **1,337.5** | 54,292 / 33 | **1,645.2** | B |

Reading: the gate pays for itself exactly where wrong answers are expensive to produce (DRAFT — B burns full-length generations on drafts it then ships wrong; C2's retries convert that waste into clean jobs). It overpays where the cheap model is already reliable (CLASSIFY — C2's retries there are pure overhead: 12/12 correct in both arms, C2 spending 47% more tokens to get them) and where the failure is a persistent misjudgment no regeneration fixes (VERIFY — C2's DLQ tasks consumed 11,538 tokens for zero clean jobs, while B "spends" one attempt and ships the wrong answer; B's VERIFY number is lower only because its wrong jobs are excluded from the denominator while their single-attempt cost stays in the numerator — the metric prices the bus's honesty, which is the point of reporting it alongside shipped-wrong, never instead of it).

*Diagnostic footnote (not the headline): calibration tok/s — B run 1: 4b 10.21 · C2 run 1: 4b 10.89, 8b 2.14 · C2 run 2: 4b 12.77, 8b 2.84 · B run 2: 4b 8.22 (CPU-heavy runner).*

## 6. DLQ pricing (design §3.2 — every dead-letter, priced)

| Run | Task | Kind | Attempts (model: validator reasons) | Tokens (prompt+eval) | Calls |
|---|---|---|---|---|---|
| C2 run 1 | v6 | VERIFY | 4b: WRONG_VERDICT_1 · 4b: UNPARSEABLE (leak-flagged) · 8b: WRONG_VERDICT_3 · 8b: WRONG_VERDICT_3 | **3,834** | 4 |
| C2 run 2 | v1 | VERIFY | 4b: WRONG_VERDICT_3 · 4b: WRONG_VERDICT_3 · 8b: WRONG_VERDICT_3 · 8b: WRONG_VERDICT_3 | **3,870** | 4 |
| C2 run 2 | v6 | VERIFY | 4b: UNPARSEABLE (leak-flagged) · 4b: WRONG_VERDICT_1+2 · 8b: WRONG_VERDICT_3 · 8b: WRONG_VERDICT_3 | **3,834** | 4 |

Aggregate DLQ price: **11,538 tokens / 12 calls for 3 tasks** — 21.3% of C2's total token spend produced no clean job. Two structural facts: (1) all three dead-letters are VERIFY tasks whose verdicts the models get *persistently* wrong — v1's claim-3 verdict was wrong on all four attempts across both models; regeneration with an identical prompt does not move it. (2) v6's price is identical in both runs (3,834) — same ladder path, same leak-burn pattern, near-deterministic at temp 0.3. DLQ records (full attempt history + artifact paths) are in each run's `deadletter/` dir on-box and joined into the metrics files (`deadletter_records`, `dlq_tokens`).

## 7. Per-task token tables (prompt+eval totals, all attempts; from call logs)

Arm B logs carry no task field (arm_b.py unmodified, amendment A-1); B's per-task values are attributed by matching call timestamps to `results/` file mtimes with prompt-length validation — all 36 B calls attributed, 0 mismatches, totals equal the metrics files exactly (20,980 / 17,807). Class-level values are exact regardless; the only per-task caveat is the c2/c4 and d1/d5 prompt-length pairs (same class), resolved by write order.

| Task | Kind | B run 1 | B run 2 | C2 run 1 (calls) | C2 run 2 (calls) |
|---|---|---|---|---|---|
| c1 | CLASSIFY | 396 | 307 | 391 (1) | 396 (1) |
| c2 | CLASSIFY | 1,492 | 504 | 424 (1) | 547 (1) |
| c3 | CLASSIFY | 852 | 608 | 679 (1) | 2,990 (2) |
| c4 | CLASSIFY | 407 | 529 | 430 (1) | 1,196 (1) |
| c5 | CLASSIFY | 478 | 624 | 1,313 (1) | 1,191 (1) |
| c6 | CLASSIFY | 557 | 347 | 396 (1) | 479 (1) |
| d1 | DRAFT | 991 | 1,771 | 2,627 (2) | 1,325 (1) |
| d2 | DRAFT | 1,771 | 1,061 | 985 (1) | 3,049 (2) |
| d3 | DRAFT | 867 | 1,101 | 1,457 (1) | 924 (1) |
| d4 | DRAFT | 1,781 | 1,152 | 3,878 (3) | 1,781 (1) |
| d5 | DRAFT | 1,757 | 1,059 | 1,143 (1) | 1,463 (1) |
| d6 | DRAFT | 1,749 | 1,319 | 891 (1) | 2,561 (2) |
| v1 | VERIFY | 1,757 | 1,757 | 1,564 (1) | **3,870 (4) → DLQ** |
| v2 | VERIFY | 961 | 780 | 894 (1) | 744 (1) |
| v3 | VERIFY | 776 | 915 | 805 (1) | 1,061 (1) |
| v4 | VERIFY | 1,372 | 1,173 | 1,531 (1) | 1,732 (1) |
| v5 | VERIFY | 1,268 | 1,052 | 868 (1) | 1,039 (1) |
| v6 | VERIFY | 1,748 | 1,748 | **3,834 (4) → DLQ** | **3,834 (4) → DLQ** |

## 8. The Nov 14 partial record (preserved)

### 8.1 Mechanics gate — PASS (before any scored run, on the post-check-fix code)

`gate_c2.py` on Fortress, `gate_pass: true` (metrics/gate-results2.json): (1) flood 1,000 tasks — 1,000 done, 0 duplicate claim attempts, 1,000 merges, 15.7 s; (2) duplicate-enqueue storm — exactly 18 tasks; (3) SIGKILL reaper + worker mid-flood — 100 done, 0 deadletters, 0 duplicate merges, 1 reap exercised; (4) reconciliation — JSONL replay == ledger on the flood DB and the policy DB; (5) **policy ladder (new in v2)** — 6 always-fail tasks × exactly 4 attempts = 24 result rows, 18 FAIL_REQUEUE, 6 DEADLETTER. The ledger core is byte-identical to v1 except the filed 7-line `dead`→`deadletter` transformation (diff in RUN-LEDGER.md).

### 8.2 The morning's environment failure — measured, not anecdotal

C2 run 1 attempts 1–3 (Nov 14 AM) were deferred/aborted under the filed protocol: the production qwen3:4b runner was mostly CPU-resident (1.26 GB VRAM vs 7.2 GB healthy) under Gemma-trial + lane-b tenancy at load 45–58; the 4b calibration generation timed out at 600 s twice; attempt 3's first scored call timed out at 600 s with the zombie-generation cascade forming (each client timeout leaves a server-side generation that slows the queue behind it). A decisive probe after a full GPU-resident reload still timed out at 600.1 s under that tenancy. The evening's scored runs differ in exactly the measured respects: launch probes 131.6/133.4/194.6 s (all < 240), runner GPU-resident for both C2 launches, and — after Joe parked Tranche B — an exclusive box for B run 2. Zero failed calls in all four scored runs (69 logged calls).

### 8.3 SwarmChat as durable log

Across every live start (Nov 14 attempts included): mirror posted 45/45 events in the aborted attempts and **116/116 + 126/126** in the scored C2 runs — 0 errors, 0 generations, 0 arbitration, on the Python-3.12-pinned server. The durable-log role is validated end-to-end; it is not a bar leg (design §5).

## 9. Analysis — what worked, what didn't (the v3 design input)

**Worked, with evidence:**
- *The ledger core, again.* 0 lost, 0 duplicated across 36 C2 tasks including a mid-run SIGKILL (recovery 478.4 s) — v1's mechanics result replicated under the v2 policy layer, and the mechanics gate's new leg 5 proves the ladder/DLQ path itself.
- *The gate as a correctness device.* Shipped-wrong 7 → 0. Five first-attempt failures were converted to clean deliveries by the ladder; three persistent failures were parked in the DLQ with full histories instead of being lost (v1) or shipped (B).
- *Zero-coordination arbitration.* 0 coordination tokens, 0 coordination calls; the mirror moved 242 events as pure transport.
- *The DLQ as an accounting surface.* Every refusal is priced (§6) — the failure modes below are visible *because* the DLQ records exist.

**Didn't work, with evidence:**
- *Wall price of the gate: 1.488× vs the filed 1.25×.* The ladder's extra generations (51 C2 calls vs B's 36) are executed serially against one shared runner per model; every retry is a full-price, full-latency regeneration. Under the evening's tenancy (load traces mean l1 39–41 for the C2 runs vs B run 2's exclusive-box 20.2), C2's walls absorbed both the retry count and the contention.
- *The 1,600-token budget on short-answer classes.* VERIFY's passing artifacts are 3-line verdicts and CLASSIFY's are labels, yet every attempt carries a 1,600-token ceiling that the 4b's think-leak burns to the cap: leak-flagged attempts and budget-burned calls cluster exactly there (v6's two 4b attempts: 1,600 + 1,600 eval tokens in both runs). The budget converts a wrong short answer into the most expensive call in the run.
- *Identical-prompt regeneration against a persistent misjudgment.* v1 (VERIFY) failed WRONG_VERDICT_3 on 4/4 attempts across two models; v6 failed on 8/8 attempts across two runs. Attempts 3–4 bought nothing measurable in these cases — the failure is in the model's reading of the claim, and an identical prompt re-asks the identical question.
- *Escalation asymmetry in VERIFY.* The 8b's VERIFY attempts are nearly free in tokens (15 eval tokens on v6's rungs) but were reached only after two full-price 4b burns; the ladder spends its money in the wrong order for this class.

**Failure-mode summary:** lost tasks — none, either arm, any run (B's discipline also lost none; v1's bus losses are not reproduced because deadletter replaced dead). Shipped-wrong — B 7/36 (19.4%), C2 0/36. DLQ behavior — 3/36, all VERIFY, all persistent-verdict failures, priced at 11,538 tokens. Latency — walls above; kill recovery B 300.1 s vs C2 478.4 s (both recovered, no duplication; C2's includes lease expiry + requeue + regeneration under load 40+).

## 10. Recommendation (v2, as filed) and the road from here

Under the filed bar, the recommendation follows v1's form: **the file-queue discipline stays the incumbent; Fleet Bus v2 is filed as tested-and-split (7/8 legs, wall failing)** — with the material difference that v2's split is a *price* failure, not a *correctness* failure: the bus system demonstrably delivers nothing-lost, nothing-duplicated, nothing-wrong at 1.49× wall and 1.23× tokens-per-clean-job. Whether that trade is worth it in production is Joe's ruling, and under his Nov 14 20:51 CT expanded mandate the question is now being put to a v3 that attacks the measured price directly (per-kind generation budgets; verdict-feedback or early-deadletter policy for persistent VERIFY failures; class-aware rung order), checked independently by both frontier seats before build, and tested by this same route. SwarmChat's role is unchanged by every measurement so far: durable log, never arbiter.

## 11. Disclosed asymmetries (carried from ADJUDICATION.md, amendments A-1…A-5)

- B's per-attempt leak metric is call-level context only (`budget_burned_calls`: run 1 = 6, run 2 = 3); C2's is per-attempt (leak-flagged lists in §2). Never compared head-to-head.
- Lease expiry is reaper-mediated in both bus versions (v1 semantics retained).
- "First attempt" = first validated/delivered artifact (v1-comparable naming).
- B delivery fencing undercounts B duplication (pro-B bias); transport errors consume C2 attempts but not B's (anti-C2 under infrastructure failure — the Nov 14 morning's attempts are the documented case; the scored evening runs had zero transport errors); shipped-wrong is validator-relative and symmetric across arms.
- Token counts are prompt+eval sums from Ollama's own counters (`workgen2` logs both); the metrics files' `work_tokens`/`per_task_tokens` are those sums. Killed in-flight generations are unlogged in both arms (B run 1: 19 real vs 18 logged; C2 run 1: 25 real vs 24 logged).
- Conditions asymmetry, stated plainly: the C2 runs ran under Tranche B tenancy (load-trace means 41.4 / 39.1); B run 1 ran under heating tenancy (26→55); B run 2 ran on an exclusive box (mean 20.2, mostly the run's own work) with a CPU-heavy 4b runner (calibration 8.22 vs 10.21–12.77 tok/s in the other runs). Walls are reported as measured under these filed traces, per the design — no wall in this file is a clean-box number.
- Arm A (SwarmChat arbitration) did not re-run: v1 settled the structural question (79,601 coordination tokens ≈ 2.5× the work; both runs hit the 60-min cap).
