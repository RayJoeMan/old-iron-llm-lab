# Fleet Bus v3 — Fresh-Workload Confirmation (A10)

**Requirement (filed pre-build, amendment A10):** a version that clears the win bar on the tuning set must pass a confirmation A/B on a fresh workload — same generator shapes, new tasks and seeds, same 8 legs — before its adoption packet is finalized.

**Article:** `~/fleet-bus-ab3-confirm/` on Fortress. Code identical to the main article except `run_ab3.py` seeds {1: 20261115, 2: 20261116} and confirm mirror-channel names (verified by diff: only `run_ab3.py` + `workload.json` differ). **Workload:** `../confirm/workload-confirm.json` — 18 new tasks (nc1–6 CLASSIFY, nd1–6 DRAFT, nv1–6 VERIFY), gold mechanically derived from each task's own text at authoring and self-checked against the validators; the set deliberately mirrors the tuning set's difficulty mix, including a comparative trap (nv3), an after-11-PM service edge (nv2), and a two-consecutive-years reading (nv6). **Order:** B run 1 (kill) → C3 run 1 (kill) → C3 run 2 → B run 2, same fairness protocol (load < 30 + dual probe < 240 s before every launch; measurements in `RUN-LEDGER.md`). No exclusions, no relaunches, no interventions.

## Runs

| Run | Wall (s) | Done | DLQ | Lost | Shipped-wrong | Tokens | Correct | tok/efj |
|---|---|---|---|---|---|---|---|---|
| B run 1 (kill) | 2,340.6 | 18 | — | 0 | 5 (nc3, nd2, nd4, nv2, nv3) | 21,283 | 13 | 1,637.2 |
| B run 2 | 2,344.7 | 18 | — | 0 | 3 (nd2, nv2, nv3) | 21,245 | 15 | 1,416.3 |
| C3 run 1 (kill) | 1,842.1 | 16 | 2 (nc3*, nv2) | 0 | 0 | 18,978 | 16 | 1,186.1 |
| C3 run 2 | 1,643.9 | 16 | 2 (nv2, nv3) | 0 | 0 | 16,910 | 16 | 1,056.9 |

*nc3 early-DLQ at attempt 2 ({WRONG_OR_MULTI_LABEL}) in run 1; it passed in run 2. Kill recoveries: B1 446.1 s (nd3), C31 204.2 s (nd1). Mirror: 132/132 and 122/122 events, 0 errors. Failed generation calls: 0 in all four runs. Aggregates — **B:** wall 4,685.3 · tokens 42,528 · correct 28 · shipped-wrong 8 · efj 1,518.9. **C3:** wall 3,486.0 · tokens 35,888 · correct 32 · DLQ 4 · efj 1,121.5.

## Scorecard — same 8 legs, C3 vs fresh B

| # | Leg | Result |
|---|---|---|
| 1 | Lost = 0 and duplicated = 0, each run | **PASS** (0/0 both runs) |
| 2 | Accounted 18/18 each run; aggregate ≥ B | **PASS** (36 ≥ 36) |
| 3 | Shipped-wrong < B | **PASS** (0 < 8) |
| 4 | DLQ ≤ 4 aggregate, ≤ 3 per run | **PASS** (4; 2 + 2) |
| 5 | Wall ≤ 1.25 × B | **PASS** (ratio **0.744**) |
| 6 | Coordination tokens = 0 | **PASS** |
| 7 | Interventions ≤ B | **PASS** (0 ≤ 0) |
| 8 | Mechanics gate | **PASS** (the identical policy code carries the main test's gate-results3.json) |

**CONFIRMATION: CLEARED, 8/8.** Per-class correct — C3: CLASSIFY 11, DRAFT 12, VERIFY 9 · B: CLASSIFY 11, DRAFT 9, VERIFY 8.

## Notes

- **The fresh set behaved like the tuning set for B** (aggregate wall/tokens/correct/shipped-wrong within ~1% of the main test's B aggregate), which validates the set's difficulty calibration — and C3's advantage replicated at a slightly smaller wall margin (0.744 vs 0.617) and a larger VERIFY yield (9 vs the tuning set's 8): the win is not an artifact of the v1 workload's quirks.
- **The trap items did their job.** B shipped nv2 (after-11-PM edge) and nv3 (comparative) wrong in *both* runs, and nd2 in both runs. Under C3, nv2 deadlettered in both runs (priced abstention), nv3 deadlettered once and was delivered correct once, and nd2/nd4 were delivered correct in both runs.
- **A13 routing-regression record (as pre-registered):** one CLASSIFY dead-letter occurred (nc3, run 1, early-DLQ after both models chose the same wrong label). It is recorded as a routing regression per the filing — with its context: the same item was shipped *wrong* by B in run 1, so the system's failure mode on the item was a surfaced abstention rather than a silent error, and nc3 passed cleanly in run 2.
- The DLQ cap again passed at exactly 4 of 4 — the same binding-margin observation as the main test (RESULTS.md §9): the persistent-misjudgment class, not correctness, is the constraint to watch in production sizing.
