# Fleet Bus A/B — RESULTS

**Date:** 2026-11-13 (runs 15:57–21:04 CT) · **Design:** `../design/DESIGN.md` (pre-registered before any run) · **Run ledger:** `RUN-LEDGER.md` · **Per-run metrics:** `metrics/*.json` (copied from Fortress `~/fleet-bus-ab/runs/`)

## Verdict

**NO — the Fleet Bus prototype does not beat both incumbents on the pre-registered criteria.** The win bar (DESIGN §6) fails on three of its six legs: the zero-loss hard gate, the wall-time leg, and the validator leg. Per the consequence filed in the design before the runs: **the file queue remains the fleet's coordination method; SwarmChat remains durable-log plumbing, not a coordinator; the Fleet Bus design is filed as tested and refuted in this configuration.** Adoption was never this report's call — but on the filed criteria there is nothing to adopt. What the A/B did prove, leg by leg, is below; the bus's coordination mechanics were flawless, and it lost on the work-quality interface, which is a different and more useful finding than "the bus is slow."

## The numbers (2 runs per arm, 18 tasks per run, identical workload/model/conditions)

| Metric (aggregate of 2 runs) | A — SwarmChat | B — File queue | C — Fleet Bus |
|---|---|---|---|
| Wall time, total | **7,202.2 s** (both runs hit the 60-min cap) | **3,058.7 s** | 5,566.9 s |
| Tasks completed | 25 / 36 | **36 / 36** | 31 / 36 |
| Tasks lost | 11 (7 + 4) | **0** | 5 (3 + 2) |
| Tasks duplicated | 0 | 0 | 0 |
| Validator pass, first attempt | 17 / 25 scored* (68%) | **30 / 36 (83%)** | 27 / 36 (75%) |
| Work tokens (generations) | 31,705 (27 calls) | 38,583 (36 calls) | 68,227 (52 calls) |
| **Coordination tokens** | **79,601 (75 calls)** | **0** | **0** |
| Coordination messages / events | 109 msgs / 54,977 B | 72 file ops | 246 ledger events / 27,532 B |
| Kill test (run 1): victim → recovery | cc-fortress / v3 → **recovered, 794.5 s** | b3 / c3 → **recovered, 336.1 s** | c3 / c3 → **recovered, 682.6 s** |
| Coordinator interventions | 0 | 0† | 0 |

\* Arm A scores only the tasks it completed (11 and 14); its unscored tasks are among the lost.
† Plus one disclosed harness repair between B run attempts — see Failures, item 2. It occurred outside any run's execution and is not counted in the in-run intervention metric; it is documented here and in the ledger so the comparison stays honest.

Per-run walls: A 3,600.3 / 3,601.9 (cap, cap) · B 1,722.4 / 1,336.3 · C 2,740.4 / 2,826.5.

## The win bar, leg by leg (DESIGN §6 — all legs required)

1. **Hard gate — C lost = 0 and duplicated = 0 in EACH run.** Duplication 0 in both runs ✓. Lost 3 (run 1: d1, v1, v6) and 2 (run 2: d5, v1) ✗. **FAIL.**
2. **Coordination tokens — C ≥30% below A, and C coordination-generation tokens = 0.** C = 0 vs A = 79,601, counted from endpoint counters. **PASS.**
3. **Wall — C ≤ 1.10 × B and ≤ 1.10 × A.** C 5,566.9 s vs B 3,058.7 s = 1.82× ✗ (vs A 7,202.2 s = 0.77× ✓, but both are required). **FAIL.**
4. **Interventions — C ≤ A and C ≤ B.** 0 everywhere. **PASS.**
5. **Validator — C ≥ A and ≥ B in aggregate; no run worse than either by >1 task.** C 27/36 < B 30/36 ✗; run 2 alone: C 13 vs B 16 (worse by 3) ✗. **FAIL.**
6. **Mechanics gate (Arm C eligibility).** All four legs passed pre-run (1,000-task claim flood with 0 duplicate claims, duplicate-enqueue storm → exactly 18 tasks, kill/reaper over 100 tasks → 100 done, JSONL replay == ledger). **PASS.**

## Why C lost — the gate worked as designed, and that was the problem

Every task C lost died the same way: three generations, three deterministic-validator failures, attempt cap reached, task marked `dead` (= lost, per the filed rule). The failure reasons are in the ledger DB:

- **v1 (VERIFY) died in both runs** — `WRONG_VERDICT_3` on all six attempts across the two runs. The model persistently misjudges one claim; the gate persistently refuses it. Arms A and B delivered that same wrong answer as a completed result (it shows as a validator failure in their columns — v1 failed in A run 2 and B run 2 — but it was *delivered*).
- **d1 (run 1) and d5 (run 2), DRAFTs** — `MISSING_FIELD / BAD_SOURCE / SHORT_SUMMARY`: qwen3:4b's reasoning leaks into the response untagged on this Ollama build, and on these tasks it consumed the generation budget before a valid card emerged, three times in a row.
- **v6 (run 1)** — `UNPARSEABLE / WRONG_VERDICT` mixes across attempts. In run 2, v6 failed its first attempt and passed on retry — the gate's intended success case.

So the trade the bus makes is real and measurable: **it converts bad work into lost tasks; the incumbents convert it into delivered results.** With a stronger worker model (or an unbounded/escalating attempt policy), that trade might favor the bus. With qwen3:4b under contention, ~14% of tasks (5/36) fell on the wrong side of it, retries inflated C's work tokens +77% over B (68,227 vs 38,583) and its wall +82%, and the filed bar — correctly, by its own terms — calls that a loss. Note what did *not* fail in C: zero duplicated work in 36 tasks, zero coordination tokens, exact idempotency, a passed mechanics gate under a 1,000-task flood, and a successful kill recovery. The ledger/lease core is sound; the validator-gate policy on top of it is what the bar rejected.

## Why A lost — chat coordination costs more than the work

Arm A is the A/B's clearest negative result. Coordination by LLM generation — one generation to choose each claim, one to compose each completion — consumed **79,601 tokens against 31,705 tokens of actual work (2.5×)**, serialized through the same contended endpoint as the work itself. Both runs hit the 60-minute cap; 11 of 36 tasks never completed; several were never even claimed (run 1 logged only 12 work calls). The deterministic ownership guard did hold (zero duplicated completions, despite repeated duplicate-claim races), and the kill recovery worked (v3 reclaimed and completed in 794.5 s — the slowest recovery, bounded below by the 150 s staleness window plus a full claim-generation cycle). SwarmChat itself never malfunctioned; the pattern it was asked to perform — LLM-mediated claim arbitration — is simply too expensive per decision at this scale. This matches and extends the Nov 11 pilot (Stage 2 wall 7.6 h for 24 briefs on the Mint): the cost is structural, not incidental.

## Why B won — and the one weakness the A/B exposed in it

The file queue completed 36/36 tasks, lost none, duplicated none, spent zero coordination tokens, posted the fastest walls in both runs, and recovered from the kill fastest (336.1 s ≈ 150 s staleness + one generation). At 3 workers / 18 tasks / one host, rename-under-flock claims are simply sufficient. The A/B's one genuine B-side finding came from its own first (invalid) attempt: **file mtime is not a lease.** `os.rename` preserves mtime, so a claim taken from an old queue file is born "stale" to any mtime-based sweeper — the first B attempt looped one task 30+ times and froze at 5 completions. That attempt was stopped, the defect repaired to match the filed design (claim resets the file clock; heartbeat touches immediately), the discarded attempt preserved on-box (`runs/B-run1-harnessbug-1738/`), and both B runs re-executed clean. The fleet's real chain-script discipline doesn't use mtime sweepers, so production was never exposed — but any future file-queue automation must treat this as a rule: staleness needs a claim-time timestamp, not a file's mtime.

## Conditions (read the walls with these)

All runs executed on Fortress during live fleet work (F2 funnel battery, YOLO dual pass) at load averages 20–54, sharing one Ollama qwen3:4b runner whose effective throughput measured 6.6 tok/s at peak contention (vs 51.6 tok/s solo for qwen3:8b on an RTX card in F1). Absolute wall times are contention walls and would compress on an idle box; the arm ordering is structural (coordination generations and validation retries serialize on the same endpoint) and was counterbalanced by run order (run 1: A,B,C; run 2: C,B,A) with seeded task shuffles. Two pre-run design amendments (generation budget 512 → 1600 tokens after the reasoning-leak smoke finding; run cap 30 → 60 min) are recorded in DESIGN §3.1 with reasons; both applied identically to all arms. Arm A ran SwarmChat in its pinned Python 3.12 environment per Joe's direction (no porting/patching; the 3.14 suite failures, F-66, are the incumbent's recorded deployment context). Disclosed harness asymmetries D-1…D-5 stand as filed in the run ledger (Arm C's completion definition is the strictest of the three — the bias ran against the bus, and it still lost on delivery).

## Recommendation (as filed in DESIGN §6 for a failed bar)

1. **File queue stays** the fleet's coordination method. It won on delivery, wall, and cost simultaneously.
2. **SwarmChat stays as durable-log/presence plumbing** — the role its pilot actually validated — and is not used for claim arbitration.
3. **The Fleet Bus design is filed as tested/refuted in this configuration.** If it is ever revisited, the A/B points at the two changes that matter: a validator policy that escalates instead of dropping (stronger model on final attempt, or dead-letter to a human queue rather than `dead`), and a worker pool strong enough that the gate's refusal rate is rare. The ledger core (leases, idempotency, reaper) needs no redesign — it was the only component that never failed at anything.
4. **Production is untouched either way.** The prototype remains a removable test article at `~/fleet-bus-ab/` on Fortress (workspace masters in `../code/`); nothing was adopted, migrated, or replaced.

*All numbers in this report are from the per-run `metrics.json` files (endpoint counters and on-disk state), the Arm C ledger DB, and the SwarmChat channel record — first-hand reads, per the commission. Raw artifacts remain on Fortress under `~/fleet-bus-ab/runs/`.*
