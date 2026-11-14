# Independent design check — Claude Opus 5.5

**Checker:** claude-opus-5-5 via the custom.anthropic connector. **Date:** Nov 14, 2026.
**Input:** the identical blind packet given to both checkers — filed DESIGN.md + the v2 harness code (fleetbus2.py, workgen2.py, workgen.py, arm_c2.py, mirror.py, run_ab2.py, gate_c2.py, arm_b.py, validators.py), ~100 KB. The checker did not see the other checker's review.
**Call record:** input 39,230 tokens / output 26,105 (19,733 thinking), stop=end_turn, 258 s. Two earlier attempts at a 64,000-token cap dropped at ~271 s each (RemoteDisconnected, an upstream duration cutoff); the successful call used a 32,768 cap. Spend on the dropped attempts is uncertain and is not counted here.
**Dispositions:** ADJUDICATION.md (alongside). This file is the checker's verbatim output.

---

# Independent Check: Fleet Bus v2 A/B Harness

**Scope:** DESIGN.md against fleetbus2.py, arm_c2.py, mirror.py, run_ab2.py, gate_c2.py, workgen2.py/workgen.py, arm_b.py (incumbent, judged as-is) and validators.py.

**Bottom line:** I found no defect that crashes a normal run.

- **Bar-relevant accounting holes:** There are three. Arm B can count a task as delivered without an artifact. The leak metric uses different definitions per arm. B's duplication and first-attempt numbers can be silently undercounted.
- **Mechanics gate:** As written, the gate never exercises the code v2 changed.
- **Unimplemented design items:** Several filed items are missing in code: the defer rule, `LEASE_EXPIRED_FINAL`, per-task budget reporting, the counterfactual, and interventions.

---

## HIGH

### H1. Arm B can count a task as done with no artifact, and it is never scored as shipped-wrong

**Where:** `arm_b.py main()` and `run_ab2.py collect()` (B branch).

- If the results write fails, arm_b swallows it and still promotes the claim to `done`:
  - `except OSError: pass` / `except Exception: pass` around `json.dump(...)`
  - followed unconditionally by `os.rename(claimed_path, done_path)`.
- In collect:
  - `terminal = done_ids` (from `done/` filenames).
  - `shipped_wrong` iterates only over `delivered.items()`.
  - A done task with no result file is therefore not lost, not shipped-wrong, and counts toward B's "accounted" total (WIN BAR leg 2).

**Second silent drop:** the result-file parse in collect swallows every error.

- `except Exception: pass` after `rec = json.load(open(pth))`.
- A truncated or unparseable result (arm_b's write is non-atomic) is dropped from `delivered` without notice.

**Contrast with C2:** C2 counts an unreadable merged artifact as shipped-wrong (`except Exception: shipped_wrong.append(tid)`). The arms are therefore scored asymmetrically.

**Likelihood:** Low in practice, but structurally unaccounted.

**Missing check:** No reconciliation asserts `done_ids == delivered.keys()`.

### H2. The leak-flag metric has different definitions per arm, and design §4.2/§6.1 is not met for B

**Where:** `run_ab2.py collect()`.

- **B:** `extra["leak_flagged_calls"] = sum(1 for e in work_entries if e.get("eval_count", 0) >= LEAK_EVAL_FLOOR)`.
  - This counts every budget-burning call, including ones that passed validation or failed for non-structural reasons.
- **C2:** requires `not v.get("passed") and STRUCTURAL_REASONS & set(v.get("reasons", []))`.

**Effect:** B's count is inflated relative to C2's by construction.

**Design conflict:**

- §4.2 says the metric is "Counted per arm … joined to verdicts by task + attempt (the v2 call log carries both fields)."
- §6.1 says the extended call log "Applies to both arms equally."
- Neither holds: arm_b calls `workgen.run_work(task, call_log_path, run_tag)`, so B's entries carry `task: None, attempt: None`.

**Disclosure gap:** The code comment ("counted at call level for this arm") is a post-filing definition change. It needs an amendment and must not be compared head-to-head with C2.

### H3. The mechanics gate never exercises the policy code v2 changed

**Where:** `gate_c2.py`.

What the gate actually covers:

- All sim checkers pass: `bus.verdict(t["id"], cid, True, "")`. So `FAIL_REQUEUE`, `DEADLETTER` and the `max_attempts` boundary are never hit.
- All gate enqueues use the default `max_attempts=3` (`bus.enqueue(f"k-{i}", "NOOP", {})`). The v2 budget of 4 is never tested.
- Leg 4 replays only `flood.db` ("reconcile the flood db from leg 1"). That log contains only ENQUEUE/CLAIM/RESULT/MERGE.
  - The new replay mappings `"DEADLETTER": "deadletter"` and `"DEADLETTER_LEASE": "deadletter"`, plus `REAP`, are never exercised.
  - `leg3`'s DB, which does contain REAPs, is not reconciled.
- `DEADLETTER_LEASE` cannot occur in leg 3. Killed-worker tasks are at attempt 1 < 3.
- The reaper's DLQ path would raise `AttributeError` anyway, because `reaper_proc`'s stub lacks `run_dir`. That error is swallowed by `except Exception: pass` in `reaper_mode`.

**Effect:** A gate pass (WIN BAR leg 8) certifies the unchanged v1 mechanics only. It does not certify the renamed terminal state or the ladder.

---

## MEDIUM

### M1. Arm B duplication and "first attempt" are invisible when the same worker reruns a task

**Where:** `arm_b.py main()` and `run_ab2.py probe_b()` / `collect()`.

- Result filenames are `taskid + "__" + worker_id + ".json"`. A sweep-and-requeue reclaimed by the same worker overwrites the earlier file.
- Consequences:
  - `probe_b` (`results[tid] = results.get(tid, 0) + 1`) sees one file, so the duplication is uncounted.
  - `first_artifacts` (earliest by mtime) actually holds the later attempt.
  - B's call log is untagged, so tokens cannot reveal the extra call per task.
- C2's equivalent is fully attributed through the `results` table.

**Bar impact:** B duplication is not a bar leg, but `validator_pass_first_attempt` is compared across arms and against v1.

### M2. B can score lost tasks as shipped-wrong; C2 never does

**Where:** `run_ab2.py collect()`.

- `delivered` is built from every file in `results/`, regardless of whether the task reached `done/`.
- Scenario: a worker is killed between writing the result and the rename, and the requeued task is not finished before the cap. That task lands in both `lost` and possibly `shipped_wrong`.
- C2 re-scores only `WHERE state='done'`.

**Fix needed in the rule:** §3.3 says "the artifact the arm delivers as its successful result." The code needs a filed rule for non-done tasks.

### M3. `LEASE_EXPIRED_FINAL` is not implemented, and DLQ records omit attempts without results

**Where:** `fleetbus2.py reap()` and `arm_c2.py write_deadletter()`.

- `reap()` final-attempt branch: `"UPDATE tasks SET state = 'deadletter' WHERE id = ?"`.
  - No reason is written, contradicting §3.1 ("deadletters with reason `LEASE_EXPIRED_FINAL`").
  - Claimant and lease fields are not cleared.
- `write_deadletter` builds `attempts` only from `results` rows. Attempts lost to a generation error, a kill, or lease expiry (including the final one) are simply absent.
- §3.2 requires "every attempt's worker, model rung, artifact path, and validator reasons."
- The docstring claims "Idempotent", but the `deadletter.jsonl` append duplicates lines on repeat calls (LOW on its own).

### M4. Transport errors become dead-letters in C2 but retry forever in B (undisclosed asymmetry)

**Where:** `arm_c2.py worker_mode()` vs `arm_b.py main()`.

- **C2:** a `run_work` exception abandons the claim ("the reaper recovers the task at lease expiry"). This consumes an attempt and shortens the cheap rung. On attempt 4 it becomes `DEADLETTER_LEASE`, which counts against the DLQ cap (leg 4).
- **B:** `except Exception: continue` leaves the claim to the sweeper, with no attempt cap.

**Effect:** An Ollama hiccup penalises C2's DLQ count. A persistent failure penalises B's wall instead. The design does not mention either effect.

### M5. A late result on the final attempt counts as duplication, and a valid artifact is discarded

**Where:** `fleetbus2.py reap()` / `post_result()`.

Sequence:

1. After a reaper deadletter, `claimant` and `attempt` are unchanged, so a slow worker's post has `claimant_match` True.
2. The state check `task["state"] in ("claimed", "validating")` fails.
3. The post falls through to the `late=1` insert.
4. `probe_c2` counts `WHERE r.late=1` as duplicated work.

**Effect:** This can fail the C2 hard gate (leg 1) even though only one generation of that attempt ever happened. The task is also deadlettered despite a deliverable artifact existing.

**Likelihood:** Rare, since it requires heartbeat failure, but it is a mis-accounting.

### M6. Kill-test victim selection differs from §7

**Where:** `run_ab2.py main()`.

- `for tid, wid in sorted(claimed.items())` picks the alphabetically-first task id, not the oldest in-flight claim.
  - C2 has `claimed_at` available.
  - B has the file mtime, although heartbeats refresh it.
- The fallback `sorted(alive)[0]` picks worker #1, but §7 says "worker #2 if none in flight."
- Related LOW items:
  - `recovered: True` is set whenever `kt in completion_ts`, which for C2 includes a deadletter.
  - Nothing restricts `--kill-test` to run 1.

### M7. The defer rule is not implemented

**Where:** `run_ab2.py main()`.

- §4.3 says that if 1-min load exceeds 30, the run "waits and re-checks."
- The code only records `pre_load = read_loadavg()` and proceeds.
- There is no guard and no record of re-checks. Compliance therefore depends entirely on the operator and is not evidenced in metrics.

### M8. A mirror setup failure can fail the C2 run, and mirror shortfall goes unreported when it matters

**Where:** `run_ab2.py create_mirror_channel()` and `mirror.py`.

- **Setup can abort the run:** `with open(os.path.join(swarm_base, "tokens", "pilot-admin.token"))` sits outside the `try`.
  - A missing token file or swarm-base raises in the orchestrator before workers launch.
  - This contradicts §5: "A mirror failure cannot fail the bus."
- **Metrics lost on termination:** the orchestrator waits 120 s, then calls `v.terminate()`. mirror.py has no SIGTERM handler, so `mirror_metrics.json` is never written and `extra["mirror"] = None`.
  - This happens exactly when the mirror is lagging (a SwarmChat outage) or the run hit the cap. Those are the cases §5 says must be disclosed.
- **Counters reset on restart:** they reinitialise (`posted = 0`, `errors = 0`) while `last_seq` is restored (LOW).

### M9. The SwarmChat token is exposed on the process command line

**Where:** `mirror.py main()` and `run_ab2.py create_mirror_channel()`.

- Both call `[swarm_bin, "--json", "--server", SERVER, "--token", token, ...]`.
- The token is readable by any local user via `ps` or `/proc/*/cmdline` for every event post.
- This defeats the "0600 files, never printed" handling in §5/§11 in spirit.

### M10. Filed metrics are missing from collection

**Where:** `run_ab2.py collect()`.

Not computed anywhere:

- Per-task token/budget reporting (§3.1: "reported per task from the call log").
- DLQ pricing in "wall + tokens spent reaching them" (§3.2).
- The gate-caught counterfactual (§3.3).
- Calls split by model; only tokens are split (`work_tokens_by_model`) (§8).
- Coordinator interventions (§8, leg 7).

Also, C2's `coord_messages` counts ledger events only, whereas §8 says "ledger events + mirror posts."

### M11. The checker can livelock a task to the cap

**Where:** `arm_c2.py checker_mode()`.

- On a validator exception, `print(f"checker: validate crashed ..."); continue` issues no verdict.
- The task stays `validating` and is re-claimed after the v-lease expires. A deterministic crash repeats indefinitely, and the task ends as lost after 60 minutes.
- `meta = tasks[logical]` is outside any `try`, so a KeyError kills the only checker. No process supervises it, and the reaper does not handle validation leases.

### M12. Gate kill leg differs from design and under-asserts

**Where:** `gate_c2.py leg3()`.

- `reaper.terminate()` / `workers[0].terminate()` send SIGTERM; §10 specifies SIGKILL.
- "mid-task" is not ensured.
- Pass is `counts["done"] + counts["deadletter"] == 100 and dup_merge == 0`. It does not assert:
  - `reaps >= 1` (that a lease was actually recovered), or
  - `deadletter == 0`, which §10 states is expected.

### M13. A possible mechanics change in `post_result` must be visible in the filed diff

**Where:** `fleetbus2.py post_result()`.

- The comment "The result is attributed to the attempt the WORKER held when it claimed (passed in)…" plus the `attempt=None` parameter suggest a behaviour change in result posting.
- §3 asserts result-posting mechanics are "untouched." I cannot verify this without v1.
- The diff in the run ledger must show this. If it is new, it needs an amendment.
- Note that the gate's `sim_worker` calls `post_result(t["id"], wid, "noop", "sha", 0)` without `attempt`, so the new path is untested.

---

## LOW

- **`fleetbus2.py verdict()`:** It does not check `v_claimant == checker` or that the validated attempt is still current. This is safe only because there is exactly one checker.
- **`run_ab2.py collect()` (C2):** Re-scores `open(rp).read()` without comparing it to the ledger's `result_sha`. The checker does not verify the sha either. The "shipped-wrong = 0 by construction" check is therefore nearly tautological. A sha mismatch would be the actual checker-defect signal.
- **`run_ab2.py calibrate()`:** C2 calibrates `[MODEL_CHEAP, MODEL_STRONG]` in that order, so the 8b is the last model loaded. If VRAM can't hold both, C2's first rung-1 calls pay a reload that B doesn't. This is a small wall asymmetry. Both arms also calibrate on a scored DRAFT prompt, which may help via the prompt cache (symmetric).
- **`run_ab2.py main()`:** `t0 = time.time()` is set after all `Popen`s, so workers can claim before wall starts. C2 launches more processes first (mirror after workers). The effect is negligible but the timing is not "first claim-able moment."
- **`run_ab2.py probe_b()` / `_logical()`:** `stem.rsplit("_", 1)[-1]` assumes workload ids contain no `_`. C2 staging parsing assumes no `__`. Verify against workload.json; if ids contain `_`, B's `done_ids` and `lost` are wrong.
- **`run_ab2.py`:** `"tasks_terminal": len(terminal)` excludes deadletters for C2 (naming only). No "accounted" field is emitted for leg 2.
- **`run_ab2.py main()`:** A re-executed run silently renames the old run (`.bak-`) and posts to the pre-existing channel. This breaks §5's "fresh channel." It is disclosed only in `channel_setup.json`.
- **`gate_c2.py leg1()`:** Uses 6 claimants plus 2 checkers; §10 says "8 concurrent claimants."
- **`arm_c2.py worker_mode()`:** `with open(path, "w") as f: f.write(artifact)` is outside the `try`. An OSError kills the worker while its claim is held. B uses `json.dump`, which escapes non-ASCII.
- **`run_ab2.py main()`:** `shutil.copy(... "workload.json" ...)` puts gold into every run dir that workers can read. §4.1 says gold lives "only in the validator copy." The models never see it, so the impact is nil.
- **DESIGN.md:** §4.3 and §9 leg 5 reference "§4.4," which does not exist. Counterbalanced arm order is not enforced by code.
- **`arm_c2.py reaper_mode()`:** `if bus.all_terminal(): break` sits outside the `try`, so an exception there kills the reaper.

---

## Clean

- **fleetbus2.py core mechanics** (claim, enqueue idempotency, heartbeat, `_mutate` transactions with `BEGIN IMMEDIATE`, `all_terminal`, `counts`): correct as written. Early returns inside `_mutate` commit properly.
- **Coordination tokens = 0 for C2:** The only model call path is `workgen2.run_work` (`purpose="work"`). The mirror and checker make no generations. Calibration uses a separate log. Untagged purposes fail collection loudly.
- **First-attempt request bodies:** Identical across arms. B's default `MODEL = "qwen3:4b"` produces the same body as C2's rung-1 `model_for_attempt`. Payloads come from the same workload, through the same `build_prompt` and `strip_think`.
- **Ladder mapping:** `CHEAP_MAX_ATTEMPT = 2` matches §3.1.
- **validators.py:** A single shared validator is used for both arms' scoring and the C2 checker, so it is symmetric. I found no defect affecting comparability.
- **C2 lost/deadletter/done accounting in `probe_c2`:** Correct against the ledger.
- **probe_c2 duplicate-row queries:** They do not double-count under the current state machine.