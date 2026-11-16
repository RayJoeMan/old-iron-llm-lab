# CONFIRMATION SCORECARD — fresh workload, all arms fresh (Nov 15, 2026)

**Construction (as filed):** 18 fresh tasks (6/6/6, sha256 `5b48868e…`, golds independently derived with notes filed before launch), staged into the phase code dir by hash-verified swap (pre-swap `e8e3748b…` → staged `5b48868e…` → restored `e8e3748b…`, RESTORE_OK in the driver log). Order B1 → C3ref1 → S1 → C3ref2 → S2 → B2, 14:18:23–15:17:43 CST, Fortress exclusive. Worker kills on run 1s; checker kill on S run 2. S channels `swarmtest-conf-run1` / `swarmtest-conf-run2`, seeds 20261115 / 20261116. Base `~/swarmchat-phase/runs/confirmation/`; S metrics filed beside this scorecard.

## Raw results

| Arm (pooled) | Wall s | Tokens | Correct (C/D/V) | Lost | Dup | Ship-wrong | DLQ | tok/efj |
|---|---|---|---|---|---|---|---|---|
| B run 1 | 766.2 | 22,249 | 14 | 0 | 0 | 4 (cc6, cd4, cd6, cv1) | 0 | 1,589.21 |
| B run 2 | 696.1 | 20,326 | 15 | 0 | 0 | 3 (cd5, cd6, cv2) | 0 | 1,355.07 |
| **B pooled** | **1,462.3** | **42,575** | **29** | 0 | 0 | **7** | 0 | **1,468.10** |
| C3ref run 1 | 370.2 | 12,230 | 17 (6/6/5) | 0 | 0 | 0 | 1 (cv4) | 719.41 |
| C3ref run 2 | 480.3 | 15,382 | 17 (5/6/6) | 0 | 0 | 0 | 1 (cc6) | 904.82 |
| **C3ref pooled** | **850.5** | **27,612** | **34 (11/12/11)** | 0 | 0 | **0** | **2** | **812.12** |
| S run 1 | 377.7 | 12,791 | 17 (6/6/5) | 0 | 0 | 0 | 1 (cv4) | 752.41 |
| S run 2 | 444.5 | 14,713 | 17 (5/6/6) | 0 | 0 | 0 | 1 (cc6) | 865.47 |
| **S pooled** | **822.2** | **27,504** | **34 (11/12/11)** | **0** | **0** | **0** | **2** | **808.94** |

S per-run detail: accounted 18/18 both runs; coordination tokens 0; fenced RESULTs 0; silent-hold suspects none; **failed calls 0 and extra generations 0 in both runs** (no runner-stall event occurred in the confirmation window). Kills: S run 1 worker w1 killed on cc1 — recovery 134.9 s, cc1 delivered; S run 2 checker killed + pre-registered relaunch — clean 18/18. Fairness probes at S launches: 63.4/2.0 s and 40.2/2.1 s. B run 1 kill (b2 on cv2) recovered in 270.1 s; C3ref run 1 kill (c1 on cv4) recovered in 138.1 s. Mirrors: C3ref runs posted 108/108 and 118/118 events, 0 errors.

**Cross-medium identity worth naming:** S and C3ref deadlettered the *same tasks in the same runs* (cv4 in run 1 — early-DLQ on repeated WRONG_VERDICT_3; cc6 in run 2 — early-DLQ on repeated WRONG_OR_MULTI_LABEL) and produced identical per-class correct counts (11/12/11). On this workload the two media are behaviorally indistinguishable task-for-task; the differences are price, and both prices favor or match S.

## Bar (vs fresh B) — ALL LEGS PASS

1. Lost = 0, duplicated = 0 in each S run — PASS.
2. Accounted 18/18 each run; aggregate 36 ≥ B's 36 — PASS.
3. Shipped-wrong 0 < 7 — PASS.
4. DLQ aggregate 2 ≤ 4; per-run 1 ≤ 3 — PASS.
5. Wall 822.2 ≤ 1.25 × 1,462.3 = 1,827.9 (ratio 0.5623) — PASS.
6. Coordination tokens = 0 — PASS.
7. Interventions 0 ≤ 0 — PASS.
8. Gate + suite qualification green before the program's scored runs — PASS (of record for the campaign).

## Yardstick (vs fresh C3ref) — ALL CONDITIONS PASS, (ii) ROBUST THIS TIME

- (ii) S tok/efj **808.94** ≤ 812.12 × 1.10 = 893.33 — PASS with a 10.4% margin; S is below C3ref's own tok/efj outright. **Robustness:** both S runs individually pass (752.41 and 865.47 ≤ 893.33), and the A15 upper bound passes too — the only unlogged exposure is run 1's killed generation (bounded ≈ +1,630 tokens → ≈856.9 tok/efj ≤ 893.33); there were no timed-out calls to bound.
- (iii) S wall ratio vs fresh B 0.56227 ≤ C3ref's 0.58163 + 0.10 = 0.68163 — PASS; S's absolute wall (822.2 s) is also below C3ref's (850.5 s).
- (iv) Correct 34 ≥ 34; shipped-wrong = 0 — PASS.
- (v) Per-class deltas 0 / 0 / 0 — PASS.
- (vi) Medium-caused extra generations = 0 (total extra generations = 0) — PASS.

## Verdict

**CONFIRMED WIN.** The SwarmChat-coordinated system (Arm S, procedure v2) clears the bar against the file queue and matches-or-beats the Fleet Bus v3 ledger on the medium yardstick, on a fresh workload with all-fresh references — the same construction that certified Fleet Bus v3 in Phase 1. Combined with the tuning-workload screen (SCORECARD-V2.md), the phase's filed claim is established: **SwarmChat is a working program for the fleet's model work, at parity-or-better economics with the adopted bus, with the chat transcript as its native audit record.**

What this does not decide: whether to *adopt* SwarmChat alongside or instead of Fleet Bus v3 for any given workload — that is Joe's ruling, and the adoption packet (ADOPTION-PACKET.md) lays out the complement case with these numbers. Fleet Bus v3's adopted status is untouched by this result.
