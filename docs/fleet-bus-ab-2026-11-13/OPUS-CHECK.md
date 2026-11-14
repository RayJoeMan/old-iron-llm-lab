# Checker report: Fleet A/B harness

Line numbers are approximate. Each finding is anchored by function name and a quoted fragment.

---

## (1) Correctness bugs

### arm_a.py

**A1. CRITICAL: `RECLAIM` can never take effect, so Arm A recovery is impossible.**
- **Where:** `live_owner()`, `return cs[0][0]`.
- **Cause:** `channel_state` appends RECLAIM entries to the same `claims[tid]` list as CLAIMs. `live_owner` always returns the first entry, which is the dead original claimant.
- **Scenario:**
  1. ab-w2 holds c3 and is SIGKILLed.
  2. After 150 s, ab-w1 posts `RECLAIM c3`.
  3. `live_owner` still returns `ab-w2`. ab-w1's `mine` never contains c3, so it never does the work.
  4. `first_seen_claim[c3]` is never reset, so every worker sees c3 as stale on every loop. Each loop costs a coord generation and posts another `RECLAIM c3`.
- **Effect on measurements:**
  - The kill-test task is always `lost`.
  - Recovery is always `recovered: False`.
  - `coord_tokens`, `coord_calls` and `coord_messages` are inflated by RECLAIM spam until the 1800 s deadline.
  - `wall_s` hits the cap.
- **Note:** this violates the design requirement "recoverable by a 150 s staleness rule in Arm A".

**A2. HIGH: DONE-id parsing does not match the driver's acceptance check.**
- **Where:** the `text.startswith(f"DONE {tid}")` guard versus `DONE_RE = r"^DONE\s+(\S+)..."`.
- **Scenario 1:** the LLM emits `DONE c1.` or `DONE c1:`.
  - The `startswith` guard passes, but `DONE_RE` keys the post as `c1.`.
  - Task `c1` is never marked done and the worker still owns it.
  - Next loop it redoes the work plus the DONE generation, indefinitely.
- **Scenario 2:** `tid=c1` and the LLM writes `DONE c10…`. This passes the guard and registers a DONE for the wrong task.
- **Effect:** endless repeated work and coord calls. These repeats are never counted as duplicates (see A6/R5), and the task shows as lost.

**A3. HIGH: the `--limit 300` read window truncates channel history.**
- **Where:** `sw(a, "read", ..., "--limit", "300")` in both `main()` and `run_ab.probe_a`.
- **Message budget:** 1 RULES + 18 TASK + about 18 CLAIM + about 18 multi-line DONE, plus RECLAIM spam (A1) and repeated DONEs (A2). This can exceed 300.
- **If the read returns the newest 300:**
  - TASK messages fall out of `tasks`, so workers can hit `all(t in dones for t in tasks)` early and exit.
  - Early DONE posts fall out, so finished tasks appear `lost` in `probe_a`/`collect`.
  - A truncated first DONE under-counts duplicates and changes `first_artifacts`.
- **If the read returns the oldest 300:** new CLAIM and DONE posts become invisible.

**A4. MEDIUM: an exception in `workgen.generate` kills the worker process.**
- **Where:** the `workgen.run_work(...)` and `workgen.generate("coord", ...)` calls are not wrapped in `try`.
- **Effect:**
  - A transient HTTP error or timeout becomes an unplanned worker death.
  - That worker's claim is stranded, and per A1 it is never recovered.
  - It can trigger the "every worker died" early exit in `run_ab`.
  - The tokens of that call are never logged (see T1).

**A5. MEDIUM, latent: staleness has no heartbeat.**
- **Where:** `now - first_seen_claim.get(tid, now) > STALE_S`.
- **Scenario:** once A1 is fixed, a live owner whose work generation plus 900-token DONE generation exceeds 150 s under 3-way contention will be reclaimed.
- **Effect:** this produces real duplicate work that Arm C avoids through heartbeats.

**A6. LOW-MEDIUM: Arm A's scored artifact is the LLM's rewrite, not the work output.**
- **Where:** `text = workgen.strip_think(text)`, posted as the DONE body. `collect` uses `lst[0][1]` from the DONE post.
- **Cause:** the coord model regenerates the result (capped at `num_predict=900`), so it may paraphrase, truncate or re-case it.
- **Effect:** Arm A's `validator_pass_first_attempt` measures the coordination rewrite rather than the work artifact. This is not comparable with Arm C, which scores the raw staging file.

**A7. LOW: claim identity is fragile.**
- **Where:** ownership is decided by `m_sender(m) == a.worker_id`. Kill-victim selection in `run_ab` relies on the same equality.
- **Risk:** if the server reports a display name or user id that differs from `ab-wN`, no worker ever owns anything.
- **Action:** verify the sender identity once.

### arm_c.py

**C1. MEDIUM: an exception in `run_work` kills the worker process.**
- **Where:** `worker_mode`, a `try/finally` around `run_work` with no `except`.
- **Effect:**
  - An HTTP error or timeout kills the process. Lease expiry does recover the task, but the arm silently runs with fewer workers, which confounds `wall_s` and the kill test.
  - The tokens of the failed call are unlogged (T1).
- **Same pattern:** `bus.claim`/`bus.all_terminal` raising `OperationalError` crashes the worker or checker.

**C2. MEDIUM: the checker is a single point of failure and has no restart.**
- **Where:** `checker_mode`; `bus.verdict(...)` and `validators.validate(...)` are not guarded.
- **Effect:** any exception (for example a DB error after the 30 s busy timeout) kills the only checker.
  - All later results sit in `validating` forever.
  - Nothing becomes terminal, so `wall_s` hits the 1800 s cap.
  - The early-exit check ignores the checker, so this is not detected.

**C3. LOW: the heartbeat closure binds late.**
- **Where:** `def hb()` references the enclosing `tid` and `stop_hb`, which are rebound every loop iteration.
- **Scenario:** an old thread that is mid-`heartbeat()` (or still in `Bus()` construction) when `stop_hb.set()` fires re-reads `stop_hb`/`tid` after rebinding. It then keeps heartbeating the next task and leaks a connection.
- **Effect:** benign for the metrics, since the lease belongs to the same worker, but it is a race.

### fleetbus.py

**F1. MEDIUM: `post_result` records late results under the wrong attempt.**
- **Where:** `post_result`; it uses `attempt = task["attempt"]` (the current attempt) and `claimant_match` (claimant only).
- **Scenario:**
  1. c1 holds attempt 1 and its lease is reaped.
  2. c2 claims attempt 2.
  3. c1 posts late. The row is stored as `(task, attempt=2, c1, late=1)`.
- **Effect:**
  - Per-attempt analysis is wrong.
  - If c2 also posts, the two rows are not distinguishable by attempt.
- **Root cause:** the worker's held attempt is never passed in or checked.

**F2. LOW: the heartbeat can resurrect an expired lease.**
- **Where:** `heartbeat`.
- **Cause:** it does not check `lease_expires_at >= now`. A worker that stalled past 150 s and then heartbeats before the next 5 s reap revives its lease.
- **Effect:** the window is small, but this is a state-machine hole.

---

## (2) Token counting

**T1. MEDIUM: failed calls are uncounted in all arms.**
- **Where:** `workgen.generate`; the call-log entry is written only after a successful `urlopen` and parse.
- **Effect:** a timeout or error after the server has already generated is consumed but never logged.
- **Related crashes:** worker-crash paths C1 and A4.

**T2. MEDIUM: cache-dependent prompt counts.**
- **Where:** `prompt_eval_count`.
- **Cause:** Ollama reports only newly evaluated prompt tokens when the KV prefix is cached, and may omit the field (which becomes 0).
- **Effect:** Arm A's repeated coord prompts share long prefixes, so its coord tokens are systematically undercounted relative to its work tokens and to the other arms.
- **Action:** count `prompt_chars` alongside, or disable prompt caching.

**T3. LOW: anything not tagged `coord` counts as work.**
- **Where:** `collect`, the `else: work_tokens += tot` branch.
- **Effect:** an untagged or mistagged call is silently counted as work.
- **Arm C status:** clean today. `arm_c.py` makes no model calls outside `run_work`, and the checker is deterministic. Arm C coordination has zero generations, as required.

**T4. MEDIUM: cross-arm asymmetry in work tokens.**
- **Cause:** Arm C re-runs work after validation failure (`verdict` → `queued`, up to 3 attempts). Arm A and Arm B (as orchestrated) do not.
- **Effect:** Arm C's `work_tokens` and `work_calls` include retries that the other arms never spend.

---

## (3) Lost or duplicated tasks going uncounted (or miscounted)

**R1. HIGH: dead tasks are counted as terminal, not lost.**
- **Where:** `probe_c`, `done_ids = {... if v in ("done", "dead")}`.
- **Effect:**
  - A task that exhausts attempts (validation failures or repeated reaps) is excluded from `lost`.
  - It also gets a `completion_ts`.
  - If it is the kill task, `recovery` reports `recovered: True`.

**R2. HIGH: Arm C's "duplicated work" includes legitimate validation retries.**
- **Where:** `probe_c`, `results` counts rows per `idem_key`. In `collect`, `n > 1` means duplicated.
- **Scenario:** attempt 1 fails validation and attempt 2 passes. That gives 2 result rows, reported as duplicated.
- **Effect:** this inflates Arm C's duplication relative to Arm A, which has no retry path.
- **Action:** filter on `late=1`, or count rows per attempt.

**R3. HIGH: "terminal" means different things per arm.**
- **Definitions:**
  - Arm A: any DONE post, unvalidated.
  - Arm C: checker-passed (or dead).
- **Effect:**
  - `wall_s`, `completion_ts`, and the "6 completions" kill trigger are not comparable.
  - The kill fires at different real progress points in each arm.

**R4. MEDIUM: the kill target is taken from a stale snapshot.**
- **Where:** `run_ab.main`, the `for tid, wid in sorted(claimed.items())` loop.
- **Cause:** the `claimed` snapshot can be more than 2 s old.
- **Scenario:** the victim has already posted and claimed a different task.
  - `kill_info["task"]` names a task that was never lost, so it reports recovered with meaningless latency.
  - The task actually orphaned is untracked.
- **Second scenario:** if nothing is claimed, the fallback kills `sorted(procs)[1]` with `task=None`, giving `recovery=None`. The kill test silently produces no recovery measurement.
- **Arm A:** the SIGKILL does not kill an in-flight `swarmchat` child, which may still deliver a CLAIM or DONE.

**R5. MEDIUM: Arm A duplicates are keyed on the parsed id.**
- **Where:** `collect`, the `len(lst) > 1` check over `dones`.
- **Missed duplicates:**
  - A2 variants (`c1.` versus `c1`) split into separate keys.
  - Re-work after a failed DONE `send` produces no second post.
  - DONEs truncated by A3 disappear.

**R6. HIGH: reruns into an existing run dir contaminate everything.**
- **Where:** `run_ab.main`, `os.makedirs(run_dir, exist_ok=True)` with no cleanup.
- **Contamination by file:**
  - **`bus.db`:** reused. `enqueue` returns the existing ids, so already-done tasks complete instantly.
  - **`call_log.jsonl`:** appended, so tokens are double-counted.
  - **`first_verdicts.jsonl`:** pre-loaded into `seen_first`, so new first verdicts are suppressed.
  - **`staging/`:** leftover files can become `first_artifacts`.
- **Arm A:** reuses the channel name `fleet-bus-ab-a{run}`, so old DONEs mark tasks done immediately.

---

## validators.py

**V1. MEDIUM: false `FOREIGN_NUMBER` on percentages.**
- **Where:** `_numbers()` keeps `%` attached.
- **Scenario:** the snippet says `10%` and FACTS says "10 percent". `10` is not in `{"10%"}`, so the draft fails as `FOREIGN_NUMBER`.
- **Effect:** this applies to every arm, but in Arm C each false fail triggers a retry. That feeds R2, T4, and possibly a `dead` task (R1).

---

## workgen.py

No issues beyond T1 and T2.