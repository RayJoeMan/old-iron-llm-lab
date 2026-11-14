# Independent design check — GPT-6 Astra

**Checker:** gpt-6-astra via the custom.openai connector. **Date:** Nov 14, 2026.
**Input:** the identical blind packet given to both checkers — filed DESIGN.md + the v2 harness code (fleetbus2.py, workgen2.py, workgen.py, arm_c2.py, mirror.py, run_ab2.py, gate_c2.py, arm_b.py, validators.py), ~100 KB. The checker did not see the other checker's review.
**Call record:** prompt 24,247 tokens / completion 5,924 (1,024 reasoning), finish=stop, 137 s.
**Dispositions:** ADJUDICATION.md (alongside). This file is the checker's verbatim output.

---

## Overall assessment

**The harness is not ready to support the filed adoption decision.** There are material holes in delivery accounting, unequal leak accounting, incomplete failure-cost accounting, and a mechanics gate that can pass without exercising the promised recovery scenario.

The shared first-generation request path and deterministic ladder selection are implemented correctly. However, those clean portions do not resolve the findings below.

**Scope limitation:** `workload.json`, the prior experiment, the promised core diff, and run records were not supplied. I cannot verify workload identity, historical byte-equivalence, actual execution order, amendments, or observed outcomes. Findings below concern the supplied code, not claims about what happened in an actual run.

---

## 1. Delivery, duplication, and validation correctness

### 1. HIGH — Arm B can count an undelivered task as successfully completed, without counting it lost or shipped-wrong

**Anchors**
- `code/arm_b.py`, `main`: result-write failures are swallowed — `"except OSError: pass"` — before `"os.rename(claimed_path, done_path)"`.
- `code/run_ab2.py`, `collect`: `"terminal = done_ids"`; unreadable result records are skipped with `"except Exception: pass"`.

A failed, missing, or partial result write does not prevent B from creating its done marker. Collection then excludes the task from `lost`, while shipped-wrong scoring sees only successfully parsed result files.

**Consequently, a task can have no usable delivered artifact and appear in neither `lost` nor `shipped_wrong`.** This is a material accounting advantage for B relative to C2, whose unreadable done artifact is counted shipped-wrong.

### 2. HIGH — Arm B permits stale delivery and can overwrite evidence of duplicated work

**Anchors**
- `code/arm_b.py`, `_sweeper_loop`: `"os.rename(full, dst)"`.
- `code/arm_b.py`, `main`: `"taskid + \"__\" + worker_id + \".json"` and `"open(results_path, \"w\")"`.
- `code/run_ab2.py`, `collect`: `"if n > 1: duplicated[tid] = n"`.

After a stale claim is requeued, the original worker can still write a result: there is no ownership check or fencing at delivery. A reclaimed task can therefore have concurrent generations and deliveries.

The result pathname identifies only task and worker, not claim or attempt. If the same worker later handles that task again, its previous result is overwritten. Counting surviving files cannot detect all repeated work or deliveries. Last-written delivery selection also does not restore the overwritten evidence.

### 3. HIGH — Validation verdicts are not fenced to their validation claim or attempt

**Anchor**
- `code/fleetbus2.py`, `Bus.verdict`: the only eligibility check is `"if task['state'] != 'validating'"`; `checker`, `v_claimant`, validation lease, and attempt identity are not checked.

A checker whose validation lease expired can submit a verdict after another checker takes ownership. More seriously, if another checker fails the old result and a new generation reaches `validating`, the stale checker can apply its old verdict to the new artifact.

This can merge an artifact that was never checked by the approving checker, or reject/deadletter an artifact based on a different attempt. Collection should catch an actually validator-failing merged artifact if it remains readable, but the gate’s approval mechanism itself is incorrect.

The A/B uses one checker, reducing exposure there; the supplied mechanics gate uses multiple checkers.

### 4. MEDIUM — Expired worker leases can still produce accepted results

**Anchor**
- `code/fleetbus2.py`, `Bus.post_result`: `"if claimant_match and task['state'] in ('claimed', 'validating')"`.

Acceptance does not check `lease_expires_at`. An expired worker can post before the reaper runs and receive a normal, non-late result.

Thus expiry does **not** always consume an attempt as §3.1 says: whether it does depends on whether posting or reaping wins the race. The result is also absent from late-result duplication accounting. This is a lease-semantics discrepancy, even if expiry were intentionally meant to become effective only upon reaping.

### 5. MEDIUM — C2’s duplication counter can double-count one row and does not incorporate duplicate merges

**Anchors**
- `code/run_ab2.py`, `probe_c2`: counts `"WHERE r.late=1"` and separately adds `"(r['n'] - 1)"` for same-attempt groups.
- `code/run_ab2.py`, `collect`: duplicate merges are placed separately in `"extra['duplicated_merges']"`.

A late row that is also the second row for an attempt contributes to both sums. If the intended metric is distinct duplicated work, it is overstated.

Conversely, repeated merge events are not incorporated into `duplicated_work`. They are disclosed separately, but a consumer evaluating the hard gate using only `duplicated_work` could miss them. The collector does not provide a consolidated hard-gate result that resolves either issue.

### 6. MEDIUM — Shared validators permit substantively wrong or malformed output to pass

**Anchors**
- `code/validators.py`, `validate`, CLASSIFY: `"found = set(l for l in LABELS if l in upper)"`.
- Same function, DRAFT: `"nums = _numbers(fields.get('FACTS', ''))"`.
- Same function, VERIFY: `"if num not in d: d[num] = verdict"`.

Examples:

- `NOT TEACHING` passes classification when the gold label is `TEACHING`.
- DRAFT can pass with empty TITLE/FACTS, fabricated prose, and foreign numbers in SUMMARY; numeric checks apply only to FACTS.
- VERIFY accepts additional contradictory answers after the first answer for each number and does not enforce exactly three lines.

**This is not an asymmetric implementation of the filed shipped-wrong definition:** both arms use the same validator, and the definition explicitly measures validator failure. It is nevertheless an important limit on the broader “nothing wrong shipped silently” claim. Re-scoring with the same permissive validator cannot reveal these errors.

---

## 2. Metric accounting and comparison bias

### 7. HIGH — B’s leak metric is not the registered metric and is not comparable to C2’s

**Anchors**
- `code/arm_b.py`, `main`: `"workgen.run_work(task, call_log_path, run_tag)"`.
- `code/workgen2.py`, `run_work`: `"task_id=None, attempt=None"`.
- `code/run_ab2.py`, `collect`, B branch: `"if e.get('eval_count', 0) >= LEAK_EVAL_FLOOR"`.

B’s calls have no task/attempt attribution. Its leak counter counts **every** high-token generation, including valid outputs and nonstructural failures. C2 requires a matching failed verdict with a structural reason.

This contradicts §§4.2 and 6’s common task-plus-attempt accounting and systematically makes B’s reported leak count broader than C2’s. The compatibility shim preserves requests, but does not implement the promised logging extension for B.

### 8. HIGH — Calls killed in flight disappear; failed calls are priced as zero tokens without an uncertainty metric

**Anchors**
- `code/workgen2.py`, `generate`: logging occurs after response completion or inside `"except Exception"`.
- Same function: failed entries use `"prompt_eval_count": 0, "eval_count": 0`.
- `code/run_ab2.py`, `main`: `"signal.SIGKILL"`.

A worker killed during the HTTP request cannot execute either logging branch. Its request may continue generating server-side, but contributes no call and no tokens to metrics.

Ordinary request failures are counted as calls but assigned zero tokens, although the code explicitly acknowledges possible server-side consumption. Collection does not report failed-call counts or unknown token cost.

This affects both arms and particularly the pre-registered kill test. Costs cannot be described as complete measured generation consumption.

### 9. HIGH — Call-log collection does not fail loudly on all unaccountable entries

**Anchors**
- `code/run_ab2.py`, `collect`: `"except Exception: continue"` around JSON parsing.
- `code/workgen2.py`, `generate`: `"text = resp_obj['response']"` occurs outside the request exception handler.

Malformed/truncated JSONL lines are silently discarded. A missing log is also accepted as zero calls and tokens. A valid JSON server response missing `response` raises before any call-log entry is written.

The collector rejects an unknown purpose only when a line successfully parses. That is weaker than the filed “any untagged call fails collection loudly” discipline, and permits incomplete evidence to look like zero coordination cost.

### 10. HIGH — “First-attempt pass rate” actually scores the earliest surviving artifact, not attempt 1

**Anchors**
- `code/run_ab2.py`, `collect`: files are sorted by `"os.path.getmtime(p)"`, then `"if tid not in first_artifacts"`.
- `code/arm_c2.py`, `checker_mode`: `"if logical not in seen_first"`.

If attempt 1 is killed, errors, or never writes an artifact, a later attempt becomes the reported first attempt. If an old attempt writes late, mtime ordering can also select the wrong attempt.

C2’s `first_verdicts` file has the same conceptual issue: it records the first validated artifact, not necessarily claim attempt 1. B has insufficient attempt metadata to recover the distinction.

This can inflate first-attempt quality and break the promised comparison, particularly around the kill test.

### 11. HIGH — The registered load-based defer rule is absent

**Anchor**
- `code/run_ab2.py`, `main`: `"pre_load = read_loadavg()"` proceeds directly to `"calibration = calibrate(...)"` and process launch.

There is no `l1 > 30` check, wait, or recheck. Runs start regardless of measured contention.

Additionally, the initial load-trace record labels the **pre-calibration** reading as `t=0`, even though calibration may take many minutes. It need not describe actual run-start conditions.

Because aggregate wall time is a win-bar leg, this is a material departure from the registered comparison protocol.

### 12. MEDIUM — Wall time and final accounting cover different intervals

**Anchors**
- `code/run_ab2.py`, `main`: `"t0 = time.time()"` occurs after worker launches.
- Same function: `"wall = time.time() - t0"` precedes `"time.sleep(2)"`, termination, and collection.

Workers may already claim and complete work before timing starts. After timing ends, workers/checkers receive another two seconds before termination, and collection includes whatever state they achieve during that interval.

At the cap, tasks can therefore be counted complete **after** the measured endpoint without their completion time being charged. Completion timestamps and kill-recovery status can also disagree with final task states. The timing contract is not precisely “first claim-able moment → last terminal.”

### 13. MEDIUM — Coordination message/byte accounting is incomplete and asymmetric

**Anchors**
- `code/run_ab2.py`, `collect`, B branch: `"coord_messages = len(files) + len(terminal)"`.
- Same function, C2 branch: `"SELECT COUNT(*) FROM events"` and `"coord_bytes = os.path.getsize(ev)"`.

B counts result and done files, not claim renames, requeues, heartbeat touches, or other file operations; its byte count remains zero.

C2 counts ledger events and exported JSONL bytes, but omits mirror posts and their bytes. These are not the filed “B: file ops; C2: ledger events + mirror posts” measurements, and are not comparable transport-cost totals.

### 14. MEDIUM — Several registered outputs and decision controls are missing

**Anchors**
- `code/run_ab2.py`, `collect`: `"tasks_terminal": len(terminal)` where C2’s `terminal` contains only done tasks.
- Same function: output includes `"work_tokens_by_model"` but no calls-by-model, per-task wall/cost summary, or intervention field.
- `code/run_ab2.py`, `main`: directly launches a selected arm/run; it never reads `gate-results2.json`.

Specific omissions:

- C2’s `tasks_terminal` excludes deadletters despite the filed terminal definition.
- No gate-caught counterfactual is produced.
- No coordinator-intervention accounting is produced.
- Per-task generation durations are unavailable from the call log.
- No aggregate win-bar evaluation is supplied.
- The orchestrator does not enforce a successful mechanics gate before collecting A/B metrics.
- Counterbalanced execution order and mandatory run-1 kill tests are not enforced.

Some of these could be performed manually outside this program, but the supplied implementation does not demonstrate them. They must not be inferred from its metrics alone.

---

## 3. Dead-letter accounting and run lifecycle

### 15. HIGH — C2 can count a deadletter as accounted without ever surfacing its DLQ record

**Anchors**
- `code/arm_c2.py`, `checker_mode`: `"outcome = bus.verdict(...)"` precedes `"write_deadletter(...)"`.
- `code/arm_c2.py`, `write_deadletter`: failures only `"print(...)"`.
- `code/run_ab2.py`, `collect`: collects existing DLQ files without reconciling them against `dead_ids`.

The terminal state transition commits before the DLQ file is written. A crash, filesystem failure, or termination in that gap leaves a deadletter with no coordinator surface.

Collection still counts it as non-lost and deadlettered. It neither reconstructs the missing record nor explicitly fails or flags the missing surface. Thus ledger accounting can look complete while the promised dead-letter work queue is incomplete.

### 16. MEDIUM — Dead-letter records omit consumed attempts and lease-expiry reasons

**Anchors**
- `code/fleetbus2.py`, `Bus.reap`: `"UPDATE tasks SET state = 'deadletter' WHERE id = ?"`.
- `code/arm_c2.py`, `write_deadletter`: `"for r in results"`.
- `code/arm_c2.py`, `checker_mode`: unreadable-artifact handling calls `bus.verdict(..., "ARTIFACT_UNREADABLE")` without writing the normal verdict log.

Final lease expiry does not set the promised `LEASE_EXPIRED_FINAL` reason. DLQ attempt history is built from result rows, so killed/error attempts with no posted result disappear.

Unreadable-artifact verdicts are absent from per-attempt verdict history. Furthermore, the normal verdict JSONL write and ledger verdict transaction are separate operations, so the file can contain a verdict that never committed.

The promised complete, attributed attempt/reason history is therefore not implemented.

### 17. MEDIUM — The orchestrator can stop C2 while the checker still has terminalization work to do

**Anchor**
- `code/run_ab2.py`, `main`: `"if all(procs[k].poll() is not None for k in worker_keys): break"`.

Worker exit is treated as a stopping condition even if the checker is alive and tasks remain `validating`. The subsequent two-second grace period may be insufficient, after which the checker is terminated.

Such tasks are normally reported lost, so this is not a silent-accounting hole. It is nevertheless an avoidable delivery failure introduced by orchestration rather than by the bus policy.

---

## 4. Kill test and mechanics gate

### 18. HIGH — The A/B kill victim is not selected by oldest in-flight claim

**Anchors**
- `code/run_ab2.py`, `main`: `"for tid, wid in sorted(claimed.items())"`.
- Same function: fallback uses `"sorted(alive)[0]"`.
- Same function: trigger uses `"len(completion_ts) >= 6"`.

Selection is by task-ID ordering, not claim age. The fallback is the first live worker, not worker #2.

For C2, `completion_ts` includes deadletters as well as done tasks, so the trigger can also occur before six successful completions. The kill is optional for either run, rather than mandatory for run 1 only.

These departures change the intended failure-injection experiment and can change recovery latency and cost.

### 19. HIGH — The mechanics kill leg can pass without testing an interrupted claim or any lease recovery

**Anchors**
- `code/gate_c2.py`, `leg3`: `"time.sleep(3)"`, followed by `"reaper.terminate()"` and `"workers[0].terminate()"`.
- Same function: `"ok = counts['done'] + counts['deadletter'] == 100 and dup_merge == 0"`.

There is no check that the selected worker is alive and holding a claim. The flood may already be finished, or the worker may be between tasks. No positive reap count, recovered victim task, or successful restarted-reaper execution is required.

`terminate()` uses SIGTERM, not the registered SIGKILL. The pass condition also ignores lingering processes and permits deadletters to satisfy completion.

This gate can report success without establishing the recovery property it is supposed to certify.

### 20. MEDIUM — The remaining gate legs are weaker than their filed claims

**Anchors**
- `code/gate_c2.py`, `leg1`: `"for i in range(6)"` creates workers; two other processes are checkers.
- Same function: duplicate claims are grouped by `"task_id, detail"`.
- `code/gate_c2.py`, `leg2`: pass condition is only `"total == 18"`.
- `code/gate_c2.py`, `leg4`: reconciles only `"flood.db"`.

Consequences:

- Claim flood uses six claimants, not eight.
- It checks repeated claims of the same task/attempt detail, not exactly one claim per task.
- Enqueue storm can pass even if one enqueuer crashes before doing any work; child success and actual contention are not established.
- Reconciliation exercises only the successful flood path. Merely adding deadletter/reap mappings does not test replay of those transitions.

The replay itself is sensible for the happy-path log it receives, but the overall gate does not substantiate the full regression claim.

---

## 5. Mirror reliability, isolation, and secrets

### 21. HIGH — Subprocess timeout errors can print or persist the authentication token

**Anchors**
- `code/mirror.py`, `main`: subprocess arguments contain `"--token", token`; exception handling prints `"post failed ...: {e}"`.
- `code/run_ab2.py`, `create_mirror_channel`: the same token-bearing arguments are used, then `"rec['error'] = str(e)[:300]"`.

`subprocess.TimeoutExpired` includes the command in its string representation. A mirror send timeout can therefore print the full token into `mirror.out`. Channel-creation errors can similarly persist token-bearing command text, subject to truncation.

This directly violates the promise that tokens are never printed or logged.

### 22. HIGH — A mirror setup failure can prevent the bus from running

**Anchor**
- `code/run_ab2.py`, `create_mirror_channel`: token-file reading occurs before its `try`.
- `code/run_ab2.py`, `main`: calls `create_mirror_channel` before launching C2 workers/checker/reaper.

A missing or unreadable token file raises out of the orchestrator. C2’s ledger has been created, but the bus run is never launched.

That contradicts §5’s isolation guarantee that mirror failure cannot fail the bus.

### 23. MEDIUM — Mirror incompleteness can become `null` instead of a quantified shortfall

**Anchors**
- `code/mirror.py`, `main`: `mirror_metrics.json` is written only after the main loop.
- `code/run_ab2.py`, `main`: mirror is terminated after its flush allowance.
- `code/run_ab2.py`, `collect`: `"extra['mirror'] = ... else None"`.

If SwarmChat remains unavailable, the orchestrator normally kills the mirror before its own 3,900-second deadline. No final metrics file is then produced, even though a progress state file may exist.

The final result reports `mirror: null`, rather than the promised posted/total counts and lag. Initial mirror crashes have the same effect.

### 24. MEDIUM — Mirror restart and retry accounting is not reliable

**Anchors**
- `code/mirror.py`, `main`: restores `"last_seq"` but initializes `"posted = 0"` and `"errors = 0"`.
- Same function: sends first, then advances `last_seq` and calls `save_state()`.

After restart, already-posted events are skipped but not included in `posted`, so cumulative counts are wrong.

A successful send followed by a crash before saving, or a timeout after server acceptance, causes retransmission. There is no transport idempotency key, and duplicate posts are not counted. State-file writes are also non-atomic.

These are log-transport defects, not bus arbitration defects, but they undermine the promised mirror completeness accounting.

### 25. MEDIUM — Existing channels are explicitly reused despite the fresh-channel isolation requirement

**Anchors**
- `code/run_ab2.py`, `c2_channel`: `"fleet-bus-v2-c2-run{run_no}"`.
- `code/run_ab2.py`, `create_mirror_channel`: a `"pre-existing channel ... is tolerated"`, and the function returns the channel regardless of creation success.

Reruns reuse the same channel name and can append events to an existing channel. This is inconsistent with §5’s fresh-channel-only promise and mixes attempt histories. Channel-creation failure is not distinguished from successful creation before posting begins.

---

## Clean portions and verification limits

- **Shared first-generation request path — clean.** `code/workgen.py` re-exports `workgen2`; `workgen2.generate` uses the same cheap-model default, prompt builder, temperature, output cap, and `think: false` for both arms. Task/attempt logging metadata does not alter the request.
- **A/B ladder selection and configured budget — clean.** `arm_c2.model_for_attempt` selects cheap for attempts 1–2 and strong thereafter; `run_ab2.setup_c2` explicitly enqueues with `max_attempts=4`. The standalone Bus/CLI defaults remain three, so this finding applies specifically to the supplied A/B setup.
- **Atomic enqueue/claim serialization — clean in the supplied implementation.** `Bus._mutate` uses `BEGIN IMMEDIATE`; idempotency keys are unique; claim selection and update occur in one transaction.
- **C2 delivered-artifact re-scoring — clean in isolation.** Collection scores the ledger’s done artifact and counts unreadability as shipped-wrong. This does not cure unfenced validation or permissive validators.
- **Coordination generation separation — clean in the visible call sites.** Workers generate with purpose `work`; the mirror contains no model call or ownership arbitration. The logging-completeness findings prevent equating that observation with a fully audited token total.
- **Historical continuity and freeze compliance — not verifiable from the supplied files.** No conclusion is warranted about amendments, the prior core, workload hashes, or actual run discipline.