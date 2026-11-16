# Scored-Run Ledger — SwarmChat phase (tuning workload, 18 tasks)

Run order (filed): B1 → C3ref1 → S1 → C3ref2 → S2 → B2. All runs on Fortress, Nov 15, 2026, under the fairness protocol (defer guard load1 < 30; per-launch generation probes < 240 s; run_ab3 calibration for bus arms). Regime note: a zombie Ollama runner (~1,541% CPU, since Nov 14 ~20:05) is a constant background for every run (see SUITE-QUALIFICATION.md).

## B run 1 (file queue, fresh) — COMPLETE
wall **2,052.6 s** · accounted 18/18 · lost 0 · duplicated 0 · shipped-wrong **4** (d1, d2, d5, v6) · correct **14** · tokens 18,808 (18 calls, all qwen3:4b) · tok/efj **1,343.4** · kill test: worker b2 killed on v2, recovered, latency 430.1 s · calibration 4b probe 86.4 s.

## C3ref run 1 (Fleet Bus v3, same-regime reference) — COMPLETE
wall **1,253.2 s** · accounted 18/18 (16 delivered + 2 DLQ) · lost 0 · shipped-wrong **0** · correct **16** · tokens 13,390 (23 calls) · tok/efj **836.9** · DLQ: v1 (early-DLQ at attempt 2, WRONG_VERDICT_3 repeated — the persistent-misjudgment class) and v6 (4 attempts, alternating WRONG_VERDICT_3 / UNPARSEABLE; 3,834 tokens) · kill test: worker c1 killed on d1, recovered, latency 210.2 s · mirror: 112/112 events posted, 0 errors (channel name pre-existed from Phase 1; posts appended, disclosed in channel_setup.json) · calibration: 8b 14.7 s, 4b 118.8 s.

## S run 1 (SwarmChat-native) — COMPLETE AT CAP, 4 TASKS LOST (scored as it stands)
wall **3,600.0 s (cap)** · accounted **14/18** · correct **13** (CLASSIFY 5, DRAFT 4, VERIFY 4) · DLQ v1 · shipped-wrong **0** · duplicated 0 · tokens 8,117 (22 calls, 4 failed) · kill test: worker w2 killed on d1 at the 6th terminal; **d1 recovered and delivered, recovery interval 299.9 s** · fairness probes at launch: draft_4b 201.9 s, verify_8b 1.0 s (8b warm) · transcript 411 messages / 60,891 bytes.

**The stall (root-caused from the run's own logs):** at ~07:59 the qwen3:4b Ollama runner reloaded; four in-flight 4b generations (d4, d6 attempt 1; v6, c5 attempt 2) were orphaned and hung until workgen2's client timeout fired at 08:21:30 (call_log: 4 entries, eval 0, "timed out"). `arm_s.py`'s generation threads let the `TimeoutError` escape — the worker logs carry "Exception in thread Thread-N (generate)" tracebacks — so the four claims were never resolved: their workers RENEWed every 60 s (~200 RENEW messages) until run_sc's 60-min cap ended the run. The 4b runner answered a fresh probe in 1.6 s at 08:26 — the wedge was the transient reload, not a persistent outage.

**Classification:** an **S harness fault** (unhandled generation exception), triggered by an environment event. Per the filed rules it is **scored, not excused**: S run 1 fails the lost-task leg, and the pooled campaign accounting carries the 4 lost tasks. Phase 1's arms survive the same event class because their workers catch generation exceptions (fleetbus requeues); the chat harness did not — a real robustness difference the test existed to find.

**Mid-campaign repair (disclosed):** before S run 2, `arm_s.py` generate() was fixed to catch generation exceptions and surface them as empty-artifact RESULTs (validator FAIL → policy requeue on the next ladder rung), md5 `744d68a9` (was `7073fb61` at gate pass). The gate's stub mode never raises, so the gate could not have caught this; no other arm uses arm_s.py. S run 1 remains scored under the unfixed harness.

---

# V2 scored pair (procedure v2, ADJUDICATION-V2) — Nov 15, 2026

Pinned implementation (md5, verified before run 1 and after run 2): arm_s.py `eb432c11`, collect.py `df296176`, scproto.py `e17234d3`, run_sc.py `c60aa4f3`. Gate of record: Fortress gate-v2-full PASS 18/18 (10:21 CST); Mint pre-runs corroborate (MINT-PRERUN.md). Fingerprint: FINGERPRINT-V2.md. Sequencing: the pair launched at 12:42 CST, after the Fleet Bus feedback campaign completed (ALL_LEGS_DONE 12:35:31) per Joe's ruling; Fortress exclusive during both runs.

## S-V2 run 1 — COMPLETE
wall **1,253.7 s** · accounted **18/18** · lost **0** · duplicated **0** · shipped-wrong **0** · correct **16** (C6/D6/V4) · DLQ v1, v6 · tokens **17,692** (30 calls, 3 failed) · tok/efj **1,105.75** · coord tokens 0 · fenced 0 · silent-hold suspects none · launch load 0.73, probes 72.1/1.2 s · kill test: worker w2 killed on d1, **recovery 291.9 s, d1 delivered** · transcript 255 msgs / 69,045 B. Failed calls: d6@1, v1@2, v6@4 — all qwen3:4b TimeoutError, claim abandoned, same attempt re-driven (see SCORECARD-V2.md).

## S-V2 run 2 — COMPLETE
wall **1,194.4 s** · accounted **18/18** · lost **0** · duplicated **0** · shipped-wrong **0** · correct **16** (C6/D6/V4) · DLQ v1, v6 · tokens **15,915** (26 calls, 3 failed) · tok/efj **994.69** · coord tokens 0 · fenced 0 · silent-hold suspects none · launch load 24.35 (< 30), probes 144.3/0.8 s · checker kill + pre-registered relaunch: clean completion, no duplicate terminals · transcript 223 msgs / 58,404 B. Failed calls: d2@1, v1@2, v6@2 — same TimeoutError/abandonment pattern.

## V2 scoring (vs frozen v1 references) — see SCORECARD-V2.md
Pooled S v2: wall 2,448.1 · tokens 33,607 · correct 32 (12/12/8) · tok/efj **1,050.22**. **Bar: all 8 legs PASS. Yardstick: all conditions PASS** ((ii) by 2.84%, disclosed **not robust** — per-run split and the A15 bound both flip it). A19 improvement test satisfied. Verdict: **provisional screen WIN** — decisive test is the confirmation campaign below.

# Confirmation campaign (fresh workload, all arms fresh) — LAUNCHED 14:18:23 CST

Workload staged by verified swap in the phase code dir: scored `e8e3748b…` → confirmation `5b48868e…` (pre-swap and staged hashes logged in confirmation-driver.log; pristine scored copy held at `~/swarmchat-phase/workload-scored-pristine.json`; restore + hash verification are the driver's final steps). Order B1 → C3ref1 → S1 → C3ref2 → S2 → B2; worker kills on run 1s, checker kill on S run 2; S channels `swarmtest-conf-run1` / `swarmtest-conf-run2`, seeds 20261115 / 20261116; base `~/swarmchat-phase/runs/confirmation`. Same bar vs fresh B, same yardstick vs fresh C3ref.

## Confirmation B run 1 — COMPLETE
wall **766.2 s** · accounted 18/18 · lost 0 · shipped-wrong **4** (cc6, cd4, cd6, cv1) · correct **14** · tokens 22,249 (18 calls) · tok/efj **1,589.21** · kill: b2 on cv2, recovered 270.1 s.

## Confirmation C3ref run 1 — COMPLETE
wall **370.2 s** · accounted 18/18 (17 delivered + 1 DLQ) · lost 0 · shipped-wrong **0** · correct **17** (C6/D6/V5) · DLQ cv4 (early, WRONG_VERDICT_3 repeated) · tokens 12,230 (22 calls) · tok/efj **719.41** · kill: c1 on cv4, recovered 138.1 s · mirror 108/108, 0 errors.

## Confirmation S run 1 — COMPLETE
wall **377.7 s** · accounted **18/18** · lost **0** · duplicated **0** · shipped-wrong **0** · correct **17** (C6/D6/V5) · DLQ cv4 · tokens **12,791** (23 calls, **0 failed**) · tok/efj **752.41** · extra generations **0** · fenced 0 · silent-hold none · probes 63.4/2.0 s · kill: w1 on cc1, **recovery 134.9 s, cc1 delivered**.

## Confirmation C3ref run 2 — COMPLETE
wall **480.3 s** · accounted 18/18 (17 + 1 DLQ) · lost 0 · shipped-wrong **0** · correct **17** (C5/D6/V6) · DLQ cc6 (early, WRONG_OR_MULTI_LABEL repeated) · tokens 15,382 (25 calls) · tok/efj **904.82** · mirror 118/118, 0 errors.

## Confirmation S run 2 — COMPLETE
wall **444.5 s** · accounted **18/18** · lost **0** · duplicated **0** · shipped-wrong **0** · correct **17** (C5/D6/V6) · DLQ cc6 · tokens **14,713** (24 calls, **0 failed**) · tok/efj **865.47** · extra generations **0** · fenced 0 · silent-hold none · probes 40.2/2.1 s · checker kill + pre-registered relaunch: clean completion.

## Confirmation B run 2 — COMPLETE
wall **696.1 s** · accounted 18/18 · lost 0 · shipped-wrong **3** (cd5, cd6, cv2) · correct **15** · tokens 20,326 (18 calls) · tok/efj **1,355.07**.

## Confirmation scoring — see CONFIRMATION-SCORECARD.md
Pooled: B wall 1,462.3 / tok 42,575 / correct 29 / ship-wrong 7 · C3ref 850.5 / 27,612 / 34 / 0 · **S 822.2 / 27,504 / 34 / 0, tok/efj 808.94 vs C3ref 812.12**. **Bar: all legs PASS. Yardstick: all conditions PASS, (ii) robust (per-run split and A15 bound both hold). CONFIRMED WIN.** Workload restored to `e8e3748b…` (RESTORE_OK).

## Post-phase suite + cleanup (Nov 15, evening)
Post-phase suite (idle, pinned 3.12): **181 tests, FAILED (5F+1E) in 106.4 s** — all failures in test_by_hand.py, the Nov 14 signature, on an idle box; filed verbatim in RESULTS.md, non-scored, not re-run. Cleanup complete: channel exports sha-filed before agent removal (counts match metrics), authorship-survives-removal proven on a scratch agent, 5 test agents + scratch agents removed, channel_creator grant removed, contact policy restored to the phase-start backup (verified exact; one wrapper-shape mishap in the first restore attempt, corrected and disclosed in RESULTS.md), 30 phase channels archived (none deleted), server never restarted.
