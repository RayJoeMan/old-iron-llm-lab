# Validator-Feedback Experiment — NEGATIVE RESULT (closed; NOT part of the v3 adoption)

Filed as a negative result under this repo's honesty rules. Run Nov 15, 2026 on Fortress, after the v3 adoption, as a bounded experiment: does feeding the checker's validator reasons into retry prompts convert the persistent-misjudgment dead-letter class that v3 prices but cannot fix? The variant lived only in a scratch copy; **the adopted v3 article was never modified**, and amending it would take a new ruling.

**Filed bar (written before any scored run; all four legs required):**

| Leg | Filed bar | Measured | Verdict |
|---|---|---|---|
| (a) Conversion | ≥3 tasks converted (dead-lettered in both baseline runs **and** done in both feedback runs) | **0** (baseline-DLQ set = {v1, v6}; neither converted in both feedback runs) | **FAIL** |
| (b) Shipped-wrong | 0 in every scored run | 0 in all 6 runs | PASS |
| (c) Class price | Feedback class tok/efj < baseline class tok/efj | 2,123.1 vs 2,730.5 (−22.2%) | PASS |
| (d) Regression | vs v3's recorded C3 (correct ≥31, DLQ ≤5, tok/efj ≤1,036.5, wall ≤3,331.9 s, lost/dup 0) | correct 34, DLQ 2, tok/efj 960.8, wall 2,190.2 s, lost 0, dup 0 | PASS |

**Result: 1 of 4 legs failed — the conversion leg, which was the point of the experiment. Bar not cleared; the idea closes.**

| Run | Wall (s) | Tokens | Done | DLQ |
|---|---|---|---|---|
| CLASS BASE-1 | 1,431.2 | 19,683 | 6/12 | fv2, fv3, nc3, nv3, v1, v6 |
| CLASS BASE-2 | 1,555.5 | 21,275 | 9/12 | nv2, v1, v6 |
| CLASS FB-1 | 1,301.2 | 18,190 | 7/12 | fv2, nc3, nv2, v1, v6 |
| CLASS FB-2 | 1,433.4 | 20,025 | 11/12 | v6 |
| REG FB-1 | 1,229.2 | 18,288 | 17/18 | v6 |
| REG FB-2 | 961.0 | 14,378 | 17/18 | v6 |

**What the runs showed:**

1. **The "persistent" class is mostly variance, not a stable blind spot.** Under fresh replication only v1 and v6 dead-lettered in both baseline runs; four of BASE-1's six dead-letters solved in BASE-2 with no feedback at all, and one task flip-flopped across all four class runs. At temperature 0.3 these borderline VERIFY items sit on a sampling knife-edge; v3's two tests froze one draw of that variance into a "class."
2. **Feedback did not crack the true core.** v6 dead-lettered in all six runs: its verdicts oscillate across attempts, so early-DLQ never fires and naming the previous reasons in the retry did not break the oscillation. v1 converted in one of two class runs — short of the filed both-runs definition.
3. **The price/yield effect is real but unattributable.** Feedback raised class yield (18 vs 15 done of 24) and cut class tok/efj 22.2%, but with the baseline itself swinging 6→9 done between identical runs, an effect this size cannot be separated from run variance at n = 2.

Hard accounting held in every run: all tasks accounted, 0 failed calls, 0 lost, 0 duplicated.
