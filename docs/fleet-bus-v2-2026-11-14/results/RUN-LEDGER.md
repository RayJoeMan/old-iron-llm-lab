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

## Interventions log

*(filled as they happen; none is the expected content)*
