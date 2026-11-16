# Fleet Bus v3 A/B — RESULTS

**Test executed:** Nov 14–15, 2026, on Fortress (exclusive to this program; Tranche B parked throughout). **Design:** `../design/DESIGN.md` as amended pre-build by `../design/ADJUDICATION.md` (dual frontier checks: Claude Opus 5.5 + GPT-6 Astra, both "do not build as filed"; amendments A1–A16 applied before the build). **Method:** `analysis.py` in this folder, computed from the six runs' metrics/call logs/verdicts in `metrics/`; run-by-run record in `RUN-LEDGER.md`.

## 1. Verdict

**Fleet Bus v3 (Arm C3) CLEARS THE PRE-FILED WIN BAR — 8 of 8 legs** against the fresh Arm B aggregate, and **meets the improvement yardstick on all five conditions** against the same-regime C2 reference. Under the loop's filed rules this is a **win**: v3 is the working program, subject to the A10 fresh-workload confirmation (§10) before the adoption packet is finalized. Adoption remains Joe's ruling.

The one-line story: v2 proved the bus's correctness and failed on price (wall 1.488×, 1,645.2 tok/error-free job). V3 changed only the policy layer's economics — alternating class-aware ladders plus a cross-model early dead-letter — and the price failure inverted: **C3 is faster than the incumbent (wall ratio 0.617×), cheaper per clean job than both incumbents (942.3 tok/efj vs B's 1,512.2 and C2ref's 1,693.1), and keeps the correctness guarantee intact (0 lost, 0 duplicated, 0 shipped-wrong, 32/36 correct with the other 4 surfaced as priced dead-letters).**

## 2. Run inventory (all scored; no exclusions, no relaunches, no interventions)

| Run | Wall (s) | Done | DLQ | Lost | Shipped-wrong | Tokens | Calls | Correct | tok/efj |
|---|---|---|---|---|---|---|---|---|---|
| B run 1 (kill) | 2,226.6 | 18 | — | 0 | 4 (c3, d2, v1, v6) | 20,022 | 18 | 14 | 1,430.1 |
| B run 2 | 2,466.8 | 18 | — | 0 | 4 (d1, d6, v1, v6) | 22,321 | 18 | 14 | 1,594.4 |
| C2 ref run 1 (kill) | 2,628.9 | 16 | 2 (v1, v6) | 0 | 0 | 24,623 | 26 | 16 | 1,538.9 |
| C2 ref run 2 | 3,163.5 | 16 | 2 (v1, v6) | 0 | 0 | 29,557 | 28 | 16 | 1,847.3 |
| **C3 run 1 (kill)** | **1,313.5** | 16 | 2 (v1*, v6) | 0 | 0 | 14,119 | 24 | 16 | **882.4** |
| **C3 run 2** | **1,583.8** | 16 | 2 (v1*, v6) | 0 | 0 | 16,035 | 24 | 16 | **1,002.2** |

*v1 deadlettered **early** (attempt 2) in both C3 runs — §7. Aggregates: **B** wall 4,693.4 · tokens 42,343 · correct 28 · shipped-wrong 8. **C2ref** wall 5,792.4 · tokens 54,180 · correct 32 · DLQ 4. **C3** wall 2,897.3 · tokens 30,154 · correct 32 · DLQ 4. Failed generation calls: **0 in all six runs** (178 logged calls). Coordination-generation tokens: **0** in every bus run. Mirror: 116/116, 124/124, 114/114, 130/130 events posted, 0 errors (four bus runs). Every launch met the filed fairness gate (load < 30 + dual probe < 240 s each; measurements in the run ledger). Load traces (exclusive box, the runs' own work): l1 means 20.1–21.0 across runs.

## 3. Win-bar scorecard (v2 §9 verbatim, C3 vs fresh B aggregate)

| # | Leg (as filed) | C3 | B | Result |
|---|---|---|---|---|
| 1 | Hard gate: lost = 0 and duplicated = 0, each run | 0 / 0 both runs | — | **PASS** |
| 2 | Accounted 18/18 each run; aggregate ≥ B | 36 | 36 | **PASS** |
| 3 | Shipped-wrong < B | **0** | 8 | **PASS** |
| 4 | DLQ ≤ 4 aggregate, ≤ 3 per run | 4 (2 + 2) | — | **PASS** (at the aggregate cap — see §9) |
| 5 | Wall ≤ 1.25 × B | 2,897.3 (ratio **0.617**) | 4,693.4 | **PASS** |
| 6 | Coordination tokens = 0 | 0 | — | **PASS** |
| 7 | Interventions ≤ B | 0 | 0 | **PASS** |
| 8 | Mechanics gate passes in full | 10/10 legs | — | **PASS** |

**8/8. The bar is cleared.** (Error-free jobs per arm, per A12/m6 disclosure: B 28, C2ref 32, C3 32 of 36.)

## 4. Improvement yardstick (as amended by A4/A5 — C3 vs the same-regime C2 reference)

| Condition | Requirement | Measured | Result |
|---|---|---|---|
| (i) No bar leg lost vs v2's pass set | legs 1,2,3,4,6,7,8 hold | all hold (and leg 5 gained) | **PASS** |
| (ii) tok/efj < C2ref by ≥ 3% | < 1,642.3 | **942.3** (−44.3%) | **PASS** |
| (iii) Wall ratio < C2ref's by ≥ 0.05 | < 1.184 | **0.617** (C2ref 1.234) | **PASS** |
| (iv) Correct ≥ C2ref and shipped-wrong = 0 | ≥ 32, = 0 | 32, 0 | **PASS** |
| (v) Class floors (within 1 of C2ref per class) | CL ≥ 11, DR ≥ 11, VE ≥ 7 | CL 12, DR 12, VE 8 — **identical to C2ref in every class** | **PASS** |

Historical context (different regime, not the yardstick): v2's filed C2 aggregate was wall 5,467.0 / tok/efj 1,645.2 / correct 33. The same-regime C2 reference measured wall 5,792.4 / 1,693.1 / 32 — the reference runs were *slower* than v2's originals despite the exclusive box, because the dominant regime variable in this test was the 4b runner's CPU-heavy placement (calibration 8.1–8.4 tok/s in all six runs vs 10.9–12.8 GPU-resident in v2's evening runs). Opus's M7 worry — that an exclusive-regime C2 might beat the yardstick "for free" — is answered by measurement: it did not; C3's margin over C2ref is a mechanism effect, not a regime effect.

## 5. Headline metric — tokens per error-free job, per class (Joe's Nov 14 addendum)

| Class | B (tokens / correct / efj) | C2ref | C3 |
|---|---|---|---|
| CLASSIFY | 10,122 / 11 / 920.2 | 10,337 / 12 / 861.4 | **1,516 / 12 / 126.3** |
| DRAFT | 16,294 / 9 / 1,810.4 | 20,923 / 12 / 1,743.6 | **15,878 / 12 / 1,323.2** |
| VERIFY | 15,927 / 8 / 1,990.9 | 22,920 / 8 / 2,865.0 | **12,760 / 8 / 1,595.0** |
| **ALL** | 42,343 / 28 / **1,512.2** | 54,180 / 32 / **1,693.1** | 30,154 / 32 / **942.3** |

Per-run values are in §2's table. Compute companion (Astra #15/Opus M9 disclosure — tokens are not compute): wall per error-free job is B 167.6 s, C2ref 181.0 s, C3 **90.5 s**; C3's tokens split 4b 25,717 / 8b 4,437 across 48 calls, so the token win is not a model-swap artifact — the 8b's share of C3's spend is small *because* its answers are short, which is the mechanism working, and the wall companion moves the same direction.

**CLASSIFY is the headline inside the headline.** On the routed ladder a CLASSIFY task costs ~80–90 tokens (one 15-eval-token 8b answer plus prompt) against ~400–3,400 on the 4b-first paths — a 6.8× per-job improvement at **identical yield (12/12 in both bus arms)**. The A13 exploratory label is retired by measurement: the 8b's CLASSIFY accuracy on the full class was 11/12 at attempt 1 (the 12th passed at attempt 2 on the 4b), with zero CLASSIFY dead-letters and zero shipped-wrong — **no routing regression** under the pre-registered definition.

## 6. Attribution — what bought what (A6 counterfactual)

Pre-registered decomposition from C3's own logs: apply B's policy (first generation ships, unvalidated) to C3's routed first attempts ("C3-attempt-1-shipped"): **17,924 tokens, 28 correct, 8 shipped-wrong, tok/efj 640.1** (per run: run 1 — 8,127 tokens, wrong {d2, d5, v1, v6}; run 2 — 9,797 tokens, wrong {c5, d2, v1, v6}).

- **Routing vs B** (42,343 → 17,924 tokens): the class-aware ladders are the entire *efficiency* story — and buy **zero correctness** (28 correct, 8 wrong, identical counts to B).
- **Gate + ladder + DLQ vs routing alone** (17,924 → 30,154 tokens): the bus machinery spends +12,230 tokens to convert all 8 would-be-wrong shipments into **4 additional correct jobs (32) and 4 surfaced, priced dead-letters**, shipping nothing wrong.
- **Net:** the system lands at 942.3 tok/efj — better than B (1,512.2) *and* correct where B is not. Neither half wins alone: routing without the gate ships 8/36 wrong; the gate without routing (C2ref) costs 1,693.1 per clean job and 1.234× the incumbent's wall.

## 7. The two mechanisms, measured

**Alternating ladders.** VERIFY attempt 1 on the 8b: **8/12 passed** — the first measurement of the 8b's VERIFY accuracy on the full class (v2's ladder only ever showed it failures). The 4b's attempt-1 VERIFY rate in C2ref was 8/11 recorded (one attempt consumed by the kill). Per Opus M1's "leak-as-reasoning" hypothesis: not supported on this workload — the 8b's 15-token verdicts matched the leaky 4b's accuracy at ~1/100th the eval tokens. CLASSIFY attempt 1 on the 8b: 11/12. DRAFT's earlier escalation also paid: C3's attempt-2 (8b) DRAFT verdicts went **4/4**, against C2ref's attempt-2 (4b) 3/4. Full rung table in `analysis.py` output (filed with the run evidence).

**Early dead-letter.** Fired **twice, both correctly**: v1 in both C3 runs, at attempt 2, on the cross-model identical pair {WRONG_VERDICT_3} (8b then 4b) — the exact signature the rule was filed for. It never fired on any task that later passed, in any run (the A1 safety property held in production conditions, not just in the gate). Price effect: v1 cost **1,935 tokens in both C3 runs** vs 2,113 / 3,870 in C2ref and 3,834×2 in v2 — the saving is real but modest; the larger VERIFY win came from routing (attempt 1 at 15 eval tokens instead of a 1,600-token leak burn). v6 never triggers the rule — its failure sets keep varying ({UNPARSEABLE} → mixed verdict sets → {WRONG_VERDICT_3} pairs only at the final rungs) — and costs the full 3,834 in every bus run of both versions. The rule is a scalpel for one failure shape, priced honestly: DLQ totals were C3 11,538 (5,769 × 2) vs C2ref 13,651.

**Kill tests (A12 reporting).** Run 1 of each arm: B — b2 killed holding v1, recovered 634.2 s (file-queue stale-claim path); C2ref — c3 killed holding v1, recovered 770.8 s (kill→terminal includes v1's full ladder climb to DLQ); C3 — c2 killed holding d1, recovered **214.2 s**. Kill-adjusted walls (recovery excised): B1 1,592.4 · C2ref1 1,858.1 · C31 1,099.3 — the ordering is unchanged; the bar's leg 5 does not depend on the kill.

## 8. Per-task token tables (all six runs)

From `analysis.py` (B attributed by call-ts ↔ result-mtime zip, prompt-length validated 36/36, totals exact; bus arms from the tagged logs):

| Task | B1 | B2 | C2ref1 | C2ref2 | C31 | C32 |
|---|---|---|---|---|---|---|
| c1 | 411 | 373 | 384 | 362 | 84 | 84 |
| c2 | 1,601 | 479 | 511 | 491 | 81 | 81 |
| c3 | 1,675 | 1,675 | 3,438 | 1,021 | 88 | 88 |
| c4 | 422 | 1,491 | 431 | 1,379 | 84 | 84 |
| c5 | 411 | 469 | 601 | 796 | 84 | 598 |
| c6 | 555 | 560 | 494 | 429 | 80 | 80 |
| d1 | 993 | 1,771 | 1,092 | 2,828 | 301 | 1,771 |
| d2 | 1,771 | 1,600 | 2,850 | 3,848 | 2,076 | 2,077 |
| d3 | 1,312 | 727 | 898 | 774 | 871 | 891 |
| d4 | 1,028 | 1,781 | 1,309 | 1,518 | 1,074 | 1,438 |
| d5 | 1,562 | 1,318 | 899 | 1,257 | 2,022 | 1,104 |
| d6 | 682 | 1,749 | 1,144 | 2,506 | 894 | 1,359 |
| v1 | 1,757 | 1,757 | 2,113 | 3,870 | 1,935 | 1,935 |
| v2 | 815 | 872 | 766 | 1,193 | 151 | 151 |
| v3 | 1,520 | 1,337 | 787 | 895 | 149 | 149 |
| v4 | 866 | 1,337 | 1,732 | 1,286 | 153 | 153 |
| v5 | 893 | 1,277 | 1,340 | 1,270 | 158 | 158 |
| v6 | 1,748 | 1,748 | 3,834 | 3,834 | 3,834 | 3,834 |

## 9. What didn't work / residual costs (stated plainly)

- **The persistent pair still wins.** v1 and v6 deadlettered in **every bus run of both versions** (8 run-instances). Their combined price in C3 was 11,538 tokens for zero clean jobs — 38% of C3's total spend. The gold audit (A15) says the items are correctly labeled and genuinely hard (comparative/edge readings both models miss); no filed mechanism converts them, and the DLQ cap (leg 4) passed with **zero headroom** (4 of 4). On a workload with one more such item, the bus would fail leg 4 while still shipping nothing wrong — the cap, not correctness, is the binding constraint at the margin.
- **VERIFY yield did not improve** (8/12 in both bus systems; B shipped 4 of its VERIFY tasks wrong and got 8 "correct" only by also shipping the pair's wrong answers in some runs — B's VERIFY correct count is 8 with 4 wrong shipped). Routing cut VERIFY's *price* 44% (2,865.0 → 1,595.0); it did not make either model better at the two hard items.
- **The 4b leak persists on 4b rungs** (leak-flagged attempts: v6 a2 in C31; d2 a1 in C32) — routing reduced exposure; the generation-path fix (A16) remains the untested v4-class lever, alongside reason-feedback.
- **DRAFT remains the bus's most expensive class per job** (1,323.2) — long artifacts on a slow runner; the alternating ladder helped (C2ref 1,743.6) but DRAFT is where the remaining cost lives.

## 10. Confirmation (A10) and disclosures

- **A10 confirmation — PASSED:** because the bar was cleared on a tuning set (the v1 workload, used by v1/v2/v3), a **fresh-workload confirmation A/B** (18 new tasks, new seeds 20261115/20261116, same 8 legs, B vs C3) was run before finalizing the adoption packet. **Result: CLEARED, 8/8 legs** — C3 wall ratio 0.744 (cap 1.25), shipped-wrong 0 vs B's 8, correct 32 vs 28, tok/efj 1,121.5 vs B's 1,518.9, DLQ 4 = cap. Full record: `CONFIRMATION.md` in this folder. The win replicates on unseen tasks; the adoption packet is finalized on that basis.
- **Validator provenance (A11):** CLASSIFY and VERIFY validators compare against hidden gold; DRAFT is structural against prompt-visible material. All correctness numbers are validator-relative; in production a gold-free checker is a different instrument and the gate's production value would need its own measurement.
- **Tuning-set scope (A10/#14):** these numbers describe this workload and regime (two Qwen3 models, one Ollama service, Fortress). Task-paired outcomes: the same two tasks (v1, v6) account for every bus dead-letter in both versions; every other task was correct in at least 5 of the 6 bus runs.
- **n = 2 per arm (A12):** no confidence interval is available; per-run values are reported for every leg above. The C3 margins (wall 0.617× vs a 1.25 cap; tok/efj −44% vs the reference) are large relative to the observed run-to-run spread of any arm.
- **Regime:** all six runs shared the same placement regime (8b fully VRAM-resident; 4b mostly CPU-resident at ~8.2–8.4 calibration tok/s) — placement is the production service's own and was never manipulated (A8). Under a GPU-resident 4b (v2's evening regime) absolute walls would compress for every arm; the bar and yardstick are ratios within the regime and the ordering has now held in two different regimes (v2's and this one).

## 11. Recommendation

**Adopt Fleet Bus v3 as the working program** — pending Joe's ruling and the §10 confirmation. The adoption packet (`ADOPTION-PACKET.md`) carries the deployable article (`../code/`), the operating picture (DLQ review as the human surface; the v1/v6 class of persistent-misjudgment tasks as a known, priced abstention), and the two standing v4 candidates if the program continues: the generation-path think-leak fix (A16) and validator-reason feedback in retry prompts — neither is needed to justify v3, and neither should be bundled into an adoption deploy.
