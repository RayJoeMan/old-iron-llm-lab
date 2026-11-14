# Fleet Bus A/B — PRE-REGISTERED DESIGN

**Filed:** Nov 13, 2026, before any build or run. Changing anything in §§2–6 after this filing requires a written amendment in the run ledger with the reason, per the spec's freeze discipline.
**Commissioned by:** Joe, Nov 13, 2026 (15:05 CT) — "design and run the Fleet Bus A/B", Fleet Dashboard build pattern.
**Governs:** the Fleet Bus spec at `~/workspace/your_files/fleet-bus-spec-2026-11-12/SPEC.md`.

## 1. Reconciliation with spec §4 (read this first)

The spec's §4 (written Nov 12) pre-registered an A/B with different arm assignments: Arm A = incumbent relay re-run, Arm B = SwarmChat's *recorded* pilot numbers (not re-run), Arm C = Fleet Bus, on the pilot's 24-brief sweep. Joe's Nov 13 commission re-specifies the test, and — as the spec's own freeze clause requires a ruling to change §4 — **this commission is that ruling**:

| | Spec §4 (Nov 12) | This design (Joe, Nov 13) |
|---|---|---|
| Arm A | Incumbent dispatch/relay, re-run | **SwarmChat, re-run live** on Fortress |
| Arm B | SwarmChat recorded numbers (10,287 coord tokens / 27,225 s) | **File queue** — the fleet's current de facto discipline, re-run live |
| Arm C | Fleet Bus | **Fleet Bus prototype** (unchanged) |
| Workload | Pilot's 24 research briefs | **Mixed fleet batch** (§3), sized for spare capacity |
| Bars | §4.4, vs Arm A only | §6 below — the bus must beat **both** live incumbents |

Carried over from the spec unchanged in substance: the §4.3 mechanics gate (Arm C must pass it before its A/B numbers count), the zero-missed / zero-duplicate hard gates, score-strictly-as-measured, and §4.4's clause that a split result is a fail. The spec's §4.5 real-work shadow is **deferred, not dropped**: Nov 13 is the Mint's experiments-only day and the commission's hard constraint is to disturb no production work; the shadow is the first follow-up if the bus is adopted. Decisions 3–5 (open, Joe's): where this prototype needs one, the spec's recommended default is used and marked **PROVISIONAL** — D3: experiment/synthetic work only (this A/B's workload only); D5: working name "Fleet Bus", built by Nyx's integration under the tandem-coder pattern. Neither is presented as decided.

## 2. Arms

All three arms run the **same workload** (§3), the **same work-generation code path** (one shared module calling Fortress Ollama), the **same model and settings** (§3.2), and **3 workers** each. Only the coordination mechanism differs.

- **Arm A — SwarmChat (live).** The production SwarmChat server on Fortress (`100.103.255.114:8484`, the R22 runway instance) with a fresh channel per run; its existing chats and data are never touched. **Amendment at setup (Nov 13, before any run):** the original plan for fresh A/B-only identities was reversed by the server's live policy — channel creation and the contacts roster are restricted to the pilot roster (the D4 design working as intended), so four fresh `ab-*` users were created, found unable to create channels, and **removed** again. Arm A instead runs on the server's own roster, exactly as the Nov 11 pilot's A/B did: operator = `pilot-admin`, workers = `cc-fortress`, `codex-fortress`, `aider-fortress` (scripted drivers under those identities, per the pilot's S0c substitution). Their tokens were copied on-box into the A/B token directory (0600, never printed or moved off-box). This measures the incumbent *as configured*, which is the fairer test anyway. Coordination is the pilot's peer pattern, faithfully replicated: a worker reads the channel, spends **one LLM generation per coordination event** (claim choice, done post, reclaim) over the recent channel tail, and posts the resulting message. A deterministic guard in the driver (not the model) enforces claim validity: the earliest live claim owns the task; later claims for the same task are void. Claim staleness rule, fixed here in advance: a claim with no DONE after **150 s** may be reclaimed by another worker via a RECLAIM generation.

  **Arm A runtime pin (Joe's direction, Nov 13):** SwarmChat is **not** ported or patched for this test. Its upstream suite fails on Fortress's Python 3.14.4 (5 failures + 1 error in `test_by_hand.py`; filed as F-66) while passing 186/186 on the Mint's Python 3.12 — so Arm A's client runs in a pinned **Python 3.12** venv on Fortress (installed from the vendored 0.1.0 wheel), measuring the incumbent in its known-passing configuration. The 3.14 suite failures are recorded here as context on the incumbent, and the runtime pin itself is noted as part of SwarmChat's deployment cost were it adopted as the fleet bus: it carries a Python-version constraint the file queue and the Fleet Bus prototype (stdlib, version-agnostic) do not.
- **Arm B — File queue (the de facto discipline).** A run directory with `queue/ claimed/ results/ done/`. Claim = move the oldest task file under a single `flock` lockfile, recording claimant + timestamp. Each worker runs a sweeper that requeues claims stale by **150 s** (the Fortress chains' skip-if-done + relaunch discipline, automated). Result = file in `results/`; the claim file then moves to `done/`. Run completes when all 18 task files are in `done/`. Zero coordination generations.
- **Arm C — Fleet Bus prototype.** Minimal implementation of the spec §3: SQLite (WAL) ledger per run, atomic claim with lease (150 s) + heartbeat (20 s), idempotency keys on enqueue and on result posting, results land in `validating` and merge only on a **checker pass** (the same deterministic validators as the other arms, run by a separate checker process), a reaper process expiring stale leases, an append-only JSONL event log written in the same transaction order, and a `run.complete` sentinel written only when every task is terminal. Zero coordination generations, verified by the generate-call log (§5), not asserted.

Prototype scope notes (test article, not production): runs as OS user `general` in `~/fleet-bus-ab/` on Fortress, removable with one `rm -rf`; the ledger has **no network listener at all** (CLI/local only — tailnet-only by construction); the spec §3.9 dedicated-user + systemd hardening is production-phase work if adopted, recorded here as a known prototype deviation.

## 3. Workload (frozen)

18 tasks, defined in `workload.json` (sha256 recorded in the run ledger at build time; gold answers live only in the validator copy, never in worker payloads beyond what the task itself presents):

- **6 × CLASSIFY** — a content title → exactly one label from {TEACHING, COMEDY, GRAPHIC-NOVEL ACTION, SPOT-THE-MISTAKE, SEASONAL} (the fleet's real classification lanes). Validator: extracted label == gold label.
- **6 × DRAFT** — a topic + a source snippet containing specific numbers → a card with fixed fields TITLE / SOURCE / FACTS / SUMMARY. Validator (the pilot's fixed-field pattern): all fields present, every number printed in FACTS appears in the source snippet, no URL other than the named source, SUMMARY ≥ 120 chars.
- **6 × VERIFY** — a short paragraph + 3 claims → SUPPORTED/UNSUPPORTED per claim, in order. Validator: all three verdicts == gold.

### 3.1 Workers and generation
3 worker processes per arm. Every work generation in every arm goes through the identical function: HTTP POST to Fortress Ollama `/api/generate`, model **`qwen3:4b`**, `temperature 0.3`, `num_predict 1200`, thinking disabled. Token counts are taken from Ollama's own response counters (`prompt_eval_count`, `eval_count`) — never estimated.

**Amendment at smoke (Nov 13, before any timed run, reason recorded per the freeze rule):** `num_predict` was filed as 512 and is amended to **1200**. The pre-run smoke (3 tasks through Arm C's full path) showed qwen3:4b's reasoning — which this Ollama build leaks into the response untagged, the fleet's known Qwen3 quirk — consuming the entire 512-token budget before any answer was emitted (2 of 3 smoke tasks produced zero answer content). At 512 the workload itself is unmeasurable in every arm; 1200 restores the pilot's regime (900) plus headroom and is identical across arms. Coordination-generation caps in Arm A were set in the same pass (claim 256, DONE 1200) for the same reason.

**Amendment 2 (same smoke window, same rule):** work `num_predict` 1200 → **1600** (DRAFT reasoning was still consuming 1200 without reaching the card on the second smoke), Arm A DONE-generation cap set to **800**, and the per-run cap (§5) raised from 30 min to **60 min**. Measured context: during the smoke window the box was at load average ~47 (F2's six-server phase + the YOLO dual pass + an Ollama runner at ~1300% CPU), and effective generation throughput was ~13 tok/s. The caps exist to bound runs, and at the smoke settings they would have bound on harness parameters rather than on the systems being compared; the amendment keeps the comparison about coordination. All values remain identical across arms.

### 3.2 Runs
**2 runs per arm.** Task order shuffled per run with fixed seeds (run 1: 20261113, run 2: 20261114). Arm order counterbalanced against box contention: run 1 = A, B, C; run 2 = C, B, A. Environmental contention (F2 chain, YOLO dual pass, other fleet work) is disclosed in the results, charged to no arm.

## 4. Kill test (pre-registered, run 1 of each arm)

After the **6th task completion** is recorded in an arm's run 1, the operator SIGKILLs one worker process — the one holding the oldest in-flight claim, or worker #2 if none is in flight. Measured per arm: whether the killed worker's task completes, whether it is duplicated, the recovery latency (kill → that task's completion), and whether recovery happened through the arm's own machinery or needed the operator. Run 2 of each arm runs unkilled as the clean control.

## 5. Metrics (counted by these rules, from first-hand records)

1. **Wall time** per run: first claim-able moment → last task terminal, from the harness's own timestamps.
2. **Tasks lost**: accepted by the arm, never terminal at run end (run ends at all-terminal or a 60-minute cap — raised from 30 by Amendment 2; hitting the cap is itself reported).
3. **Tasks duplicated**: merged/completed more than once for the same task id.
4. **Recovery**: kill-test outcome + latency (§4).
5. **Coordinator interventions**: any action by the operator beyond launching the arm and the pre-registered kill — each counted and described. Automated machinery inside an arm (sweepers, reapers) is not an intervention.
6. **Coordination overhead**: (a) LLM tokens spent on generations whose purpose is coordination, summed from Ollama counters — every Ollama call in every arm is logged with a purpose tag (`work` / `coord`), so B's and C's zero is a counted zero; (b) coordination message count and total bytes (SwarmChat posts; file moves; ledger ops) as the secondary measure.
7. **Validator pass rate**: the shared deterministic validators, per task type and total.
8. **Work tokens** per arm (context only; not a bar).

## 6. WIN BAR — falsifiable, all legs must hold

Fleet Bus (Arm C) is adoption-justified **iff**, on the aggregate of the 2 runs:

1. **Hard gate:** Arm C lost = 0 **and** duplicated = 0, in **each** run individually.
2. **Coordination tokens:** Arm C ≥ 30% below Arm A **and** Arm C coordination-generation tokens = 0 exactly (its by-construction claim, counted). Any coordination generation inside Arm C fails this leg.
3. **Wall:** Arm C aggregate wall ≤ 1.10 × Arm B aggregate wall **and** ≤ 1.10 × Arm A aggregate wall. (Arm B is expected to bind; Arm A is named so the bus cannot win on a technicality against the slow arm only.)
4. **Interventions:** Arm C ≤ Arm A and ≤ Arm B.
5. **Quality:** Arm C validator pass ≥ Arm A and ≥ Arm B in aggregate, and worse than neither in any single run by more than 1 task.
6. **Mechanics gate (§7) passes in full** before the A/B numbers are counted.

A split result is a **fail** (spec §4.4 clause). If the bar fails, the recommendation filed with the results is: file-queue discipline stays the fleet's coordination method, SwarmChat stays as proven durable-log plumbing, and this design + record are filed as a tested-and-refuted (or tested-and-split) design. **Adoption is Joe's ruling either way; nothing in this A/B replaces any live system.**

## 7. Mechanics gate (Arm C only, before its A/B numbers count)

Per spec §4.3, at claim-layer scale, on Fortress:
1. **Claim flood:** 1,000 synthetic no-op tasks, 8 concurrent claimants claiming + completing: exactly 1,000 tasks, every task claimed exactly once, all terminal.
2. **Duplicate-enqueue storm:** the 18-task batch enqueued twice, concurrently, from two processes → exactly 18 tasks (idempotency-key collisions return the existing task).
3. **Kill/restart:** during a 100-task flood, SIGKILL the reaper daemon and one worker mid-task, restart the daemon → zero tasks lost, zero duplicated merges, all leases recovered without operator action.
4. **Reconciliation:** an independent replay of the JSONL event log reproduces the ledger's per-state counts exactly.

## 8. Safety and isolation

The A/B's workers, tasks, channels, and stores are its own. The kill test kills only A/B worker processes, identified by PID at launch. Nothing touches: the F2 funnel chain, the YOLO dual pass, Mint anything, the backup migration, the dashboards, SwarmChat's pre-existing users/chats/data, or any live queue. SwarmChat A/B identities are created fresh for this test; their tokens live only on Fortress in 0600 files under the A/B run directory and are never printed, copied off-box, or recorded in any report. All workload content is synthetic and non-sensitive.

*Design ends. Filed before build.*
