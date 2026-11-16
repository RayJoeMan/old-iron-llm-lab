# RESULTS — SwarmChat Phase (Phase 2 of Joe's fleet program loop)

**System under test:** SwarmChat (live on Fortress, tailnet-only, pinned Python 3.12 venv) as a coordination medium for the fleet's model work, carrying the Phase 1 winning policy (C3) unchanged. **Question:** can a SwarmChat-coordinated system clear the Phase 1 bar against the file queue, and can the medium itself match the Fleet Bus v3 ledger on the yardstick? **Route:** baseline → design with the win bar filed before any scored run → dual frontier check (Claude Opus 5.5 + GPT-6 Astra, mutually blind) → written adjudication → mechanics gate → scored runs under the fairness protocol → fresh-workload confirmation for any win. SwarmChat source was never forked, patched, or reprogrammed; the harness is a client of the live server.

## Baseline (filed before design)

- Suite `python -m unittest discover -s tests` as swarmops: **181/181 OK** on the pinned 3.12 venv (77.4 s ×2) and on system Python 3.14.4 (85.8 s ×1), idle box.
- **Premise correction, filed openly:** the brief's claim that the suite fails on 3.14 was **not reproduced**. The Nov 14 failures (5F+1E, timing/subprocess-sensitive `test_by_hand` tests, during the Phase 1 campaign) are consistent with a load-sensitivity hypothesis; the loaded diagnostic later ran green too (181 OK in 93.5 s under concurrent generation load), so the hypothesis is not supported at scored-run load either. The scored environment is the pinned 3.12 because it is the production runtime.
- Qualification before scored runs: **3/3 green** (77.7/77.3/77.4 s, loads <2/2/4).
- API-semantics probe against the live server: **all 7 properties pass** — total order (300 posts, second reader identical), cross-identity visibility 50/50, wait wakes on thread replies 20/20, **wait-after-kill 100/100 under load** (the Nov 14 failing primitive is empirically sound here), non-consuming peek, exact pagination, payload fidelity sha256-exact.

## V1 campaign — bar FAILED on the S arm (legs 1–2)

Six runs (B1 → C3ref1 → S1 → C3ref2 → S2 → B2), tuning workload (18 tasks, sha256 `e8e3748b…`):

| Arm (pooled) | Wall s | Tokens | Correct (C/D/V) | Lost | Ship-wrong | DLQ | tok/efj |
|---|---|---|---|---|---|---|---|
| B | 3,659.0 | 40,303 | 26 (11/6/9) | 0 | 10 | 0 | 1,550.12 |
| C3ref | 2,394.2 | 31,445 | 32 (12/12/8) | 0 | 0 | 4 | 982.66 |
| S v1 | 4,474.5 | 21,373 | 30 (11/10/9) | **4** | 0 | 2 | 712.43 |

S1 hit the 3,600 s cap with 4 tasks lost. Root cause (evidence-corrected in ADJUDICATION-V2 §7): four concurrent qwen3:4b generations were orphaned by a runner stall; their client calls timed out at 600 s; the harness's generation threads let the `TimeoutError` escape, so the four claims were RENEWed every 60 s (254 of 411 transcript messages) until the cap. Classification: **S harness fault, scored not excused.** S2 (run after a disclosed mid-campaign repair) is labeled **non-scoring repair evidence** under the precedent fence; v1's verdict is unmoved. The mechanics gate had passed 17/17 before the campaign — it caught two real harness bugs (deterministic double generation; foreign CLAIMs entering protocol state), both fixed and re-proven — but its stub generation never raises, so the exception path was exactly what it could not see.

## V2 iteration — parity fix, adjudicated

The amendment was dual-checked (both frontier seats SOUND WITH CONDITIONS) and adjudicated in writing. The fix is **behavioral parity with C3**, not the amendment's original empty-artifact mechanism (which source evidence showed would have diverged on attempts, rungs, and DLQ reasons): on a generation exception the S worker now logs the failure and **abandons the claim** — renewals stop, nothing is posted — and the checker's lease machinery re-drives the **same attempt**, exactly as C3's reaper does. Plus: renewal is liveness-gated, RESULT-post failures are retried, and the collector gained a silent-hold audit. Gate leg (r) was added for the exception paths (per-class abandonment, concurrent hang-raise ×3, raise-always → `LEASE_EXHAUSTED` DLQ with zero validator verdicts, RESULT-post retry). **Full gate re-run on the pinned implementation: PASS 18/18** (Fortress), independently corroborated by labeled Mint pre-runs (suite 181 OK in 68.4 s; gate 18/18 from the Mint host; workload/gold/prompt-equivalence clean — MINT-PRERUN.md).

## V2 scored pair — provisional screen WIN (details: SCORECARD-V2.md)

| S v2 (pooled) | Wall s | Tokens | Correct (C/D/V) | Lost | Dup | Ship-wrong | DLQ | tok/efj |
|---|---|---|---|---|---|---|---|---|
| Run 1 | 1,253.7 | 17,692 | 16 (6/6/4) | 0 | 0 | 0 | 2 | 1,105.75 |
| Run 2 | 1,194.4 | 15,915 | 16 (6/6/4) | 0 | 0 | 0 | 2 | 994.69 |
| **Pooled** | **2,448.1** | **33,607** | **32 (12/12/8)** | **0** | **0** | **0** | **4** | **1,050.22** |

**Bar: all 8 legs pass** (the two legs v1 failed — lost/accounted — now pass in each run; wall ratio 0.6691 vs the 1.25 cap; DLQ 4 at, not over, the cap). **Yardstick: all conditions pass** — (ii) tok/efj 1,050.22 ≤ 1,080.93; (iii) wall ratio 0.66908 ≤ 0.75436; (iv) correct 32 ≥ 32, shipped-wrong 0; (v) per-class deltas 0/0/0; (vi) medium-caused extra generations 0 (all 6 extras attributed runner-caused under the filed rule: each pairs with a qwen3:4b `TimeoutError` + claim-abandonment log line). **A19 improvement test satisfied.** The v1 failure event recurred three times per run (concurrent 4b timeouts) and was absorbed with zero lost tasks — the procedure working as adjudicated on the exact fault that motivated it.

**Robustness disclosure:** yardstick (ii) is **not robust** — the per-run split flips it (run 1 alone fails it) and the A15 token upper bound flips it. All other legs pass by wide margins under every reading. The screen is a *historical-reference provisional screen* by the adjudication's own terms; the win is decisive only if the fresh-workload confirmation clears.

## Confirmation campaign — CONFIRMED WIN (Nov 15, 2026, 14:18–15:17 CST; details: CONFIRMATION-SCORECARD.md)

Six fresh runs on the pre-committed confirmation workload (18 tasks, sha256 `5b48868e…`), staged by hash-verified swap (restore verified, RESTORE_OK), all arms fresh, interleaved as filed:

| Arm (pooled) | Wall s | Tokens | Correct (C/D/V) | Lost | Ship-wrong | DLQ | tok/efj |
|---|---|---|---|---|---|---|---|
| B fresh | 1,462.3 | 42,575 | 29 | 0 | 7 | 0 | 1,468.10 |
| C3ref fresh | 850.5 | 27,612 | 34 (11/12/11) | 0 | 0 | 2 | 812.12 |
| **S fresh** | **822.2** | **27,504** | **34 (11/12/11)** | **0** | **0** | **2** | **808.94** |

**Bar: all legs pass. Yardstick: all conditions pass — and (ii) is robust this time** (S tok/efj 808.94 is below C3ref's own 812.12, both S runs individually pass, and the A15 bound passes; S wall is also absolutely below C3ref's). S and C3ref deadlettered the same tasks in the same runs (cv4, cc6 — the filed traps) with identical per-class yields; S had zero failed calls and zero extra generations across both runs. **The v2 win is confirmed under the filed construction.** Production adoption is Joe's ruling; the adoption/complement case is in ADOPTION-PACKET.md.

## Post-phase suite run — FAILED (5F+1E), reported verbatim, non-scored

One idle-box suite run after the scored work (Nov 15, ~16:12 CST, pinned 3.12 venv, load 0.24–1.02 at launch, no models resident): **Ran 181 tests in 106.4 s — FAILED (failures=5, errors=1)**, all in `test_by_hand.py` (test_a_stopped_wait_does_not_use_up_the_next_message — ERROR on 'ctrl-c', FAIL on 'kill', "'sent after kill' not found"; test_a_killed_download_leaves_no_half_file — FAIL on 'ctrl-c', 'kill', 'hard kill', and the parent case). Full log: `post-phase-suite.log`. This is the **same signature as Nov 14** and it occurred on an idle box, which weakens the load-sensitivity hypothesis (the loaded diagnostic was green; the qualification was 3/3 green; this idle run is red). Per the filed discipline the failure is reported verbatim and **not** silently re-run; it is non-scored (suite health is qualification + diagnostics, not an adoption leg — the pre-run qualification stands). The tension is noted honestly: the phase's own probe of the same wait-after-kill primitive passed 100/100 under load and every kill leg of every gate passed, so the flakiness localizes to the by-hand tests' subprocess choreography rather than to the primitive as the harness exercises it — but the suite is the vendor's own, and its intermittent red on an idle box is a defect signal about the system under test that a future phase should isolate. It does not change any scored result in this phase.

## Phase-end cleanup — complete

- **Exports before removal:** all six run channels + both probe channels exported in full (`read --all --limit 100000 --peek` as pilot-admin); message counts match the metrics exactly (411 / 233 / 255 / 223 / 185 / 192 / 1,553 / 597); sha256 manifest filed (`channel-exports-manifest.json`; exports on-box in `~/swarmchat-phase/exports/`).
- **Authorship dry run:** a scratch agent posted to a scratch channel and was removed; the archived readback still names it as author — **agent removal does not anonymize archived authorship** (readback filed on-box).
- **Agents removed:** swarmtest-dispatch, swarmtest-checker, swarmtest-w1/w2/w3, plus the scratch agents used in cleanup. Pilot-admin's people list is back to the original 10 identities, zero swarmtest.
- **Grant removed:** channel_creator holders are now [pilot-admin] only.
- **Contact policy restored:** contacts match the phase-start backup (`policy-backup-20261115.json`) exactly; full policy = backup-minus-grant, verified by policy-show diff. **Disclosure:** the first restore attempt passed the backup file in its `{"rules": …}` wrapper shape, which policy-set stored literally, leaving an effectively empty policy for ~2 minutes (no runs in flight, no other server activity in the window); the corrected flat restore was applied and verified immediately. Final state is exact.
- **Channels archived, none deleted:** 30 phase channels archived (6 run, 2 probe, 1 scratch, 21 gate). The SwarmChat server process was never restarted by this phase.

## Standing notes

- Regime: a zombie Ollama runner (since Nov 14 ~20:05 CT, not in /api/ps) is a constant background for every run in this phase; flagged for the parent, untouched (Ollama is outside this phase's scope).
- Sequencing disclosures: the Fortress gate-v2-full re-run (10:21 CST) preceded the Fleet Bus feedback campaign's completion (12:35:31 CST) — the gate is stub mechanics with no model generation, the pinned hashes were re-verified byte-identical at the scored launch (12:42), and the Mint pre-run reproduced the gate 18/18 independently. The scored runs themselves ran in the exclusive window per Joe's ruling.
- Production adoption is Joe's ruling. Nothing in this phase changes Fleet Bus v3's adopted status on its own.
