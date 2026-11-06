# Fleet Findings — measured results from a home-lab LLM fleet

> **Status: STAGING DRAFT (2026-11-06).** This folder is a local staging scaffold for a
> proposed public repository. Nothing here has been published, pushed, or sent anywhere.
> Whether this becomes a public repo at all is an open decision.

## What this is

A curated collection of **measured findings** from a small, deliberately old-hardware
local-LLM fleet: prompt/brief contracts, sampling and routing choices, platform quirks,
and failure envelopes — each one produced by a controlled experiment with a pre-registered
bar, a frozen eval set, and a named checker.

The fleet's working premise: on salvaged hardware (a Maxwell laptop GPU, a dual-socket
AVX-only Xeon workstation), *useful output per token* is won by routing, brief design,
batching, and verification discipline — not by engine swaps. This repo is where the
evidence for that claim lives, in public, in a form other people running old hardware
can check.

## Who runs it

A home-lab fleet operated by one owner (GitHub: RayJoeMan) with an AI orchestrator
(Muse lane) that designs the experiments, runs the adoption reviews, and verifies
every number before it is filed. Local models do the generation work under test;
they never grade their own homework (see Methodology).

## Honesty rules

These rules are the point of the repo. Every finding here is held to them:

1. **Measured numbers only.** No estimated, extrapolated, or "should be" figures are
   presented as results. Where a number is an estimate, the entry says so.
2. **Hardware fingerprint on every finding.** A result without its platform
   (machine, GPU + compute capability, driver, serving stack + version, relevant
   service environment) is not a finding. See `platforms/`.
3. **Pre-registered bars.** Experiments state their pass bar before the run.
   A bar that fails is a fail; bars are not renegotiated after the draw.
4. **Negative results are published too.** Rejected challengers, wedges, crash
   boundaries, and "no difference" outcomes are findings, filed with the same care
   as the wins. Several entries here exist *because* a plausible idea measured badly.
5. **Replicates over single draws.** Single-draw wins are proposals, not results.
   Adoption requires replication — ideally fresh-seed, byte-checked where the lane
   is deterministic.
6. **Checker independence.** The checker is never the model that did the work.
   Where a measured exception exists, the entry names it, prices it, and names
   its backstop (see the summary merge-loop finding).
7. **Corrections stay visible.** When a later measurement overturns an earlier
   record, the correction is filed, not silently edited away.

## Scope — read this first

**This repo holds curated exports only.** The working ledgers (the full chronological
experiment log, the production queue, per-agent contract scaffolds) stay private.
What appears here is a finding that has already been **adopted or certified** in the
working program, rewritten as a standalone entry with its evidence.

**No business or operational content appears here.** No customer data, no commerce,
pricing strategy, outreach, credentials, network addresses, or production content.
Eval sets are described by what they measure and how large they are; raw eval text
is included only where it is fixed, non-sensitive instructional text — and anything
doubtful on that line is excluded and flagged (see `evals/README.md`).

## Layout

```
methodology/    how experiments are designed, checked, and adopted
platforms/      per-machine fingerprints + baselines (the context every number needs)
findings/       dated, self-contained adopted/certified results
contributions/  tracker for drafts sent (or ready to send) to upstream projects
evals/          descriptions of the frozen eval sets behind the findings
```

See `STRUCTURE.md` for the full tree and the conventions for adding an entry.

## Contents at staging (2026-11-06)

- **13 seeded findings**, all from the Mint lane's adopted/certified record:
  the TUNING #97 adoption batch (6 items, 2026-11-04), the B4 stack brief (#138)
  and filler-fact scanner (#139) adoptions (2026-11-05), and the five adoption
  filings of 2026-11-06.
- **Fortress content is provisional only**: a platform fingerprint page marked
  PROVISIONAL / PRE-BUILD. The Fortress tuning chain (r6, 150 jobs) was still
  running at staging time and its hardware is not settled (CPU swap and GPU
  installs pending), so **no Fortress findings are seeded** — only platform facts.
- **1 contribution draft**: a llama.cpp bug report (see `contributions/`),
  marked DRAFT — NOT SENT.
