# Fleet Bus A/B — Run Ledger

**Design:** `../design/DESIGN.md` (pre-registered, filed before build). **Spec:** `~/workspace/your_files/fleet-bus-spec-2026-11-12/SPEC.md`. **Commissioned:** Joe, Nov 13, 2026.

## Build record (Nov 13, 2026)

Build pattern (Joe's Nov 13 standard): tandem coders + independent checker + integrator.

| Piece | Author | Notes |
|---|---|---|
| `fleetbus.py` (ledger core: SQLite WAL, atomic claims, leases/heartbeats, idempotency, reaper, JSONL event export) | DeepSeek (`deepseek-flash`) | First call burned its full 20K output cap on reasoning and returned empty; second died on a truncated HTTP response (balance verified unchanged, $18.06); third delivered (~19.7K chars, 27,666 completion tokens). |
| `workgen.py` (shared generation path + call log), `validators.py` (deterministic validators) | Muse Spark 1.3 | 15,628 tokens. Self-test + integrator spot checks pass. |
| `arm_b.py` (file-queue worker/sweeper) | Muse Spark 1.3 | First call died on an SSL timeout; retry delivered (11,834 tokens). |
| `arm_a.py` (SwarmChat worker driver), `arm_c.py` (bus worker/checker/reaper), `run_ab.py` (orchestrator), `gate_c.py` (mechanics gate), workload | Nyx (integrator) | Token handling for Arm A kept in the integrator's hands by design. |
| Independent check of the integrated code | Claude Opus 5.5 (`claude-opus-5-5`) | Full text: `../design/OPUS-CHECK.md`. 22,459 input / 15,256 output tokens. |

### Opus findings and their disposition (all fixed before any run, unless noted)

- **A1 CRITICAL — Arm A RECLAIM could never take effect** (ownership always returned the first claimant; a killed worker's task would be lost and RECLAIM spam would inflate coord tokens to the cap). Fixed: `live_owner` now resolves the ordered claim events; a RECLAIM displaces a stale owner (>150 s by message timestamp). This is exactly the failure the pilot's Arm B never got to exhibit because its mechanics never engaged.
- **A2** DONE-post id parsing mismatches (`DONE c1.` / `DONE c10`) → posted DONE is now always driver-formed `DONE <id>` + verbatim artifact; the DONE generation still happens and is metered (see disclosure D-2 below).
- **A3** Channel read window `--limit 300` could truncate history → 1000 (server max_page).
- **A4/C1/C2** Unguarded generation/DB calls could kill a worker or the single checker → try/except + continue in arm_a worker, arm_c worker, arm_c checker.
- **C3** Heartbeat closure late binding → tid/stop captured as defaults.
- **F1** Late results booked under the wrong attempt → `post_result` takes the worker's held attempt; arm_c passes it.
- **F2** Heartbeat could resurrect an expired lease → heartbeat only extends a live lease.
- **R1** Arm C `dead` tasks counted as terminal (hiding losses, faking kill recovery) → dead counts as lost; completion = `done` only.
- **R2** Arm C "duplicated" included sanctioned validation retries → duplicated = late result rows + same-attempt duplicate rows only.
- **R4** Kill victim chosen from a 2 s-stale snapshot → fresh probe inside the kill branch.
- **R6** Reruns into a dirty run dir would contaminate every metric → orchestrator renames any pre-existing run dir to `.bak-<ts>`.
- **V1** Validator false FOREIGN_NUMBER on percentages (`10%` vs `10 percent`) → numbers compare %-agnostically.
- **T1** Failed model calls went unlogged → workgen logs an error entry (0 tokens, error text) before re-raising.
- **Disclosed, not "fixed" (properties of the systems, recorded here):**
  - D-1 (A5): Arm A has no heartbeat primitive — a slow-but-live owner can be reclaimed after 150 s. Intrinsic to chat coordination.
  - D-2 (A6): Arm A's DONE post carries the verbatim work artifact rather than the coordination model's rewrite, so the validator scores the work product in all three arms. The DONE generation is still performed and metered per event, so the token economics being tested are unchanged.
  - D-3 (R3): "Completion" is each arm's own bookkeeping (A: DONE posted; B: done file; C: checker-passed). Arm C's is the strictest — the bias runs against the bus.
  - D-4 (T2): Token counts come from the endpoints' own counters per the pre-registered rule; Ollama prefix caching can understate prompt tokens on similar prompts. `prompt_chars` is logged per call and summed in metrics as the secondary view.
  - D-5 (T4): Arm C spends work tokens on sanctioned validation retries that A/B never spend; work tokens are context, not a bar.
  - A7: sender identity verified empirically — SwarmChat reports `from` as the user id (`cc-fortress` etc.), matching `--worker-id`.

### Arm A setup facts (first-hand)

- SwarmChat server: live Fortress instance, `swarmops` user, `--fsync`, tailnet bind `100.103.255.114:8484`.
- Client: pinned **Python 3.12.16** venv on Fortress (`~/fleet-bus-ab/swarmchat-venv`), installed `--no-index` from the vendored wheel; wheel sha256 `a786a94066a4d570502fb4b600a27b2e7dde23278cb3a029ba47db687a60d346` — matches the pilot's `vendor/HASHES.txt` exactly. No SwarmChat code patched (Joe's direction). Context: upstream suite fails on Fortress Python 3.14.4 (F-66) and passes 186/186 on 3.12 — the pin is SwarmChat's deployment cost, recorded in the design.
- Policy forced the roster change (design amendment, filed pre-run): `channel_creators = [pilot-admin]`, closed contacts roster. Four fresh `ab-*` users were created, could not create channels, and were **removed** (`Removed ab-operator / ab-w1 / ab-w2 / ab-w3` in the setup log). Arm A runs as operator `pilot-admin` + workers `cc-fortress`, `codex-fortress`, `aider-fortress`; tokens copied on-box from the data-dir custody files into `~/fleet-bus-ab/tokens/` (0600), never printed.
- Channels `fleet-bus-ab-a1`, `fleet-bus-ab-a2` created by pilot-admin with the full roster. A smoke channel round-trip (cc posts, aider reads) verified, then archived.

## Mechanics gate (Arm C) — PASS (required before A/B numbers count)

Run on Fortress, Nov 13, 2026 (identical results in the integrator's local validation run):

| Leg | Result |
|---|---|
| 1. Claim flood: 1,000 NOOP tasks, 8 concurrent claimants | **PASS** — 1,000 done, 0 duplicate claim attempts, 1,000 merges, 15.6 s |
| 2. Duplicate-enqueue storm (18-task batch × 2 processes) | **PASS** — exactly 18 tasks (18 created + 0/18 collisions split across the two processes) |
| 3. Kill/restart: reaper + one worker SIGKILLed mid-run over 100 tasks | **PASS** — 100 done, 0 duplicated merges, 1 reaper recovery |
| 4. Reconciliation: JSONL replay vs ledger | **PASS** — per-state counts identical (1,000 done) |

## Smoke-phase corrections (all before any timed run; design amendments recorded in DESIGN.md §3.1)

1. **Generation budget.** qwen3:4b's reasoning leaks into the response untagged on this Ollama build (no `</think>` marker within budget). At the filed 512 tokens, 2 of 3 smoke tasks produced zero answer content. Amended: work `num_predict` 512 → 1200 → 1600 (DRAFT reasoning still consumed 1200), Arm A claim cap 512, DONE cap 800, per-run cap 30 → 60 min. Identical across arms.
2. **Throughput measurement.** A benchmark DRAFT generation at peak contention (load avg ~47: F2's six-server phase + YOLO dual pass + Ollama runner ~1300% CPU) took 243.7 s wall for 1,600 eval tokens = **6.6 tok/s**. The pilot's Mint rate was ~3.2 tok/s (CPU); Fortress solo rates are far higher — the A/B measures the systems under real fleet load, disclosed as a condition, counterbalanced by run order.
3. **Arm A claim extraction.** First Arm A smoke: zero CLAIMs posted. Cause: the extraction captured ids with trailing punctuation from the model's reasoning (which quotes the option list before deciding). Fixed pilot-faithfully (the pilot harness extracted its choices tolerantly): scan all CLAIM/RECLAIM mentions, capture ids as letter+digits, take the last mention naming a currently available task. Re-smoke verified live: CLAIM v3 posted by both workers (the duplicate-claim race resolved by the deterministic ownership guard), work generation followed.

## A/B runs

(filled in as runs complete; per-run metrics in `runs/<arm>-run<n>/metrics.json` on Fortress, copied here at collection)

### Arm A run 1 — COMPLETE (valid)

Wall 3,600.3 s (hit the 60-min cap). 11/18 terminal; **lost 7** (c1, c5, c6, d1, d3, d5, d6); duplicated work 0; validator first-attempt pass 7/11 scored. Work tokens 14,959 (12 calls) vs **coordination tokens 35,750 (33 calls)** — coordination cost 2.39× the work; 51 coordination messages / 26,661 bytes. **Kill test fired**: victim cc-fortress holding v3 at the 6th completion; **v3 recovered, latency 794.5 s**. Full metrics copied into the RESULTS report.

### Arm B run 1, attempt 1 — INVALID (harness defect; stopped at ~17:38 CT, discarded, preserved on-box as `runs/B-run1-harnessbug-1738/`)

Observed: 5 tasks completed in the first ~7 min (v3, d6, d4, v4, d1), then progress froze while generations continued (~44 work calls by 17:35). A 50 ms-resolution directory watcher caught the mechanism live: task c4 was claimed, generated (~31 s), its result written — and the claim file was **swept back to the queue 1–3 s after each claim**, so the done-rename always failed and the task looped (c4 generated 30+ times; its result file rewritten each cycle).

Root cause (two implementation defects against the design's intent, neither present in Arm A or C): (1) `os.rename` preserves the queue file's mtime, and Arm B judges staleness by mtime — every claim taken more than 150 s after seeding was **born stale**, no matter how live its worker; (2) the heartbeat thread waited one 20 s interval before its first touch, leaving even fresh claims unprotected at birth. The first five tasks survived only because they were claimed within ~130 s of seeding. Generalizable finding, recorded for the report: **file mtime is not a lease** — a rename-based queue cannot distinguish "abandoned" from "just claimed" by mtime alone.

Repair (implementation brought back in line with DESIGN §3.3, which defines staleness over claims with the heartbeat as the liveness mark): claim now resets the file clock (`os.utime` at claim time) and the heartbeat touches immediately on claim, then per interval. No design parameter changed (same 150 s staleness, same flock claim, same sweeper). Attempt 1's directory is preserved on-box for audit; its numbers are NOT used. The run sequence was restarted from B run 1 (A run 1 stands; it does not depend on Arm B's code). This stop/restart is logged here as a coordinator intervention on the harness, not on any arm's protocol; the pre-registered per-arm intervention metric counts operator actions during a run's execution, and the report will disclose this event alongside it.

### Remaining runs — COMPLETE (sequence finished 21:04 CT; ALLDONE marker on-box)

| Run | Wall (s) | Done | Lost | Dup | Validator 1st-attempt | Work tok / calls | Coord tok / calls | Kill → recovery |
|---|---|---|---|---|---|---|---|---|
| A run 1 | 3,600.3 (cap) | 11/18 | 7 | 0 | 7/11 scored | 14,959 / 12 | 35,750 / 33 | v3 → recovered, 794.5 s |
| B run 1 (post-repair) | 1,722.4 | 18/18 | 0 | 0 | 14/18 | 21,421 / 18 | 0 / 0 | c3 → recovered, 336.1 s |
| C run 1 | 2,740.4 | 15/18 | 3 (d1, v1, v6) | 0 | 14/18 | 33,641 / 26 | 0 / 0 | c3 → recovered, 682.6 s |
| C run 2 | 2,826.5 | 16/18 | 2 (d5, v1) | 0 | 13/18 | 34,586 / 26 | 0 / 0 | — (no kill in run 2) |
| B run 2 | 1,336.3 | 18/18 | 0 | 0 | 16/18 | 17,162 / 18 | 0 / 0 | — |
| A run 2 | 3,601.9 (cap) | 14/18 | 4 | 0 | 10/14 scored | 16,746 / 15 | 43,851 / 42 | — |

Arm C's lost tasks, from the ledger DB: run 1 — d1 (DRAFT structural failures ×3), v1 (`WRONG_VERDICT_3` ×3), v6 (UNPARSEABLE/verdict mix ×3); run 2 — d5 (SHORT_SUMMARY/BAD_SOURCE ×3), v1 (`WRONG_VERDICT_3` ×3 again — a stable model error the gate refused six times across two runs while both incumbents delivered it). Verdict vs the §6 bar: **FAIL on legs 1 (zero-loss gate), 3 (wall vs B), 5 (validator vs B)**; pass on legs 2 (coordination tokens), 4 (interventions), 6 (mechanics gate). Full analysis: `RESULTS.md`.

## Interventions log

- **In-run interventions during any valid run: none.** Every run executed untouched from launch to its own completion/cap; the only kills were the pre-registered run-1 kill tests.
- **Harness repair between attempts (disclosed, not an in-run intervention):** Arm B run 1 attempt 1 was stopped at ~17:38 CT after the mtime-as-lease defect was diagnosed live (see the attempt-1 entry above); the implementation was repaired to the filed design, the attempt discarded and preserved, and the sequence restarted from B run 1. Arm A run 1 was not re-run.
- Runtime restarts of the integrator's VM interrupted three monitoring probes during the evening; the on-box sequence (detached `setsid` drivers) was verified unaffected after each, by process listing and metrics continuity.
