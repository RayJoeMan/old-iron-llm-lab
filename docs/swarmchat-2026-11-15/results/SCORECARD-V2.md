# SCORECARD — Arm S procedure V2 vs frozen V1 references (historical-reference provisional screen)

**Runs:** S-V2 run 1 (Nov 15, 2026, 12:42:42–13:04:50 CST, channel `swarmtest-s2-run1`, seed 20261113, worker kill test) and run 2 (13:04:50–13:27:10 CST, channel `swarmtest-s2-run2`, seed 20261114, checker kill + pre-registered relaunch). Base `~/swarmchat-phase/runs/scored-v2/`; metrics filed beside this scorecard in `scored-v2/`. Pinned implementation verified by md5 before run 1, between runs (driver is sequential, no code path touched), and after run 2: arm_s.py `eb432c11`, collect.py `df296176`, scproto.py `e17234d3`, run_sc.py `c60aa4f3`. Environment fingerprint: `FINGERPRINT-V2.md` (matches ADJUDICATION-V2 §5 in full). Gate of record: Fortress gate-v2-full **PASS 18/18**; suite qualification 3/3 green; API probe 7/7 (≥99/100 wait-after-kill under load). Mint pre-runs corroborate (MINT-PRERUN.md) — labeled, non-scoring.

## Raw results

| Arm (2 runs pooled) | Wall s | Tokens | Correct (C/D/V) | Lost | Dup | Ship-wrong | DLQ | tok/efj |
|---|---|---|---|---|---|---|---|---|
| B (v1, frozen) | 3,659.0 | 40,303 | 26 (11/6/9) | 0 | — | 10 | 0 | 1,550.12 |
| C3ref (v1, frozen) | 2,394.2 | 31,445 | 32 (12/12/8) | 0 | — | 0 | 4 | 982.66 |
| **S v2 run 1** | 1,253.7 | 17,692 | 16 (6/6/4) | **0** | **0** | 0 | 2 (v1, v6) | 1,105.75 |
| **S v2 run 2** | 1,194.4 | 15,915 | 16 (6/6/4) | **0** | **0** | 0 | 2 (v1, v6) | 994.69 |
| **S v2 pooled** | **2,448.1** | **33,607** | **32 (12/12/8)** | **0** | **0** | **0** | **4** | **1,050.22** |

S v2 per-class tok/efj (pooled): CLASSIFY 1,002 tok / 12 = **83.50**; DRAFT 17,910 / 12 = **1,492.50**; VERIFY 14,695 / 8 = **1,836.88**.

Run conditions: run 1 launch load 0.73, probes draft_4b 72.1 s / verify_8b 1.2 s; worker w2 SIGKILLed mid-generation on d1 — **recovery interval 291.9 s, d1 delivered** (attempt 2). Run 2 launch load 24.35 (< 30 guard), probes 144.3 s / 0.8 s; checker SIGKILLed and relaunched per pre-registration — run completed 18/18, no duplicate terminal events. Coordination tokens 0 both runs; interventions 0 both runs; fenced RESULTs 0 both runs; `silent_hold_suspects` empty both runs. Transport: run 1 — 255 transcript messages / 69,045 B (CLAIM 82, RENEW 67, RESULT 27, VERDICT 27); run 2 — 223 / 58,404 B (CLAIM 65, RENEW 71, RESULT 23, VERDICT 23).

## The v1 failure event recurred — and was absorbed

Each v2 run logged **3 failed generation calls, all qwen3:4b `TimeoutError: timed out`, 0 tokens** (run 1: d6@1, v1@2, v6@4; run 2: d2@1, v1@2, v6@2), the same runner-stall signature that sank v1-S1. Under the v2 parity procedure each was handled identically to C3: worker logged the failure, **abandoned the claim** (renewals stopped), the checker's lease machinery re-drove the **same attempt**, and every affected task reached a correct terminal state (d6, d2 delivered; v1, v6 deadlettered through the normal validator ladder). Cost per the adjudicated pricing: one concurrent ~600 s timeout block per run, inside the wall budget. **Zero lost tasks.** This is the procedure working as adjudicated, on the exact fault that motivated it.

## Bar (DESIGN §5, vs frozen B) — ALL 8 LEGS PASS

1. Lost = 0 and duplicated = 0 in each run — **PASS** (v1 failed).
2. Accounted 18/18 in each run; aggregate 36 ≥ B's 36 — **PASS** (v1 failed).
3. Shipped-wrong 0 < B's 10 — PASS.
4. DLQ aggregate 4 ≤ 4; per-run 2 ≤ 3 — PASS (at the aggregate cap, not over it).
5. Wall 2,448.1 ≤ 1.25 × 3,659.0 = 4,573.75 (ratio 0.6691) — PASS.
6. Coordination tokens = 0 — PASS (structural).
7. Interventions 0 ≤ B's 0 — PASS (kills pre-registered, exempt).
8. Gate 18/18 in full + suite qualification green before the runs — PASS.

## Yardstick (medium claim, vs frozen C3ref) — ALL CONDITIONS PASS

- (ii) tok/efj 1,050.22 ≤ 982.66 × 1.10 = 1,080.93 — **PASS**, margin 30.71 tokens (2.84%). **Not robust** (below).
- (iii) S wall ratio vs B 0.66908 ≤ C3ref's 0.65436 + 0.10 = 0.75436 — PASS (identically: aggregate 2,448.1 ≤ the adjudicated ceiling 2,760.1 s).
- (iv) Correct 32 ≥ 32, shipped-wrong = 0 — PASS (v1 failed at 30).
- (v) Per-class yield deltas vs C3ref: CLASSIFY 0, DRAFT 0, VERIFY 0 (none more than 1 below) — PASS (v1 failed DRAFT −2).
- (vi) Medium-caused extra generations = **0** — PASS. The metrics count 3 extra generations per run; under ADJUDICATION-V2 §8 every one is **runner-caused**: each pairs exactly with a call_log `TimeoutError` entry and a worker-log "generation FAILED … claim abandoned" line for the same (task, attempt), with no epoch/lease anomaly (silent-hold audit empty, nothing lost). The run-1 kill-test crash path is excluded separately per the filed text and produced no extra logged generation.

## A19 improvement test — SATISFIED

V2 clears both failed v1 legs (1 and 2) and loses no leg v1 passed (bar 3–8 all pass; yardstick (ii) and (vi), the conditions v1's analysis passed, both pass).

## Robustness disclosure (DESIGN §5)

Yardstick (ii) is **not robust**: the per-run split flips it (run 1 alone: 1,105.75 > 1,080.93; run 2 alone: 994.69 <), and the A15 upper bound flips it too (7 unlogged/zero-logged calls — 6 timeouts + 1 killed generation — bounded at num_predict 1,600 + prompt each ≈ +12,600 tokens → ≈1,444 tok/efj). Every other bar and yardstick leg passes by a wide margin under any of these readings. Per the filed construction this screen is **provisional**: the win stands or falls on the all-fresh confirmation campaign (fresh B, C3ref, and S pairs on the pre-committed confirmation workload, sha256 `5b48868e…`), launched 14:18 CST today.

**Screen verdict: BAR CLEARED + YARDSTICK CLEARED (provisional, historical-reference).** No adoption claim is made on this screen; production adoption remains Joe's ruling after confirmation.
