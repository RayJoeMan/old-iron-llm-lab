# Arm S Mechanics Gate — RESULTS (DESIGN.md §6)

**Verdict: PASS — 17/17 legs**, gate3 run, Nov 15, 2026 (`gate-results-s.json`, on-box `~/swarmchat-phase/runs/gate3/`). The gate ran the real harness (`arm_s.py`, stub generation) on throwaway channels. Three attempts were needed; the failures found two real harness bugs, both fixed and re-proven:

## Bugs the gate caught (the gate doing its job)

1. **Deterministic double generation (leg a, attempt 1: 40 generations for 20 tasks).** The worker took its state snapshot *before* posting finished RESULTs, then seeked work from that stale snapshot — the just-posted RESULT was invisible, so it generated a second time for the same epoch. Same-worker pairs in the generation log isolated it from the cross-worker race it mimicked. **Fix:** post finished RESULTs first, then snapshot (arm_s.py worker loop). Re-proven: exactly 20 generations, 0 fenced.
2. **Foreign CLAIMs entered protocol state (leg o, attempt 1: ignored=2 of 4).** `derive_state` role-checked VERDICT/DELIVERED/TASK senders but not CLAIM/RENEW — a non-worker CLAIM could have become an epoch's confirmed claim and stalled it until lease expiry (its RESULT could never be accepted). Malformed lines also went uncounted. **Fix:** sender-role acceptance for CLAIM/RENEW (workers only) and all non-accepted messages counted in `_ignored` (scproto.py). Re-proven: 4/4 ignored, real flow unaffected.

Gate-harness artifacts fixed along the way (not product bugs): pilot-admin token path; verdicts.jsonl location; claims-list shape in two legs; **channel reuse across gate runs** (server channels persist — run 2's dispatcher read run 1's transcripts and posted 0 tasks; channels are now run-tagged unique); orphaned harness processes after failed legs (now stopped in a `finally`).

## Legs (all PASS, gate3)

| Leg | Result |
|---|---|
| (a) claim race ×20 | exactly 20 generations, 20 delivered, 0 fenced |
| (b) claim-confirm | earlier claim blocks the second worker entirely; first claim's RESULT delivers |
| (c) early-DLQ matrix | identical pair DLQs at attempt 2 (`early_dlq` logged); differing pairs run to 4; superset pair does not fire, delivers at 3 |
| (d) fencing after DEADLETTER | post-terminal correct RESULT changes nothing; 1 terminal event |
| (e) lease expiry | lease REQUEUE fired; second claim delivered; late RESULT inert |
| (f) kill recovery, full 18 | worker SIGKILLed mid-generation; 18/18 accounted, killed task delivered, no duplicate terminals |
| (g) full stub run, checker vs collector | exact agreement: 17 delivered-correct, v1 DLQ, 0 lost, 0 duplicated |
| (h) duplicate RESULT | second RESULT fenced; exactly one DELIVERED |
| (i) late RESULT after lease requeue | accepted RESULT is the second claim's; its artifact stands |
| (j) RESULT racing VERDICT/REQUEUE | exactly one requeue, one delivery |
| (k) stale-epoch CLAIM | ignored by workers and checker; attempt 2 delivers |
| (l) checker crash ×2 | transcript replay recovers; 6 delivered, 0 duplicate terminals |
| (m) dispatcher crash | killed after ~9 TASKs; relaunch posts exactly the missing 9 |
| (n) SIGSTOPped worker | misses the wake, catches up on full re-read (process state verified `T` while stopped) |
| (o) foreign + malformed | fake VERDICT/DELIVERED, malformed line, non-worker CLAIM all ignored |
| (p) payload fidelity via harness | 6,525-char artifact byte-exact (sha256) |
| (q) kill-victim selection | both seeded variants pick the earliest confirmed-first in-flight claim |

## Code state at gate pass (md5, identical local and on-box)

arm_s.py `7073fb61` · scproto.py `e17234d3` · gate_s.py `1176cba4` · collect.py `acbaabfc` · run_sc.py `c60aa4f3` (run_sc carries the fairness-probe addition; the gate does not exercise it beyond leg (q)'s import).

---

## V2 gate addendum (ADJUDICATION-V2)

**Verdict: PASS — 18/18 legs**, full rerun `gate-v2-full`, Nov 15, 2026 (`gate-results-s-v2.json`, on-box `~/swarmchat-phase/runs/gate-v2-full/`). Legs (a)–(q) all PASS on the pinned v2 implementation (md5 verified on-box at run time: arm_s.py `eb432c11`, collect.py `df296176`, scproto.py `e17234d3`, run_sc.py `c60aa4f3`, gate_s.py `2b523885`).

New leg (r) **generation-exception parity** PASS (83.1 s): r1 per-class (CLASSIFY/DRAFT/VERIFY) raise_first → claim abandonment, no validator verdict, same attempt redelivered; r3 three concurrent hang-then-raise generations all recovered; r4 raise-always → DEADLETTER reason `LEASE_EXHAUSTED` with zero validator verdicts; r5 first RESULT post throws (injected) → retried to exactly one RESULT.

Path here: first v2 gate run scored 17/18 — leg (r) failed on a gate-script defect only (the raise_first stub returned the literal "PASS" artifact, invalid for CLASSIFY/VERIFY, so attempt-2 verdicts appeared). Fixed in gate_s.py only (per-class artifacts in attempt-1 specs); arm_s.py untouched. Leg (r) standalone rerun PASS, then the full (a)–(r) rerun PASS above. No scored-arm code changed at any point in this sequence.
