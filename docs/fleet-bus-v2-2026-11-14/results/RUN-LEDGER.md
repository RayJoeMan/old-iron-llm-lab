# Fleet Bus v2 — Run Ledger

**Design:** `../design/DESIGN.md` (pre-registered, filed Nov 14, 2026 before build). **Checks:** `../design/OPUS-CHECK.md` (Claude Opus 5.5) + `../design/ASTRA-CHECK.md` (GPT-6 Astra) — two independent, mutually blind checks of the identical design+code packet, per Joe's Nov 14 amendment; adjudication in `../design/ADJUDICATION.md`. **Commissioned:** Joe, Nov 14, 2026. **V1 record:** `~/workspace/your_files/fleet-bus-ab-2026-11-13/`.

## Inventory (step 1 of the commission)

V1 workspace masters verified byte-identical to the on-box test article before any v2 work: `fleetbus.py` sha256 c2985494b360f8b3a002fc45addbe6a063e9c2002b3f78c0369aa488c8b0fffb and `workload.json` sha256 e8e3748b1e2f8d69d1e077a59c8196cf48ec9596a80e4e970c9e5a9d81268920 match on both sides. On-box `~/fleet-bus-ab/` intact (code/, runs/, swarmchat-venv — Python 3.12.16 — tokens/ 0600). V2 lives separately at `~/fleet-bus-ab2/`; v1's article is untouched.

Environment at design time (Nov 14, ~08:13 CT): Fortress load ≈ 14 (co-tenant: the Gemma trial's 12-thread CPU-only lane); GPUs idle; system Ollama serves both ladder models (`qwen3:4b`, `qwen3:8b` present in /api/tags). The SwarmChat server is already running the infra-buildout coordinator's Python 3.12 pin (`/home/swarmops/venvs/swarmchat312/bin/python3.12 … serve`, started 08:10 CT) — v2 consumes the pin as designed; no pin work done here.

## Build record (Nov 14, 2026)

Built by the coordinator (Nyx) directly; the two frontier checks serve as the independent-checker stage of Joe's build pattern.

| Piece | Basis | Change vs v1 |
|---|---|---|
| `fleetbus2.py` | v1 `fleetbus.py`, scripted transform | **7 lines**: terminal-failure state `dead` → `deadletter` in `verdict()` + `reap()` (+ event names, counts list). Full diff below. Claim/lease/heartbeat/idempotency/reaper mechanics byte-identical. |
| `workgen2.py` | v1 `workgen.py`, scripted transform | Model parameterized (default = v1's qwen3:4b, so rung-1 request bodies are byte-identical); call-log entries gain `model`/`task`/`attempt` on success and error paths. |
| `workgen.py` | new | Compatibility shim re-exporting workgen2 so v1's `arm_b.py` runs byte-unmodified (DESIGN §6.4). |
| `arm_c2.py` | v1 `arm_c.py`, adapted | Worker picks the model by ladder rung (attempt ≤2 cheap, ≥3 strong) and tags generations with task+attempt; checker logs **every** verdict (`verdicts.jsonl`) in addition to v1's first-verdicts file and writes dead-letter records on deadletter transitions; reaper writes dead-letter records for lease-expiry deadletters. Shared `write_deadletter()` builder (idempotent). |
| `mirror.py` | new | Tails the ledger events table (read-only), posts each event to the run's fresh SwarmChat channel as pilot-admin via the pinned 3.12 client; best-effort with retry-on-next-poll; writes `mirror_metrics.json` (posted/total/errors/lag). Zero generations, zero arbitration. |
| `gate_c2.py` | v1 `gate_c.py`, scripted transform | Same four legs against fleetbus2; replay map gains the DEADLETTER transitions; leg 3 terminal = done+deadletter. |
| `run_ab2.py` | v1 `run_ab.py`, adapted | Arms B/C2 only; per-run load trace + pre-load snapshot; unscored calibration generation per model before t0 (separate log, never in arm metrics); C2 setup enqueues with max_attempts=4 and creates the mirror channel; kill victim pool = workers only; collect adds shipped-wrong re-scoring for **both** arms, deadletter records, leak flags (C2 per-attempt; B call-level — B's harness predates per-task tagging, disclosed), work tokens by model, mirror metrics. |
| `arm_b.py`, `validators.py`, `workload.json`, `arm_a.py` | v1 copies | Byte-identical (arm_a.py carried for reference; not imported by the v2 harness). |

### fleetbus.py → fleetbus2.py diff (the "mechanics untouched" evidence)

```
399c399            state = 'dead'            -> 'deadletter'        (verdict, SQL)
408,409c408,409    event "DEAD" -> "DEADLETTER"; return "dead" -> "deadletter"
454c454            state = 'dead'            -> 'deadletter'        (reap, SQL)
459c459            event "DEAD_LEASE"        -> "DEADLETTER_LEASE"
465c465            actions "dead"            -> "deadletter"
470c470            counts list "dead"        -> "deadletter"
```
7 changed lines, all in the terminal-failure naming. Nothing else differs.

## Checker findings and dispositions

Two independent, mutually blind checks of the identical packet (filed DESIGN.md + all v2 code, ~100 KB), per Joe's Nov 14 amendment: **Claude Opus 5.5** (`../design/OPUS-CHECK.md` — 39,230 in / 26,105 out tokens; two earlier attempts at a 64K cap dropped at ~271 s on an upstream duration cutoff, the successful call ran at a 32,768 cap in 258 s) and **GPT-6 Astra** (`../design/ASTRA-CHECK.md` — 24,247 in / 5,924 out, 137 s). Full adjudication with the issue-by-issue tally: `../design/ADJUDICATION.md`.

**Tally:** 29 substantive issues — 15 caught by both, 6 Astra-only, 8 Opus-only. Three disagreements adjudicated with reasons (probe double-count: Opus correct, the sums are disjoint by construction; verdict-fencing severity: LOW for this single-checker A/B, HIGH for any production adoption; validators: symmetric across arms *and* permissive absolutely — shipped-wrong stays a validator-relative metric). One Opus query (post_result's attempt parameter) verified a non-issue against the 7-line fleetbus diff. The single most valuable catch was Opus-only: **the mechanics gate as inherited never exercised the code v2 changed** (sim checkers always passed; gate used max_attempts=3; reconciliation replayed only the happy-path log).

**Dispositions:** 20 fixed in code before any run (token via env + sanitized errors; mechanical load-defer guard; kill victim by claim age + mandatory run-1 kill; DLQ reconcile pass + enriched DLQ records; checker VALIDATOR_ERROR verdicts instead of livelock; collect fails loudly on malformed/missing call logs; B shipped-wrong restricted to delivered tasks + done-without-artifact counted; C2 shipped-wrong sha-verified; late-row dup rule; gate leg 3 SIGKILL + exercised-recovery assertions, leg 2 exit codes, **new gate leg 5 (policy ladder)** + reconciliation over the policy DB; mirror SIGTERM metrics + state fallback; per-task token/DLQ pricing in metrics). 7 disclosed as amendments A-1…A-5 in the adjudication (B leak accounting, reaper-mediated lease semantics, first-attempt definition, §4.4→§4.3 pointer, and the known-limitations set with bias directions). Files changed by the fixes: `mirror.py`, `arm_c2.py`, `run_ab2.py`, `gate_c2.py`. `fleetbus2.py` itself was **not** changed by either check — the ledger core stands as transformed. Local smoke after fixes: ladder climbs 4 attempts → deadletter, DLQ record complete (verified in a temp dir before transfer).

## Mechanics gate (C2) — PASS (required before A/B numbers count)

Run on Fortress, Nov 14, 2026, against the post-fix code (`gate-results2.json` in the code dir, all five legs):

| Leg | Result |
|---|---|
| 1. Claim flood: 1,000 NOOP tasks, 6 workers + 2 checkers | **PASS** — 1,000 done, 0 duplicate claim attempts, 1,000 merges, 15.7 s |
| 2. Duplicate-enqueue storm (18-task batch × 2 processes) | **PASS** — exactly 18 tasks, both enqueuers exit 0 |
| 3. Kill/restart (SIGKILL reaper + worker mid-run, 100 tasks) | **PASS** — in-progress at kill, 100 done, 0 deadletters, 0 dup merges, **1 reap exercised** |
| 4. Reconciliation (JSONL replay vs ledger) | **PASS** — exact on the flood DB *and* the policy DB (the DEADLETTER/FAIL_REQUEUE transitions replay correctly) |
| 5. Policy ladder (always-fail checker, max_attempts=4) | **PASS** — 6 tasks × exactly 4 attempts, 24 result rows, 18 FAIL_REQUEUE, 6 DEADLETTER, all terminal deadletter |

## A/B runs

### Arm B run 1 — COMPLETE (valid)

Wall 1,746.5 s. 18/18 done, lost 0, duplicated 0. Validator first-attempt 14/18. **Shipped-wrong 4: d4, d5, d6, v1** — the incumbent delivered four validator-failing artifacts as completed work, v1 among them (the same task the v1 bus died refusing). Kill test: victim b1 holding v2 → recovered, 300.1 s. Work 20,980 tokens / 18 logged calls (the killed in-flight generation never reached the log — the adjudication #16 uncountable case, occurring live; real generations = 19). Budget-burned calls 6 (context, amendment A-1). Conditions: calibration qwen3:4b 10.21 tok/s; run started at load ~5–14, load trace 26→55 as lane-b's CPU lane and the Gemma trial heated the box — a contention wall, reported as such.

### Arm C2 run 1, attempt 2 — ABORTED minutes in (harness/environment failure; discarded, preserved)

The relaunch passed the defer guard (≈25.8) and calibrated: qwen3:8b clean (9.4 s, 10.96 tok/s, 103 eval tokens — no leak). The **qwen3:4b calibration generation then timed out at the 600 s HTTP limit** — the same call that took 95.4 s during B run 1. The run launched regardless (calibration errors are recorded, not fatal, by design), but a coordinator probe immediately after — a 50-token 4b generation — also failed to return within 120 s: **the 4b endpoint was effectively wedged** (its runner showed 1.26 GB VRAM vs 7.2 GB when healthy; load 53–56 from lane-b + the Gemma trial; a server-side zombie generation from the timed-out calibration cannot be excluded). Under the filed systems, C2's workers would have burned attempts on 600 s transport timeouts — adjudication issue #25's failure mode, measuring an incident, not the comparison. Following v1's B-attempt-1 precedent, the coordinator stopped the run (all six arm processes + orchestrator killed by PID from pids.json), preserved the run dir, and discarded its numbers. State at abort: 3 claimed / 15 queued / 0 completed, 21 ledger events; the mirror had begun posting to `fleet-bus-v2-c2-run1`. Production Ollama was **not** restarted or touched (out of scope); recovery path is queue drain + re-probe, then relaunch, or deferral with the window stated. **Recovery verified ~09:41:** with the A/B's own load removed, the queue drained and a 50-token probe answered in 10.9 s (response carrying the classic untagged think-leak). The wedge was transient queue-stacking — the timed-out zombie calibration generation plus queued worker requests on a CPU-contended runner — not a service failure. Relaunching as attempt 3.

### Arm C2 run 1, attempt 3 — ABORTED ~10 min in (same failure; discarded, preserved). Remaining runs DEFERRED to a quieter window.

Attempt 3 repeated the failure end-to-end: the 4b calibration timed out at 600 s again, the run launched, the mirror kept a perfect record (24/24 events posted, 0 errors — the SwarmChat durable-log role is the one component that performed flawlessly all morning), 3 results posted, then worker c1's first scored call (task 1) **timed out at 600 s** — the cascade in the run's own accounting: each client timeout leaves a server-side zombie generation that slows the queue behind it, causing the next timeout. State at abort: 6 claimed / 12 queued / 0 terminal. Root condition, measured first-hand: the production Ollama qwen3:4b runner is **mostly CPU-resident (1.26 GB VRAM vs 7.2 GB during B run 1)** and shares 40 threads with the Gemma trial's CPU llama-server at ~1053% CPU and lane-b's at ~651%, load 45–58 sustained; a leaked 1,600-token 4b generation cannot clear within 600 s in that regime. B run 1 stands in contrast: GPU-resident runner, 10.21 tok/s calibration, 0 failed calls. No filed-harness change can repair runner placement (production Ollama's decision) or tenant load, and enlarging the HTTP timeout mid-experiment would be an unfiled design change. Per the brief's explicit fallback, the remaining runs (C2 run 1, C2 run 2, B run 2) are **deferred to a quieter window**: 1-min load < 30 **and** a full DRAFT-prompt 4b probe completing < 240 s (the endpoint health B run 1 actually enjoyed). The natural trigger is the 4b runner unloading after 30 idle minutes and reloading — bus-41 RTX sits at 7 MiB used, so a reload may restore GPU residency. Attempts 1–3 are preserved on-box (`.bak-*` dirs) and none of their numbers enter RESULTS.

### Endpoint probe after runner reload — window does NOT open (Nov 14, ~10:34–10:46 CT)

The coordinator waited with zero 4b requests until the wedged runner's keep-alive expired (10:33:40) and it unloaded (`/api/ps` → empty). A single decisive probe followed: the exact worker path (`workgen2.run_work`, task d1, qwen3:4b, 1,600-token budget). Two facts, both first-hand: **(1) the reload restored full GPU residency — size_vram 7,220,326,563, byte-identical to B run 1's healthy placement** — the placement theory is confirmed; **(2) the probe still timed out at 600.1 s.** GPU residency alone does not restore service while the tenant CPU load (Gemma trial + lane-b, load 31–36 even in this quieter phase) and a shared, busy GPU (bus-05 at 74–93% util earlier) starve the runner's pipeline. The filed window conditions (load < 30 **and** DRAFT probe < 240 s) are therefore **not met today**, and per the brief's fallback the remaining runs (C2 run 1, C2 run 2, B run 2) stand DEFERRED — to be launched, in the filed counterbalanced order, by whoever picks this up when both conditions measure true. RESULTS.md is filed as a partial-results verdict: the v2 win bar is **not evaluated**, and no leg is scored on a single arm.

## Completion session — Nov 14, 2026 evening (Joe's directive ~18:17 CT: "Finish out the testing on swarmbus v2")

The three deferred runs were executed in the filed order — C2 run 1 (`--kill-test`) → C2 run 2 → B run 2 — under the §4 window protocol of the partial RESULTS filing: launch only when 1-min load < 30 **and** a fresh DRAFT-prompt probe through `workgen2.run_work` (task d1, 1,600-token budget) completes < 240 s, both measured immediately before launch. Probe script: `/tmp/probe_draft.py` on-box (workgen2 path, run tag "probe", own call log; unscored, never in arm metrics).

### Window hunt + C2 run 1 (scored, attempt 4) — COMPLETE

Probes before the scored launch: probe 1 launched 18:21 at l1 19.52 completed **216.6 s** — under the bar, but load had spiked to 31.8–40.7 during it (Tranche B CPU blocks), so condition 1 failed at completion; no launch. Probe 2 at l1 16.69 completed **131.6 s** with l1 8.65 at completion — **both conditions true**. Launch 18:28:49 CT: pre-load l1 8.20 (orchestrator's metrics record 8.2/19.38/21.25); qwen3:4b GPU-resident, size_vram **7,220,326,563** (bus 06 M4000, 7,072 MiB); per-bus at launch: 05:00.0 6,034 MiB/93% (Tranche B main chain), 41:00.0 5,342 MiB/95% (lane41); tenancy: tranche-b-chain active, tranche-b-lane41 active, tranche-b-m4000 inactive; one tenant llama-server ~1100% CPU. Calibration: 8b 44.8 s (96 eval, 2.14 tok/s), 4b 146.9 s (1,600 eval, 10.89 tok/s). Mid-run, Tranche B blocks drove l1 to a 62.6 peak (trace mean 41.4); the endpoint never wedged — **0 failed calls in 24**. Kill test fired after the 6th completion: worker c2 SIGKILLed holding v2 → recovered via lease expiry + reaper requeue, **latency 478.4 s**, no duplication. **Result: 17 done + 1 deadletter (v6) = 18/18 accounted, lost 0, duplicated 0, shipped-wrong 0, first-attempt pass 15/18, wall 2,358.1 s, work 24,110 tokens / 24 logged calls (25 real generations incl. the killed in-flight call), coordination tokens 0, mirror 116/116 events 0 errors.** DLQ v6 priced 3,834 tokens (reasons: WRONG_VERDICT_1, UNPARSEABLE-leak, WRONG_VERDICT_3 ×2). Metrics copied off-box (`results/metrics/C2-run1-metrics.json` + call log).

### C2 run 2 — COMPLETE

Window: load collapsed to l1 1.92 as a Tranche B segment boundary passed; probe 3 completed **133.4 s** with l1 8.75 at completion — both conditions true. Launch 19:18:47 CT: pre-load l1 8.13 (metrics: 8.13/15.77/28.40); 4b GPU-resident 7,220,326,563 B; 8b partially resident (1,773,634,846 B VRAM) at launch. Calibration: 8b 42.9 s (122 eval, 2.84 tok/s), 4b 82.5 s (1,053 eval, 12.77 tok/s). Load trace mean l1 39.1 / max 43.6 (Tranche B tenancy); 0 failed calls in 27. The run's tail was ladder-heavy: two tasks climbed all four rungs in the final minutes and the last completion landed ~1 min inside the 60-min cap. **Result: 16 done + 2 deadlettered (v1, v6) = 18/18 accounted, lost 0, duplicated 0, shipped-wrong 0, first-attempt pass 13/18, wall 3,108.9 s, work 30,182 tokens / 27 calls, coordination tokens 0, mirror 126/126 events 0 errors.** DLQ priced: v1 3,870 (WRONG_VERDICT_3 ×4), v6 3,834 (UNPARSEABLE, WRONG_VERDICT_1+2, WRONG_VERDICT_3 ×2) — run DLQ total 7,704. Metrics off-box (`C2-run2-metrics.json` + call log).

### B run 2 — window hunt (four failed probes), then COMPLETE on an exclusive box

Probes 4–7 all failed the < 240 s condition under sustained Tranche B tenancy (two tenant llama-servers at ~1,250–1,950% CPU each): **329.2 s** (load spiked to 43 mid-probe), **252.1 s**, **283.6 s**, **255.1 s**. No launch was attempted on a failed window. At **20:47 CT Joe parked the Tranche B filler lanes**; the main agent stopped them on-box (chain + lane41 processes gone, all three units inactive) and Fortress became exclusive to this program. The 4b runner was by then mostly CPU-resident (1.26 GB VRAM — the production service's placement under the day's VRAM pressure; not altered by the coordinator). Probe 8 completed **194.6 s** with l1 9.74 — both conditions true. Launch 20:53:44 CT: pre-load l1 6.48 (metrics: 6.48/15.37/23.37); GPUs near-empty (bus 05 562 MiB, bus 06 1,384 MiB, bus 41 7 MiB). Calibration: 4b 194.6 s wall for the 1,600-token calibration burn = **8.22 tok/s** (the CPU-heavy runner, recorded as filed). Load trace mean l1 20.2 / max 20.8 — the run's own CPU-side generation work on an exclusive box. **Result: 18/18 done, lost 0, duplicated 0, shipped-wrong 3 (d1, v1, v6), first-attempt pass 15/18, wall 1,926.6 s, work 17,807 tokens / 18 calls, failed_calls 0, coordination tokens 0, budget-burned calls 3.** No kill test (run 1 of the arm carried it). Metrics off-box (`B-run2-metrics.json` + call log).

### Program rulings filed during the completion session

- **Metric addendum (Joe, Nov 14 20:57 CT):** the headline efficiency metric for every scorecard in this program is **tokens per error-free job, per task class** — total tokens (prompt processing + generation, all attempts incl. retries/escalations; checker passes are deterministic code = 0 tokens here) ÷ jobs verified correct at collection. Raw tok/s is a diagnostic footnote. Computable for all four v2 runs from the call logs (`prompt_eval_count` + `eval_count` per call): the v2 metrics files' `work_tokens`/`per_task_tokens` are already prompt+eval sums (verified to the token against the logs). B's per-class/per-task split uses prompt-length attribution validated against `results/` file mtimes (36/36 calls, 0 mismatches; class-exact). RESULTS.md §5 carries the tables.
- **Expanded mandate (Joe, Nov 14 20:51 CT):** the program is now an iterate-until-working loop — this v2 scorecard + analysis is the design input to **v3**, which gets independent design checks from both frontier seats (Opus + Astra) before build, is tested by this same route (same harness discipline, same fairness protocol, same pre-filed criteria), and the loop continues version by version until a version clears the bar or an iteration fails to improve on its predecessor (Joe's decision point). Fortress exclusivity holds for the whole loop; Tranche B stays parked. Adoption of any winning version remains Joe's ruling.

### Final scorecard (design §9, aggregate of 2 runs / 36 tasks per arm)

Legs 1–4, 6–8 **PASS** (hard gate 0/0 both runs; accounted 36 ≥ 36; shipped-wrong 0 < 7; DLQ 3 ≤ 4 and ≤ 3/run; coordination tokens 0; interventions 0 ≤ 0; mechanics gate PASS). Leg 5 **FAIL**: C2 wall 5,467.0 s vs cap 1.25 × B 3,673.1 s = 4,591.4 s (ratio 1.488×). **Split = fail: Fleet Bus v2 is not adoption-justified as measured.** Full tables, DLQ pricing, per-task tokens, and the failure-mode analysis: RESULTS.md §§3–9.

## Interventions log

No in-run operator interventions in any scored run (B runs 1–2, C2 runs 1–2): no process was touched, restarted, or repaired between a scored run's launch and its completion, in either arm. Coordinator actions on **unscored** attempts (Nov 14 AM aborts of C2 run 1 attempts 2–3 under the filed defer/abort protocol; the evening's probe/window measurements) are recorded in the run entries above, per the design's leg-7 accounting. The Tranche B park (20:47 CT) was Joe's own action on a co-tenant, outside any run (B run 2 launched after it, under the standard window protocol).
