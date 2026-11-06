# Methodology

How a number earns its way into `findings/`. Distilled from the fleet's working
experiment program (Mint lane, running since 2026-11-01) and its agent-registry
methodology.

## The experiment shape

Every experiment is **one variable** against a frozen champion, on a **frozen
eval set**, with the **pass bar written down before the run** ("pre-registered").
The bar is read as written afterward: a failed bar is a fail, a closing clause
that fires is closed, and single-draw wins are judged on their replicate, not
on the draw.

Adoption standard (the "clear-win rule"): a challenger is adopted only if it is
strictly better on the primary axis, or equal at ≥20% faster, with **no
regression on sibling benchmarks** — and, for anything production-shaped, after
a fresh-seed replication. Judgment overrides of a met bar are allowed but must
be recorded as judgment, with the reason (this has happened exactly once in the
seeded record: a hook-temperature change whose bars were met twice was declined
because it produced the lane's first exact duplicate — see the registry review
notes; that item is *not* seeded as a finding because nothing was adopted).

## Contracts, not personas

Work is organized as named **job classes** ("agents" in the working registry),
each a contract with three parts:

1. **Job contract** — what it produces, the exact brief shape, the champion
   model + parameters, the batching shape.
2. **Eval** — a fixed set with a fixed key/ruler, a named metric, and the
   latest measured score.
3. **Checker** — who or what verifies output before it is used.

A job class without a fixed eval is not an agent yet — it's a habit. (One
seeded-adjacent lane, overnight long-form drafting, openly carries that gap;
its absence of a frozen eval is recorded as a finding about the lane, not
papered over.)

## Checker independence

**The checker is never the model that did the work.** Mechanical validators
first (deterministic format/compliance scorers), a different-lineage model or
a two-guest judge pair second, a human-supervised editorial pass last.

One measured exception exists in the seeded findings and is the exception that
proves the bookkeeping: the summary merge loop's checker is the same model as
its worker. That adoption was made knowingly — the checker's bias was audited
first (a known, stable false-positive pair; recall that collapses on a
different generator's output, which is why the loop is barred there), and a
mandatory independent figure check backstops every summary. The finding
(`2026-11-06-summary-merge-loop.md`) carries the full pricing.

## Portable contracts vs platform profiles

Every result separates two layers:

- **Portable contract layer** — brief text, restatements, temperature,
  batching, extraction rules. These are model/prompt properties and are
  *expected* to transfer between machines — but transfer is verified by a
  confirmation run on the receiving platform, never assumed. (The fleet has a
  standing counterexample: a summary brief line adopted on the Mint *harmed*
  scores on Fortress and was rejected there. Same model family, same brief,
  opposite verdict.)
- **Per-machine platform profile** — threads, splits, NUMA placement, KV
  settings, driver/backend facts. These never transfer; they are re-measured
  per platform fingerprint.

## Tokens/sec honesty

On a memory-bandwidth-bound box, decode speed is a hardware constant
(bandwidth ÷ bytes-per-token), not a tuning outcome. Sampler sweeps on the
Mint all came back saturated, which is the measurement behind that claim.
The tuning program therefore optimizes **useful output per token** — routing,
contracts, batching, fewer do-overs — and reports speed changes only where
the mechanism is real (model/quant choice, offload, batching), never as a
sampler trick.

## Negative results

Rejected challengers are closed **in writing, with the measurement** — the
closure is what stops the same idea being re-run next month. The working
ledger's rejections (temperature levers closed on both sides of a lock,
exemplar insertions measured harmful, a decertified single-draw win reversed
by its own replication) are the program's institutional memory. Public
findings here seed only the adopted side; the rejections that bound an
adopted finding are summarized inside that finding's entry.
