# ADOPTION PACKET — SwarmChat as a fleet coordination medium (for Joe's ruling)

**Claim established by this phase (filed construction, both workloads):** a SwarmChat-coordinated system running the C3 policy (Arm S, procedure v2) clears the Phase 1 bar against the file queue and matches-or-beats the Fleet Bus v3 ledger on the medium yardstick — first on the tuning workload against frozen references (provisional screen), then **confirmed on a fresh workload with all-fresh references**:

| Confirmation (fresh) | Wall s | Tokens | Correct | Ship-wrong | DLQ | tok/efj |
|---|---|---|---|---|---|---|
| File queue (B) | 1,462.3 | 42,575 | 29/36 | 7 | 0 | 1,468.10 |
| Fleet Bus v3 (C3ref) | 850.5 | 27,612 | 34/36 | 0 | 2 | 812.12 |
| **SwarmChat (S v2)** | **822.2** | **27,504** | **34/36** | **0** | **2** | **808.94** |

## The complement case

Fleet Bus v3 is adopted and stays adopted — nothing here displaces it. What the phase adds is a **second certified medium with a different native shape**, and the choice between them is per-workload:

- **Audit surface.** The bus's record is a SQLite ledger + DLQ files; SwarmChat's record is the channel transcript itself — every TASK/CLAIM/RESULT/VERDICT/REQUEUE/DELIVERED is a timestamped, server-ordered message a human can read in the SwarmChat console as it happens. The collector re-derives every metric from that transcript independently of the checker, and the two agreed exactly in every gate and run. For work Joe wants to *watch* or *show*, the chat medium is the record and the interface at once.
- **Behavioral parity where it matters.** On the confirmation workload the two media deadlettered the same tasks in the same runs with identical per-class yields (11/12/11). The policy is the same; the medium did not change a single outcome — it changed only price (S marginally cheaper on both wall and tokens) and surface.
- **Failure behavior.** The v1 campaign found the chat harness's one real weakness — unhandled generation exceptions wedging claims — and v2 fixed it to exact C3 parity (abandon → lease re-drive at the same attempt). The fixed procedure then absorbed six concurrent qwen3:4b timeout stalls in the scored pair with zero lost tasks, and ran the confirmation pair with zero failed calls. Kill recovery is proven on both media (S: worker kill 134.9–291.9 s; checker kill + relaunch clean).
- **Cost shape.** Coordination tokens are 0 on both (bus: ledger ops; chat: messages). S's coordination traffic is measurable and small: 223–255 transcript messages (~58–69 KB) per 18-task run.

## Caveats that travel with the win

1. **The vendor suite is intermittently red.** Post-phase idle run: 181 tests, FAILED (5F+1E), all in `test_by_hand.py` — the Nov 14 signature, this time on an idle box. The phase's direct probe of the same primitive passed 100/100 under load and every kill gate passed, so the evidence points at the tests' subprocess choreography — but it is the vendor's own suite, and a future phase should isolate it before SwarmChat carries anything production-critical. The live server itself never faulted during the phase (it was never restarted; S server faults would have been scored, and there were none).
2. **Single-process server.** SwarmChat runs as one process on Fortress (tailnet-only :8484). The bus's ledger is a file any host can open; the chat medium depends on that server being up. Channels archive in place and export cleanly (this phase exported and hash-filed every run channel), and authorship survives agent removal — both verified at cleanup.
3. **Harness discipline is load-bearing.** The v1 lesson generalizes: any client of this medium must treat generation exceptions as claim abandonment, never as a thread death. Procedure v2 (hash-pinned in this phase's code article) encodes that; adopting the medium means adopting the procedure with it, not re-deriving it.
4. **Margins are decision rules, not significance tests** (n = 2 runs per arm, as filed). The confirmation margins are comfortable (tok/efj below the reference outright; wall below outright), but they are two-run margins.

## What adoption would mean concretely (Joe's call on each)

- **A.** Certify procedure v2 as the standing S operating procedure (the pinned code article from this phase) for any workload routed to SwarmChat. No code changes needed — it is the tested artifact.
- **B.** Route *observable* work (anything Joe may want to watch live or audit conversationally — e.g., drafting batches with a human review surface) to SwarmChat channels; keep bulk/throughput work on Fleet Bus v3. The DLQ remains the human review surface on the bus; on SwarmChat the DEADLETTER transcript entries + exported channel play the same role.
- **C.** Commission a small follow-up (separate phase, Joe's word): isolate the `test_by_hand` intermittent failures against the live server build, since that suite is the vendor's health signal for the medium.
- **D.** Do nothing further: Fleet Bus v3 remains the sole medium, and this phase's result stands as a certified fallback if the bus ever needs one.

**Coordinator's recommendation:** A + B, with C queued behind the Falcon bake-off in Joe's tenant order. The medium earned parity-or-better twice under the program's own discipline; its transcript-native audit is a genuinely different capability, not a duplicate. D remains respectable — the bus is adopted and proven — but it leaves a certified, cheaper-on-both-prices medium unused.

*All numbers trace to filed artifacts: RESULTS.md, SCORECARD-V2.md, CONFIRMATION-SCORECARD.md, RUN-LEDGER.md, and the metrics/exports in this article. SwarmChat source was never modified; the phase's test agents, grant, and policy changes were fully reverted at cleanup (verified against the phase-start backup).*

---

## RULING — ADOPTED (Joe, Nov 15, 2026, 16:26 CT)

Joe adopted this packet as filed: **procedure v2 is certified as the standing SwarmChat operating procedure. Observable work routes to SwarmChat (transcript-native audit); Fleet Bus v3 keeps bulk work.** The file queue remains untouched for rollback. The `test_by_hand` suite-isolation follow-up stays queued behind the Falcon bake-off, as proposed. Recorded by Nyx in MEMORY.md and ~/memory/2026-11-15.md.
