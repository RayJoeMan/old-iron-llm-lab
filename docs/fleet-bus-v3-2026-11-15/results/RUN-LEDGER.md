# Fleet Bus v3 — Run Ledger

**Program:** Fleet Bus v3 A/B (design: `../design/DESIGN.md` as amended by `../design/ADJUDICATION.md`). **Article:** `~/fleet-bus-ab3/` on Fortress (exclusive to this program; Tranche B parked by Joe Nov 14, 2026). **Order filed:** B run 1 (kill) → C2 run 1 reference (kill) → C3 run 1 (kill) → C3 run 2 → C2 run 2 reference → B run 2.

## Environment of record (filed before the scored runs, per A8)

- **Ollama service (production, untouched):** system service, `OLLAMA_HOST` set to the machine tailnet address (tailnet only), `OLLAMA_KEEP_ALIVE=30m`; no `OLLAMA_MAX_LOADED_MODELS` / `OLLAMA_NUM_PARALLEL` overrides set (service defaults). Runner placement is the service's own; never manipulated for a run.
- **Co-residency:** verified in the mechanics gate (leg P8): qwen3:4b and qwen3:8b resident simultaneously in `/api/ps`.
- **Fairness gate per launch (A8):** 1-min load < 30 **and** dual probe (4b DRAFT d1 + 8b VERIFY v1 through `workgen2.run_work`, each < 240 s), run identically before every arm's launch; residency (per-bus `memory.used` + `/api/ps`) recorded per launch.

## Design / build / gate record

- **Nov 14, 2026 (evening):** v3 design filed (`../design/DESIGN.md`). Dual frontier checks run against the identical packet: GPT-6 Astra (16 issues, 3 BLOCKER) and Claude Opus 5.5 (1 BLOCKER, 11 MAJOR) — both "do not build as filed." (Opus's first call died at ~272 s on an upstream disconnect, the duration cutoff seen in v2's checks; the retry completed in ~264 s and is the review of record.)
- **Adjudication** (`../design/ADJUDICATION.md`): convergences C1–C10, single-checker items, and four disagreements resolved (alternating ladders over block ladders; C2 reference runs adopted; CLASSIFY routing kept with exploratory label + smoke + regression reporting; unload-all warm-state step rejected as production-service manipulation). DESIGN.md amended pre-build (A1–A16), including the correction of the design's own false safety sentence (Astra #1 — verified against the attempt-level verdict trajectories) and the v1/v6 gold audit (A15: both golds re-derived and confirmed).
- **Build:** `~/fleet-bus-ab3/code/` (workspace masters in `../code/`). `fleetbus2.py` carries exactly one additive, default-off parameter (`verdict(..., force_deadletter=False)`; diff vs v2's core = 2 hunks). `arm_c3.py` = `arm_c2.py` + kind-aware alternating `model_for_attempt` + checker early-DLQ (verdict-history comparison, early_dlq.jsonl, DLQ flag). `run_ab3.py` = `run_ab2.py` with B/C2 paths verbatim + C3 arm + reference channels. Workload byte-identical to v1/v2 (md5 f196c417… on-box, both articles).
- **Mechanics gate v3 — PASS (all 10 legs)**, Nov 14, 2026: regression (v2 gate re-run against the modified core) · routing/full ladder (model sequences exactly as filed; no early DLQ on varying reasons) · early-DLQ fires (attempt 2, cross-model pair, exactly one DEADLETTER event) · near-equal sets don't fire · nonconsecutive repeats don't fire · canonicalization (reordered/duplicated sets fire; subsets don't) · transport exclusion (2 error attempts, 1 verdict row, pass at attempt 3) · late-result fencing (late post recorded, no resurrection, no MERGE) · co-residency pre-flight · real-model smoke (held-out items: format clean 9/9; gold agreement 8/9 — the SEASONAL classify item missed on content, format fine). Evidence: `metrics/gate-results3.json`, `metrics/gate-results2.json` (regression), `metrics/gate-c3.out`.

## Interventions log

None so far. (The pre-registered kill tests are filed interventions-exempt per A12.)

## Run entries

### B run 1 (kill test) — SCORED, complete
- **Fairness at launch:** pre-probe load l1 1.39 (l5 2.76); dual probe **4b DRAFT 85.8 s · 8b VERIFY 1.6 s** (both < 240 s); post-probe l1 15.26 (< 30). Tenancy: none (Tranche B units verified inactive; box exclusive). Residency at launch: 8b fully VRAM-resident (13,488,692,917 B); GPUs bus 05 5,095 / 06 5,794 / 41 4,470 MiB.
- **Calibration:** 4b 98.4 s / 825 eval / 8.38 tok/s (CPU-heavy placement).
- **Kill test:** after the 6th completion, worker b2 SIGKILLed holding v1 → recovered by the file queue's stale-claim path, **latency 634.2 s**.
- **Result:** 18/18 done, lost 0, duplicated 0, **shipped-wrong 4 (c3, d2, v1, v6)**, correct 14, wall **2,226.6 s**, work **20,022 tokens / 18 calls**, failed calls 0, coord tokens 0, budget-burned calls in metrics. Load trace (60 s samples, n=38): l1 mean 20.1 / max 22.4 — the run's own CPU work on an exclusive box. **tok/error-free job 1,430.1.**
- Evidence copied off-box: `metrics/B-run1-metrics.json`, `metrics/B-run1-call_log.jsonl`.

### C2 run 1 — REFERENCE (kill test) — launched
- **Fairness at launch:** pre-probe load l1 3.33; dual probe **4b DRAFT 200.6 s · 8b VERIFY 9.5 s** (both < 240 s — the 4b probe is slow because the 4b runner is mostly CPU-resident: `/api/ps` size_vram 1,256,194,048 B; the 8b is fully VRAM-resident at 13,488,692,917 B; service placement, not manipulated). Tenancy: none. GPUs at launch: bus 05 5,096 / 06 5,794 / 41 4,468 MiB.
- **Calibration:** 8b 6.8 s / 124 eval / **18.15 tok/s** (fully GPU-resident) · 4b 168.8 s / 1,388 eval / 8.22 tok/s (CPU-heavy).
- **Kill test:** worker c3 SIGKILLed holding v1 → recovered via lease expiry + reaper; v1 then climbed the full ladder to dead-letter; kill→terminal latency **770.8 s** (includes the ladder climb — the killed task was v1 itself).
- **Result:** 16 done + 2 DLQ (v1, v6) = 18/18 accounted, lost 0, duplicated 0, shipped-wrong 0, correct 16, wall **2,628.9 s**, work **24,623 tokens / 26 calls** (4b 23,841 · 8b 782), failed calls 0, coord 0, DLQ priced **5,947 tokens**, mirror 124/124 events 0 errors (channel fleet-bus-v3-c2ref-run1), leak-flagged attempts **0** (the 4b's failures this run were verdict-content failures on parseable artifacts, not structural truncations). Load trace l1 mean 20.5 / max 22.3 (exclusive box). **tok/error-free job 1,538.9.**
- Evidence copied off-box: `metrics/C2ref-run1-metrics.json`, `metrics/C2ref-run1-call_log.jsonl`, `metrics/C2ref-run1-verdicts.jsonl`.
- **Regime note (for the analysis):** even with the box exclusive, this reference run's wall (2,628.9 s) sits between v2's two C2 walls (2,358.1 / 3,108.9) — the dominant regime variable is the 4b runner's placement (CPU-heavy at 8.22 tok/s calibration here vs GPU-resident 10.89–12.77 in v2's evening runs), not co-tenancy alone. This is exactly why A4 re-referenced the yardstick to same-regime C2 runs.

### C3 run 1 (kill test) — launched
- **Fairness at launch:** pre-probe load l1 0.18; dual probe **4b DRAFT 88.1 s · 8b VERIFY 1.0 s** (both < 240 s). Tenancy: none. Residency: 8b fully VRAM-resident (13,488,692,917 B), 4b mostly CPU-resident (1,256,194,048 B VRAM) — identical placement to the C2 reference run 1 launch. GPUs: bus 05 5,099 / 06 5,794 / 41 4,472 MiB.
- **Calibration:** 8b 6.2 s / 124 eval / 20.12 tok/s · 4b 81.1 s / 681 eval / 8.40 tok/s.
- **Kill test:** worker c2 SIGKILLed holding d1 → recovered via lease expiry + reaper, **latency 214.2 s** (fastest of the three run-1 kills).
- **Result:** 16 done + 2 DLQ (v1, v6) = 18/18 accounted, lost 0, duplicated 0, shipped-wrong 0, checker defects 0, correct 16, wall **1,313.5 s**, work **14,119 tokens / 24 calls** (8b 2,499/16 calls · 4b 11,620/8 calls), failed calls 0, coord 0, mirror 116/116 events 0 errors (channel fleet-bus-v3-c3-run1). Load trace l1 mean 20.3 / max 21.8. **tok/error-free job 882.4.**
- **Early-DLQ fired as designed:** v1 deadlettered at **attempt 2** — the 8b (a1) and 4b (a2) independently returned {WRONG_VERDICT_3}; DLQ record flagged `early_dlq: true`. v6 climbed the full ladder (its failure sets varied) and priced accordingly; total DLQ price 5,769 tokens. One leak-flagged attempt (v6 a2, a 4b rung) — the leak persists on 4b rungs; routing reduced exposure rather than eliminating it.
- Evidence copied off-box: `metrics/C3-run1-metrics.json`, `metrics/C3-run1-call_log.jsonl`, `metrics/C3-run1-verdicts.jsonl`.
- **Run-1 set standings (context, not a verdict):** wall — C3 1,313.5 < B 2,226.6 < C2ref 2,628.9 · tok/efj — C3 882.4 < B 1,430.1 < C2ref 1,538.9 · correct — C3 16 = C2ref 16 > B 14.

### C3 run 2 — launched
- **Fairness at launch:** pre-probe load l1 7.35; dual probe **4b DRAFT 201.7 s · 8b VERIFY 1.1 s** (both < 240 s). Tenancy: none. No kill test (run 2).
- **Calibration:** 8b 6.2 s / 124 / 20.03 tok/s · 4b 196.8 s / 1,600 eval (full-cap draw) / 8.13 tok/s.
- **Result:** 16 done + 2 DLQ (v1, v6) = 18/18 accounted, lost 0, duplicated 0, shipped-wrong 0, checker defects 0, correct 16, wall **1,583.8 s**, work **16,035 tokens / 24 calls** (8b 1,938/14 · 4b 14,097/10), failed calls 0, coord 0, mirror 114/114 events 0 errors (channel fleet-bus-v3-c3-run2). Load trace l1 mean 20.8 / max 22.2. **tok/error-free job 1,002.2.**
- **Early-DLQ fired identically:** v1 at attempt 2, {WRONG_VERDICT_3} — the signature replicated across both C3 runs. DLQ price again **5,769 tokens** (not a copy error: VERIFY prompt sizes are fixed and failed 4b attempts burn exactly 1,600 eval while 8b attempts burn exactly 15, so the same failure trajectories price identically). One leak-flagged attempt (d2 a1, a DRAFT 4b opener; d2 completed via the ladder).
- Evidence copied off-box: `metrics/C3-run2-metrics.json`, `metrics/C3-run2-call_log.jsonl`, `metrics/C3-run2-verdicts.jsonl`.
- **C3 aggregate (both runs):** wall 2,897.3 s · tokens 30,154 · correct 32 · DLQ 4 (2 per run — aggregate exactly at the leg-4 cap of 4) · shipped-wrong 0 · tok/efj 942.3.

### C2 run 2 — REFERENCE — launched
- **Fairness at launch:** pre-probe load l1 5.92; dual probe **4b DRAFT 200.2 s · 8b VERIFY 1.0 s** (both < 240 s). Tenancy: none. No kill test (run 2).
- **Calibration:** 8b 5.1 s / 102 / 19.89 tok/s · 4b 84.0 s / 708 / 8.43 tok/s.
- **Result:** 16 done + 2 DLQ (v1, v6) = 18/18 accounted, lost 0, duplicated 0, shipped-wrong 0, correct 16, wall **3,163.5 s**, work **29,557 tokens / 28 calls** (4b 28,557 · 8b 1,000), failed calls 0, coord 0, DLQ priced **7,704 tokens**, mirror 130/130 events 0 errors (channel fleet-bus-v3-c2ref-run2). Load trace l1 mean 20.4 / max 21.8. **tok/error-free job 1,847.3.** Two leak-flagged attempts (v6 a1, d2 a2 — both 4b rungs).
- Evidence copied off-box: `metrics/C2ref-run2-metrics.json`, `metrics/C2ref-run2-call_log.jsonl`, `metrics/C2ref-run2-verdicts.jsonl`.
- **C2 reference aggregate (both runs, this regime):** wall 5,792.4 s · tokens 54,180 · correct 32 · DLQ 4 · shipped-wrong 0 · **tok/efj 1,693.1**. (V2's filed C2 aggregate in its co-tenant regime was wall 5,467.0 / tok/efj 1,645.2 / correct 33 — reported as historical context only; the yardstick reads from this same-regime reference.)

### B run 2 — launched
- **Fairness at launch:** pre-probe load l1 12.17; dual probe **4b DRAFT 200.3 s · 8b VERIFY 1.0 s** (both < 240 s). Tenancy: none. No kill test (run 2).
- **Calibration:** 4b 194.8 s / 1,600 eval (full-cap draw) / 8.21 tok/s.
- **Result:** 18/18 done, lost 0, **shipped-wrong 4 (d1, d6, v1, v6)**, correct 14, wall **2,466.8 s**, work **22,321 tokens / 18 calls**, failed calls 0, coord 0. Load trace l1 mean 21.0 / max 22.6. **tok/error-free job 1,594.4.**
- Evidence copied off-box: `metrics/B-run2-metrics.json`, `metrics/B-run2-call_log.jsonl`.
- **Fresh B aggregate (the bar's comparator):** wall 4,693.4 s · tokens 42,343 · correct 28 · shipped-wrong 8 · tok/efj 1,512.2.

## Scorecard outcome (main test)

**Win bar: CLEARED, 8/8 legs** (C3 wall ratio 0.617 vs the 1.25 cap; shipped-wrong 0 vs B's 8; DLQ 4 = the cap; full scorecard in RESULTS.md §3). **Yardstick: all five conditions pass** vs the C2 reference (tok/efj 942.3 vs 1,693.1, −44.3%; class yields identical 12/12/8). Per the filed loop rule this is a **win** — subject to the A10 confirmation below before the adoption packet is finalized.

## Confirmation A/B (A10) — fresh workload, same 8 legs

- **Article:** `~/fleet-bus-ab3-confirm/` — code identical to the main article except `run_ab3.py` seeds {1: 20261115, 2: 20261116} and confirm mirror-channel names, and `workload.json` = the fresh confirmation workload (`../confirm/workload-confirm.json`, 18 new tasks nc/nd/nv, gold mechanically derived and self-checked). Order: B run 1 (kill) → C3 run 1 (kill) → C3 run 2 → B run 2. Same fairness protocol (dual probe on nd1/nv1).

### Confirmation B run 1 (kill test) — launched
- **Fairness at launch:** pre-probe load l1 0.64; dual probe **4b DRAFT (nd1) 197.5 s · 8b VERIFY (nv1) 11.5 s** (both < 240 s). Tenancy: none.
- **Calibration:** 4b 105.3 s / 892 eval / 8.47 tok/s.
- **Kill test:** worker b3 SIGKILLed holding nd3 → recovered via the stale-claim path, **latency 446.1 s**.
- **Result:** 18/18 done, lost 0, **shipped-wrong 5 (nc3, nd2, nd4, nv2, nv3)** — including both designed trap items (nv2 the after-11-PM edge, nv3 the comparative) — correct 13, wall **2,340.6 s**, work **21,283 tokens / 18 calls**, failed calls 0, coord 0. **tok/error-free job 1,637.2.**
- Evidence copied off-box: `metrics/CONF-B-run1-metrics.json`, `metrics/CONF-B-run1-call_log.jsonl`.

### Confirmation C3 run 1 (kill test) — launched
- **Fairness at launch:** pre-probe load l1 3.45; dual probe **4b DRAFT (nd1) 203.3 s · 8b VERIFY (nv1) 11.3 s** (both < 240 s). Tenancy: none.
- **Calibration:** 8b 5.4 s / 94 eval / 17.57 tok/s · 4b 194.9 s / 1,600 eval (full-cap) / 8.21 tok/s.
- **Kill test:** worker c2 SIGKILLed holding nd1 → recovered via lease expiry + reaper, **latency 204.2 s**.
- **Result:** 16 done + 2 DLQ (nc3, nv2) = 18/18 accounted, lost 0, duplicated 0, shipped-wrong 0, correct 16, wall **1,842.1 s**, work **18,978 tokens / 28 calls**, failed calls 0, coord 0, DLQ priced **5,566 tokens**, mirror 132/132 events 0 errors (channel fleet-bus-v3-confirm-c3-run1). **tok/error-free job 1,186.1.**
- **Early-DLQ fired on nc3** at attempt 2 ({WRONG_OR_MULTI_LABEL} — both models mislabeled the graphic-novel title identically; B shipped nc3 wrong). Per A13 this is recorded as a **CLASSIFY routing regression** (the 8b opener missed the item) — with the system's outcome noted alongside: the gate converted B's shipped-wrong into a surfaced abstention. The other DLQ, nv2 (the after-11-PM edge), is the confirmation set's v6-analog. Three of B run 1's five shipped-wrong tasks (nd2, nd4, nv3 — including the comparative trap) were delivered **correct** by the ladder in this run.
- Evidence copied off-box: `metrics/CONF-C3-run1-metrics.json`, `metrics/CONF-C3-run1-call_log.jsonl`, `metrics/CONF-C3-run1-verdicts.jsonl`.

### Confirmation C3 run 2 — launched
- **Fairness at launch:** pre-probe load l1 7.61; dual probe **4b DRAFT (nd1) 199.2 s · 8b VERIFY (nv1) 1.0 s** (both < 240 s). Tenancy: none. No kill test (run 2).
- **Result:** 16 done + 2 DLQ (nv2, nv3) = 18/18 accounted, lost 0, shipped-wrong 0, correct 16, wall **1,643.9 s**, work **16,910 tokens / 26 calls**, failed calls 0, coord 0, DLQ priced **7,628 tokens**, mirror 122/122 events 0 errors (channel fleet-bus-v3-confirm-c3-run2). **tok/error-free job 1,056.9.** No early-DLQ this run (failure sets varied); nc3 — run 1's early-DLQ — passed here, and nv3 — run 1's ladder save — deadlettered here: the hard-item outcomes are draw-dependent at the margin, the system's accounting is not.
- Evidence copied off-box: `metrics/CONF-C3-run2-metrics.json`, `metrics/CONF-C3-run2-call_log.jsonl`, `metrics/CONF-C3-run2-verdicts.jsonl`.
- **C3 confirmation aggregate so far:** wall 3,486.0 s · tokens 35,888 · correct 32 · DLQ 4 · shipped-wrong 0 · tok/efj 1,121.5.

### Confirmation B run 2 — launched
- **Fairness at launch:** pre-probe load l1 0.40; dual probe **4b DRAFT (nd1) 107.9 s · 8b VERIFY (nv1) 1.1 s** (both < 240 s). Tenancy: none. No kill test (run 2).
- **Calibration:** 4b 195.5 s / 1,600 eval (full-cap) / 8.19 tok/s.
- **Result:** 18/18 done, lost 0, **shipped-wrong 3 (nd2, nv2, nv3)**, correct 15, wall **2,344.7 s**, work **21,245 tokens / 18 calls**, failed calls 0, coord 0. **tok/error-free job 1,416.3.**
- Evidence copied off-box: `metrics/CONF-B-run2-metrics.json`, `metrics/CONF-B-run2-call_log.jsonl`.
- **Confirmation B aggregate:** wall 4,685.3 s · tokens 42,528 · correct 28 · shipped-wrong 8 · tok/efj 1,518.9 (within ~1% of the main test's B aggregate on every axis — the fresh set is difficulty-matched).

## Confirmation scorecard (A10)

**CLEARED — 8/8 legs** (full record: `CONFIRMATION.md`). C3 aggregates: wall 3,486.0 (ratio **0.744** vs the 1.25 cap) · tokens 35,888 · correct 32 · DLQ 4 (= cap; 2 + 2) · shipped-wrong 0 · tok/efj **1,121.5** vs B's 1,518.9. Per-class correct: C3 CLASSIFY 11 / DRAFT 12 / VERIFY 9 vs B 11 / 9 / 8. One pre-registered A13 routing regression recorded (nc3 CLASSIFY early-DLQ in run 1; the item passed in run 2 and was shipped wrong by B in run 1).

## Program close

The iterate-until-working loop terminates under its filed rule: **v3 cleared the pre-filed win bar (8/8) on the tuning set and passed the fresh-workload confirmation (8/8)**. No v4 is commissioned. Deliverables: `RESULTS.md`, `CONFIRMATION.md`, `ADOPTION-PACKET.md`, this ledger, `analysis.py`, and all run metrics/call logs/verdicts in `metrics/`. Adoption/deployment remains Joe's ruling.
