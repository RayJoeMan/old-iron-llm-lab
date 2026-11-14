# Fleet Bus v2 — PRE-REGISTERED DESIGN

**Filed:** Nov 14, 2026, before any v2 build or run. Changing anything in §§2–7 after this filing requires a written amendment in the run ledger with the reason, per the freeze discipline v1 used.
**Commissioned by:** Joe, Nov 14, 2026 (~08:10 CT) — "Commission Fleet Bus v2: design + A/B on the salvage."
**Governs:** the v1 record at `~/workspace/your_files/fleet-bus-ab-2026-11-13/` (design, Opus check, results, run ledger, code masters — workspace masters verified byte-identical to the on-box test article: fleetbus.py sha256 c2985494…, workload.json sha256 e8e3748b…).

## 1. What v1 settled, and what v2 is actually testing

V1 answered the coordination question: the bus's ledger mechanics (atomic claims + leases + heartbeats, idempotency keys, reaper, JSONL export) never failed — 0 duplicates in 36 tasks, 0 coordination tokens, mechanics gate passed in full — and LLM-arbitrated claims (Arm A) are structurally too expensive (79,601 coordination tokens = 2.5× the work; both runs hit the cap). V1's bus lost on exactly one layer: its **validator policy**. Every lost task (5/36) died the same way — 3 generations, 3 deterministic-validator failures, attempt cap, `dead` — while the file queue shipped some of the same wrong answers as completed work. The results file's own revisit conditions were: *a validator policy that escalates instead of dropping, and a worker pool strong enough that the gate's refusal rate is rare.*

V2 therefore does **not** re-test coordination mechanics in isolation. It tests a **system**: the v1 ledger core, unchanged in its mechanics, plus an escalation ladder and a dead-letter queue, against the incumbent file-queue discipline end-to-end. The filed question is: *does the bus system — nothing lost, nothing duplicated, nothing wrong shipped silently — beat the incumbent discipline on delivery, wall, and shipped-wrong, at a bounded escalation cost?*

Two consequences of that framing, filed openly:

- **First attempts are identical across arms** (same model, prompt, settings — §4), so first-attempt quality stays directly comparable to v1 and across arms. The ladder is the only quality-policy difference.
- **Arm A does not re-run.** Its question was answered structurally in v1, not marginally: re-running would spend ~2 h of shared endpoint time re-measuring a 2.5× structural overhead. V1's A numbers stand as context. SwarmChat appears in v2 only in its validated role — durable log (§5).

## 2. Arms

- **Arm B — File queue (control, the incumbent).** V1's arm_b.py discipline, unchanged: `queue/ claimed/ results/ done/`, claim = flock-guarded rename of the oldest task file with the claim-time clock reset (the v1 repair: file mtime is not a lease), 150 s staleness sweeper, one generation per claim on the cheap worker, result delivered **unvalidated** — whatever the worker produces is what ships. Zero coordination generations.
- **Arm C2 — Fleet Bus v2.** The v1 ledger core with the policy layer changed (§3): results land in `validating`, a separate checker process runs the same deterministic validators as v1, failures climb the escalation ladder (§3.1), and terminal failure is a **dead-letter**, not a death (§3.2). A mirror process copies ledger events to SwarmChat as a durable log (§5). Zero coordination generations — arbitration is deterministic ledger code; the mirror transports events and arbitrates nothing.

Both arms: **same workload** (§4.1), **same work-generation code path** for first attempts (§4.2), **3 workers** each.

## 3. What changes in the bus — policy layer only

`fleetbus2.py` is v1's `fleetbus.py` with the smallest change that implements the ladder. The claim, lease, heartbeat, idempotency, result-posting, validation-claim, and reaper *mechanics* are untouched. The changes are:

1. **Terminal-failure state renamed `dead` → `deadletter`**, with event types `DEAD`/`DEAD_LEASE` → `DEADLETTER`/`DEADLETTER_LEASE`. A deadlettered task is **terminal and accounted**: it carries its full validator-reason history in the task record and is surfaced to the coordinator (§3.2). It is not `done`, and it is not lost.
2. **Attempt budget raised to `max_attempts = 4`** at enqueue (the ladder length, §3.1).
3. `counts()` reports the `deadletter` state. `all_terminal()` semantics unchanged (queued/claimed/validating are the only non-terminal states).

A unified diff of fleetbus.py → fleetbus2.py is filed in the run ledger so the "mechanics untouched" claim is checkable, not asserted.

### 3.1 The escalation ladder (filed numbers)

| Rung | Attempts | Model | Settings |
|---|---|---|---|
| 1 — cheap | 1, 2 | `qwen3:4b` | temp 0.3, num_predict 1600, think off + strip (§4.2) |
| 2 — escalation | 3, 4 | `qwen3:8b` | identical prompt and settings; only the model changes |

- Attempt → rung mapping is deterministic from the task's attempt number at claim time; the worker selects the model by rung. No model makes any routing decision.
- **Per-task budget:** at most 4 generations; each generation capped at 1,600 output tokens; worst case ≈ 4 × (prompt + 1,600) tokens per task, reported per task from the call log.
- **Per-run budget:** 60-minute cap (v1's amended value), all-terminal ends the run earlier.
- Lease/heartbeat unchanged (150 s / 20 s). A lease expiry consumes the attempt exactly as in v1; expiry on the final attempt deadletters with reason `LEASE_EXPIRED_FINAL`.

### 3.2 The dead-letter queue (nothing dies silently)

When the checker records a task's 4th validator failure (or the reaper deadletters it), the checker/orchestrator writes `deadletter/<task-id>.json` in the run dir containing: task id, kind, every attempt's worker, model rung, artifact path, and validator reasons, plus the accumulated reason string from the ledger. A `DEADLETTER` ledger event is emitted in the same transaction as the state change. The run completes when every task is `done` or `deadletter`. The DLQ files are the coordinator's surface: in a production adoption they are the human/coordinator work queue; in this A/B they are counted, priced (wall + tokens spent reaching them), and reported per task.

### 3.3 Shipped-wrong — a first-class metric (the gate's value, priced)

**Definition, identical for every arm:** a task is *shipped-wrong* if the artifact the arm delivers as its successful result fails the shared deterministic validator when re-scored at collection time.

- Arm B delivers unvalidated work, so its shipped-wrong count is whatever its single-attempt output gets wrong. Delivered artifact for B = the **last-written** result file for that task in `results/` (a consumer integrating the results directory ends with the final state; the rule is filed here, before runs).
- Arm C2 delivers only checker-passed artifacts, so its shipped-wrong should be 0 *by construction* — and is still measured: the merged artifact recorded in the ledger is re-scored at collection, and any failure is counted as shipped-wrong **and** disclosed as a checker defect.
- The counterfactual is reported alongside: how many of Arm B's shipped-wrong tasks Arm C2's gate caught (passed on retry, or deadlettered rather than shipped).

## 4. Workload and generation (frozen)

### 4.1 Workload
V1's `workload.json`, byte-identical (sha256 e8e3748b…): 18 tasks — 6 CLASSIFY, 6 DRAFT, 6 VERIFY — with gold answers only in the validator copy. Same seeds as v1 (run 1: 20261113, run 2: 20261114), so per-run task order matches v1's shuffles exactly; disclosed as a continuity choice, not a freshness claim. **2 runs per arm.** Arm order counterbalanced: run 1 = B then C2; run 2 = C2 then B.

### 4.2 Generation path
One shared module (`workgen2.py`, v1's workgen with the model parameterized and the call log extended — §6) serves every work generation in both arms: HTTP POST to Fortress Ollama `/api/generate`, `temperature 0.3`, `num_predict 1600`, `think: false`, response passed through v1's `strip_think`. Token counts from Ollama's own response counters, never estimated.

**Think-leak handling (E271 / TUNING #288, E56/#55).** The fleet's measurements say: qwen3:4b's blob-embedded chat template ignores every budget control on the Ollama path — budget-0 is a *template* property (it binds only via Qwen3's native jinja template + `enable_thinking: false` on the llama.cpp stack), and the leak is a qwen3:4b-only pathology (qwen3:8b measured 0.0% think share in E56). V2's handling, at the harness level, on the Ollama path both arms share:

1. `think: false` is sent and the response is stripped before validation (v1 behavior, retained) — the validated artifact is always the post-strip text.
2. **Leak-affected failures are their own metric class:** a generation is *leak-flagged* if its `eval_count` ≥ 95% of the 1,600 budget **and** the resulting artifact fails validation with a structural reason (NO_LABEL / UNPARSEABLE / MISSING_FIELD). Counted per arm, per run, per rung, from the call log joined to verdicts by task + attempt (the v2 call log carries both fields — §6).
3. The ladder is the mitigation: rung 2 moves the task to a model with no measured leak pathology, so a leak-killed cheap attempt does not end the task.

Switching serving stacks (llama.cpp native template) mid-A/B is rejected on the record: it would change the generation path for one arm only and break comparability; template-level budget control is a serving-lane property, out of scope here.

### 4.3 Worker pool and contention plan
- Cheap worker: **qwen3:4b** (continuity with v1; the fleet's classification-class lane). Escalation: **qwen3:8b** (fleet drafting standard; leak-free in E56; F1 solo rate 51.60 tok/s on an RTX card via llama.cpp — Ollama-path rate measured by calibration, §4.4, not assumed).
- Both models are served by the Fortress system Ollama (tailnet endpoint, as v1). Arm B never calls the 8b; C2 calls it only on rung 2. Disclosed asymmetry: C2's escalation runner is a resource B doesn't use — that is the system being tested, priced via work tokens and wall.
- **Contention protocol (v1's walls were contention walls; v2 files its conditions in advance):**
  - Before each run: record 1-/5-/15-min load averages and one **unscored calibration generation per model the run will use** (timed, filed in the run ledger).
  - During each run: load average sampled every 60 s into the run's metrics (`load_trace`).
  - **Defer rule:** if the 1-min load average exceeds **30** at a run's scheduled start (box: 2× E5-2660 v2, 40 threads; the known co-tenant is the Gemma trial's 12-thread CPU lane, baseline load ≈ 14), the run waits and re-checks rather than starting distorted. If a clean-ish window cannot be had today, the runs are deferred and the design + Opus check are filed with the window stated — honesty over speed, per the commission.
  - Walls are always reported as *measured under the filed load trace*, never as clean numbers.

## 5. SwarmChat's role — durable log only

- Per C2 run, a **mirror process** tails the run's ledger events table and posts each event (type, task, actor, detail) to a fresh SwarmChat channel (`fleet-bus-v2-c2-run<n>`), created by the roster operator identity exactly as v1's Arm A setup did. The mirror makes **zero model generations** and **zero arbitration decisions**; claim ownership exists only in the ledger.
- The mirror is best-effort transport: if SwarmChat is unreachable (e.g. a service restart by the infra-buildout coordinator, whose Python 3.12 pin owns that service — v2 consumes the pin, never does pin work), events queue in the mirror and are posted when the server returns; mirror lag and posted/total counts land in the run's metrics, and any shortfall is disclosed in the results. **A mirror failure cannot fail the bus, and cannot pass it either** — mirror completeness is reported, not a bar leg.
- Client: the pinned Python 3.12 environment, as v1's Arm A client used (server side: the infra coordinator's 3.12-pinned service, consumed as-is). Mirror identities are the existing roster's; tokens stay on-box in 0600 files, never printed or copied off-box. Pre-existing SwarmChat chats/data are never touched; the mirror writes only to its own fresh channels.

## 6. Harness changes vs v1 (all disclosed; logging-only except where stated)

1. `workgen2.py`: model is a parameter (rung selection); call-log entries gain `task`, `model`, and `attempt` fields so tokens, walls, and leak flags attribute per task/rung. Generation request bodies are otherwise byte-identical to v1's for rung 1. Applies to both arms equally.
2. `run_ab2.py`: orchestrates arms B and C2 only; adds per-run load trace, calibration record, C2 deadletter collection (DLQ files joined into metrics), shipped-wrong re-scoring for both arms (§3.3), and leak-flag computation (§4.2). The v1 kill test carries over (§7).
3. `arm_c2.py`: v1's arm_c with rung-aware model selection in the worker, and DLQ file writing on deadletter transitions. Worker/checker/reaper structure, heartbeat discipline, and exception guards are v1's, unchanged.
4. Arm B runs v1's `arm_b.py` **unmodified**, against `workgen2.py` (its `run_work` signature gains a defaulted model argument; arm_b's call is unchanged).

## 7. Kill test (pre-registered, run 1 of each arm)

As v1: after the 6th task completion in run 1, SIGKILL the worker holding the oldest in-flight claim (fresh probe at kill time; worker #2 if none in flight). For C2 the victim pool is workers only — checker, reaper, and mirror are never kill victims in this test (their resilience is covered by the mechanics gate's kill leg). Measured: recovery (yes/no), latency (kill → that task terminal), duplication.

## 8. Metrics (counted by these rules, from first-hand records)

Per run, per arm: wall time (first claim-able moment → last task terminal, DLQ counting as terminal for C2); tasks done / deadlettered / lost; duplicated work (v1's definitions per arm; for C2: late result rows + same-attempt duplicate rows — sanctioned ladder retries are not duplication); shipped-wrong (§3.3) with the gate-caught counterfactual; validator first-attempt pass rate (comparable to v1); work tokens and calls split by model/rung; coordination tokens (counted from purpose-tagged call logs — any untagged call fails collection loudly, as v1); coordination messages/bytes (B: file ops; C2: ledger events + mirror posts); leak-flagged failures (§4.2); kill recovery; coordinator interventions; load trace + calibration readings; mirror posted/total.

## 9. WIN BAR — falsifiable, all legs must hold

Fleet Bus v2 (Arm C2) is adoption-justified **iff**, on the aggregate of the 2 runs (36 tasks per arm):

1. **Hard gate:** C2 lost = 0 **and** duplicated = 0, in **each** run individually. (Lost = neither done nor deadlettered at run end.)
2. **Accounted delivery:** C2 accounted (done + deadlettered) = 18/18 in each run, and C2 aggregate accounted ≥ Arm B aggregate accounted.
3. **Shipped-wrong:** C2 aggregate shipped-wrong < Arm B aggregate shipped-wrong. Filed knowingly: if B ships nothing wrong in either run, this leg cannot pass — the gate's value must be demonstrated on this workload, not assumed.
4. **DLQ cap:** C2 aggregate deadlettered ≤ 4 of 36, and ≤ 3 in any single run. (A bus that escalates everything to the DLQ has automated nothing.)
5. **Wall:** C2 aggregate wall ≤ 1.25 × Arm B aggregate wall. (Looser than v1's 1.10×, deliberately: escalation costs wall by design; 1.25× is the filed price of the gate. Measured under the §4.4 load protocol and reported with the trace.)
6. **Coordination tokens:** C2 coordination-generation tokens = 0 exactly, counted. Any coordination-purpose generation inside C2 fails this leg. (Mirror posts are transport events, counted in messages/bytes, not generations.)
7. **Interventions:** C2 ≤ Arm B (in-run operator actions beyond launch and the pre-registered kill; harness repairs between attempts are disclosed in the ledger and reported alongside, as v1 did).
8. **Mechanics gate (§10) passes in full** before the A/B numbers are counted.

A split result is a **fail**. If the bar fails, the recommendation filed with the results follows v1's: file-queue discipline stays, SwarmChat stays as log plumbing, and this design + record are filed as tested-and-refuted (or tested-and-split). **Adoption is Joe's ruling either way; nothing in this A/B replaces any live system.**

## 10. Mechanics gate (C2 only, before its A/B numbers count) — v1's gate as regression

V1's four legs, run against `fleetbus2.py`, adapted only for the renamed terminal state:

1. **Claim flood:** 1,000 synthetic no-op tasks, 8 concurrent claimants claiming + completing: exactly 1,000 tasks, every task claimed exactly once, all terminal.
2. **Duplicate-enqueue storm:** the 18-task batch enqueued twice, concurrently, from two processes → exactly 18 tasks.
3. **Kill/restart:** during a 100-task flood, SIGKILL the reaper and one worker mid-task, restart the reaper → zero lost, zero duplicated merges, all leases recovered without operator action. (Terminal = done or deadletter; the gate's sim workers always pass validation, so deadletter count is expected to be 0 and is reported.)
4. **Reconciliation:** an independent replay of the JSONL event log reproduces the ledger's per-state counts exactly (replay map gains `DEADLETTER → deadletter`, `DEADLETTER_LEASE → deadletter`).

## 11. Safety and isolation

Test article only: everything v2 lives in `~/fleet-bus-ab2/` on Fortress (workspace masters in this folder's `code/`), removable with one `rm -rf`. The ledger has no network listener. Nothing touches: production lanes, the production file queue, SwarmChat production data (§5's fresh channels excepted, as v1), lane-b, the Gemma trial, the capture-rig build, the infra-buildout coordinator's workstreams, or the Mint. The kill test kills only v2 worker processes, identified by PID at launch. All workload content is synthetic and non-sensitive; all tokens stay on-box.

*Design ends. Filed before build.*
