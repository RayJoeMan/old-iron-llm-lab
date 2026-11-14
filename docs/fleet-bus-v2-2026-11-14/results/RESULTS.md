# Fleet Bus v2 — A/B Results (PARTIAL — runs deferred by environment)

**Filed:** Nov 14, 2026, by the v2 coordinator. Design: `design/DESIGN.md` (filed before any run). Independent checks: `design/OPUS-CHECK.md`, `design/ASTRA-CHECK.md`; adjudication: `design/ADJUDICATION.md` (29 substantive issues: 15 caught by both checkers, 6 Astra-only, 8 Opus-only; 20 fixed in code before any run, 7 carried as disclosed amendments A-1…A-5). Build/run record: `results/RUN-LEDGER.md`. Metrics: `results/metrics/`.

## Verdict, up front

**The v2 win bar is NOT EVALUATED.** The filed comparison requires 2 runs per arm; exactly **one** run completed validly (arm B run 1, the control). All three C2 run-1 attempts were stopped by the coordinator for the same measured environment failure, and the remaining runs (C2 run 1, C2 run 2, B run 2) are **deferred to the window specified below** per the commission's explicit fallback — report honestly rather than rush distorted runs. No win-bar leg is scored on a single arm, and this file claims no winner.

What the partial record does establish is listed in §2, including the control-side evidence for the design's central thesis. Adoption remains Joe's ruling; the completion report (`~/workspace/fleet-watchman/reports/fleet-bus-v2.md`) carries the recommendation.

## 1. Run inventory

| Run | Status | Numbers used? |
|---|---|---|
| B run 1 | **Complete + valid** | Yes (§2.2) |
| C2 run 1, attempt 1 | Deferred before launch (load spiked to 41+ during calibration; no workers, no ledger) | No |
| C2 run 1, attempt 2 | Aborted minutes in (4b endpoint wedged; 3 claimed / 15 queued / 0 terminal) | No |
| C2 run 1, attempt 3 | Aborted ~10 min in (first scored worker call timed out at 600 s; 6 claimed / 12 queued / 0 terminal) | No |
| C2 run 1 (scored), C2 run 2, B run 2 | **Deferred** — window conditions not met today | — |

All attempts preserved on-box under `~/fleet-bus-ab2/runs/` (`.bak-*` dirs). Full narrative with timestamps: RUN-LEDGER.md.

## 2. What the partial record establishes

### 2.1 Mechanics gate — PASS (before any scored run, on the post-check-fix code)

`gate_c2.py` on Fortress, `gate_pass: true` (metrics/gate-results2.json):

| Leg | Result |
|---|---|
| 1. Flood 1,000 tasks | 1,000 done, **0 duplicate claim attempts**, 1,000 merges, 15.7 s |
| 2. Duplicate-enqueue storm | exactly 18 tasks, both enqueuers exit 0 |
| 3. SIGKILL / restart / reap | in-progress at kill confirmed; 100 done, 0 deadletters, 0 duplicate merges, 1 reap exercised |
| 4. Reconciliation | JSONL replay == ledger on the flood DB **and** the policy DB |
| 5. **Policy ladder (new in v2)** | 6 always-fail tasks × exactly 4 attempts = 24 result rows, 18 FAIL_REQUEUE, 6 DEADLETTER — the escalation ladder + dead-letter path exercised end-to-end |

The ledger core (claims + leases + heartbeats + idempotency + reaper) is byte-identical to v1 except the filed 7-line `dead`→`deadletter` transformation (diff in RUN-LEDGER.md). v1's core never failed; v2's regression gate says it still doesn't, and leg 5 closes the gap Opus's check flagged (v1's gate never exercised the changed policy path).

### 2.2 Arm B run 1 (control) — the incumbent, measured

- **18/18 done, 0 lost, 0 duplicated.** Wall **1,746.5 s**. Work 20,980 tokens / 18 logged calls, failed_calls 0, coordination-generation tokens 0. Kill test: worker b1 SIGKILLed holding task v2 → recovered, latency 300.1 s.
- **Shipped-wrong = 4 of 18: d4, d5, d6, v1** — delivered artifacts that fail the shared validator, shipped as completed work. First-attempt validator pass 14/18. (Validator-relative, per amendment A-5: read "validator-wrong" where precision matters.)
- **The gate-caught counterfactual, on the record:** task **v1** is one of the four. In the v1 A/B, the bus spent 3 generations refusing this task's wrong answers and then *lost* it at the attempt cap; the file queue simply delivered the wrong answer and counted the task a success. Under v2's policy, all four of these tasks would have climbed the ladder (qwen3:4b → qwen3:8b rungs) and either validated or landed in the dead-letter queue with a full attempt history — never silently shipped. This is the design's thesis demonstrated on the control arm. The C2 arm's own numbers on these same task IDs remain unmeasured.
- Accounting note (adjudication #16, occurring live): the killed in-flight v2 generation never reached the call log, so real generations = **19**, logged = 18. `budget_burned_calls = 6` (call-level context per amendment A-1; the per-attempt leak metric is C2-only by design and the two are never compared head-to-head).
- Conditions: started at pre-load l1 4.49; the load trace heated to l1 26→55 across the run (lane-b tranche + Gemma trial). Calibration qwen3:4b = **10.21 tok/s** (GPU-resident runner, 7.2 GB VRAM). These are contention walls, reported as such.

### 2.3 SwarmChat as durable log — performed flawlessly in every live start

Across C2 attempts 2 and 3, the mirror posted **45/45 ledger events (21/21 and 24/24), 0 errors, 0 generations, 0 arbitration** — per-run channels `fleet-bus-v2-c2-run1` on the Python-3.12-pinned SwarmChat server. The v2 role for SwarmChat (durable log only) is the one component validated end-to-end under real run conditions today.

### 2.4 The environment failure — measured, not anecdotal

- The production Ollama **qwen3:4b runner was mostly CPU-resident (1.26 GB VRAM)** during the C2 attempts vs **7.2 GB GPU-resident** during B run 1. Runner placement is decided by the production service at load time under VRAM pressure — outside the test article's control and outside this commission's scope to change.
- Tenancy at attempt time: Gemma trial CPU llama-server ≈1053% CPU, lane-b ≈651%, sustained load 45–58 (box = 40 threads). A leaked 1,600-token 4b generation cannot clear the 600 s HTTP cap in that regime.
- Cascade mechanism (observed in attempt 3's own accounting): a client timeout leaves a server-side "zombie" generation that keeps the runner busy; queued calls slow, time out in turn, and stack more zombies. Worker c1's first scored call (task 1) timed out at 600 s — adjudication issue #25's transport-error failure mode, live.
- Decisive probe (~10:46 CT): after the runner's keep-alive expired and it reloaded **fully GPU-resident (7,220,326,563 bytes VRAM — identical to B run 1's placement)**, a single DRAFT generation through the exact worker path (`workgen2.run_work`, task d1) **still timed out at 600.1 s** (load 31–36; bus-05 GPU at 74–93% util under another tenant earlier). GPU residency is necessary but not sufficient under current tenancy.

## 3. Win-bar scorecard (filed §9 — all legs require the full run set)

| Leg | Status |
|---|---|
| 1. Hard gate: C2 lost=0 + duplicated=0 per run | **Not evaluated** (no scored C2 run) |
| 2. Accounted delivery C2 ≥ B | Not evaluated (B run-1 side: 18/18 accounted) |
| 3. Shipped-wrong C2 < B | Not evaluated (B aggregate so far: 4, from one run; the filed aggregate is over 2 runs) |
| 4. DLQ cap (≤4/36, ≤3/run) | Not evaluated (ladder+DLQ proven synthetically, gate leg 5) |
| 5. Wall C2 ≤ 1.25× B | Not evaluated (B run-1 side: 1,746.5 s) |
| 6. Coordination-generation tokens C2 = 0 | **Structurally verified** (no such code path exists; both checkers confirmed; mirror = 0 generations in live starts) — formal scoring awaits scored runs |
| 7. Interventions C2 ≤ B | Not evaluated (B run 1: 0 in-run interventions. The C2 aborts/deferrals are coordinator actions on unscored attempts, logged in RUN-LEDGER.md, and are not in-run interventions of a scored run) |
| 8. Mechanics gate | **PASS** (§2.1) |

Split result = fail under the filed rules; an incomplete run set is reported as incomplete, not as a split.

## 4. Run window for completion (whoever picks this up)

Launch the three remaining runs, in the filed counterbalanced order — **C2 run 1 (`--kill-test`), C2 run 2, B run 2** — only when **both** measure true immediately before launch:

1. 1-min load < 30 (the orchestrator's own defer guard also enforces this at start; do not bypass it), and
2. a DRAFT-prompt qwen3:4b probe through `workgen2.run_work` (any DRAFT task, 1,600-token budget) completes in < 240 s.

Command form: `cd ~/fleet-bus-ab2/code && setsid nohup python3 run_ab2.py --arm <ARM> --run <N> --base ~/fleet-bus-ab2 [--kill-test] > ~/fleet-bus-ab2/runs/<ARM>-run<N>-orch.out 2>&1 &` (run 1 of each arm takes `--kill-test`; the harness refuses C2 unless gate-results2.json shows pass, and renames a pre-existing run dir to `.bak-<ts>`). Copy each `metrics.json` off-box after each run. Then complete §3's scorecard and the DLQ pricing / per-task token tables from the metrics files. Natural window candidates: after the Gemma trial and the lane-b tranche wind down, or an early-morning slot before the fleet's day work starts.

## 5. Disclosed asymmetries (carried from ADJUDICATION.md, amendments A-1…A-5)

- B's per-attempt leak metric is call-level context only (`budget_burned_calls`); C2's is per-attempt. Never compared head-to-head.
- Lease expiry is reaper-mediated in both bus versions (v1 semantics retained) — deadletter-by-lease arrives via the reaper's DEADLETTER_LEASE path.
- "First attempt" = first validated/delivered artifact (v1-comparable naming).
- B delivery fencing / same-worker overwrite undercounts B duplication (pro-B bias); verdict fencing is single-checker-safe only (fine for this A/B, a production caveat); transport errors consume C2 attempts but not B's (anti-C2 under infrastructure failure — the exact effect §2.4 documents); settle-window completions may land after a wall endpoint (negligible, both arms); shipped-wrong is validator-relative and symmetric across arms.
- Arm A (SwarmChat arbitration) did not re-run: v1 settled the structural question (79,601 coordination tokens ≈ 2.5× the work; both runs hit the 60-min cap). v2 re-scopes SwarmChat to the durable-log role measured in §2.3.
