# Fleet Bus v3 — Adoption Packet

**For Joe's ruling.** Prepared Nov 15, 2026 by the Fleet Bus program coordinator, at the end of the iterate-until-working loop Joe commissioned Nov 14, 2026 (20:51 CT).

## The ask

Adopt **Fleet Bus v3** as the fleet's task-delivery system for model work — replacing both the plain file queue (Arm B, the incumbent) and Fleet Bus v2 — on the strength of two pre-registered A/B tests it cleared under criteria filed before it was built.

## What v3 is

The v1/v2 ledger core (SQLite bus: idempotent claims, leases, heartbeats, reaper, dead-letter queue — unchanged except one additive, default-off `verdict(force_deadletter)` parameter) with a v3 policy layer:

- **Alternating class-aware ladders** (4 attempts max): VERIFY/CLASSIFY open on qwen3:8b and alternate 8b/4b; DRAFT opens on qwen3:4b and alternates 4b/8b. Every retry is a different model than the attempt before it.
- **A deterministic checker** validates every generation; failures climb the ladder; a task whose failure *repeats identically across two different models* dead-letters immediately (early-DLQ); a task that exhausts the ladder dead-letters with a full priced record. Nothing ships unvalidated; nothing is silently dropped.
- **Zero coordination generations** — arbitration is programmatic; the SwarmChat mirror is a durable log only.

Deployable article: `~/fleet-bus-ab3/code/` on Fortress (workspace masters in `../code/`): `fleetbus2.py`, `arm_c3.py`, `arm_b.py` (incumbent, for rollback), `validators.py`, `workgen2.py`, `mirror.py`, `run_ab3.py`, `gate_c3.py` + `gate-results3.json` (mechanics gate, 10/10 legs — re-run it after any code change; the orchestrator refuses bus runs without a passing gate file).

## The evidence (pre-filed criteria, both tests)

| | Main test (tuning set) | Confirmation (fresh tasks) |
|---|---|---|
| Win bar (8 legs, vs file queue) | **CLEARED 8/8** | **CLEARED 8/8** |
| Wall ratio vs incumbent (cap 1.25×) | **0.617×** | **0.744×** |
| Shipped-wrong (bus vs incumbent) | **0 vs 8** of 36 | **0 vs 8** of 36 |
| Correct jobs (of 36) | 32 vs 28 | 32 vs 28 |
| Tokens / error-free job (headline metric) | **942.3** vs 1,512.2 | **1,121.5** vs 1,518.9 |
| Lost / duplicated | 0 / 0 (incl. mid-run SIGKILL tests) | 0 / 0 (incl. kill tests) |
| Dead-letters (cap 4) | 4, all priced | 4, all priced |

Full records: `RESULTS.md` (main test, incl. the same-regime C2 reference runs and the routing-vs-gate attribution), `CONFIRMATION.md`, `RUN-LEDGER.md`, `metrics/`.

## What adoption means operationally

- **The DLQ is the human surface.** Dead-lettered tasks arrive as complete records (every attempt, model, validator reasons, token price). In both tests the DLQ held exactly one class of work: *persistent-misjudgment items* — tasks both models get wrong the same way (comparative/edge readings). Budget a human glance at the DLQ; its size in tests was 2 per 18 tasks.
- **The DLQ cap is the sizing constraint.** Both tests used the full cap (4/36). If production work has a higher share of persistent-misjudgment items, DLQ volume — not correctness — is what grows. The system never trades a silent wrong answer for DLQ relief; that is the point of it, and the trade Joe is being asked to endorse explicitly.
- **Correctness is validator-relative (disclosed in both designs).** The test validators for VERIFY/CLASSIFY compare against gold; production checkers will be structural or model-based and weaker. The bus's *mechanics* (no loss, no duplication, no unvalidated shipment, priced abstention) are checker-independent; the *yield* numbers are not — expect production correct rates to track checker quality.
- **Known untested levers (not part of this adoption):** the generation-path think-leak fix and validator-reason feedback in retry prompts are filed v4 candidates (DESIGN A16, §1). Neither is needed to justify v3; neither should be bundled into an adoption deploy.
- **Rollback:** the incumbent file queue (`arm_b.py`) is untouched and remains in the article; reverting is a launcher change, not a migration.

## Recommendation

Adopt. V3 is the first version to beat the incumbent on **both** axes the program was chartered on — correctness (v1/v2's axis: nothing lost, nothing wrong shipped) and price (the axis v2 failed: it is now *faster and cheaper per clean job than the incumbent itself*, not merely within a surcharge cap) — and it did so twice, on the tuning set and on fresh tasks, under criteria filed before it existed, with both frontier design checks' objections adjudicated into the build. The loop's work is done; the decision is yours.
