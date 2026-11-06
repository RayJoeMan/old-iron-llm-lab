# Upstream contributions — tracker

The fleet's give-back rule (owner directive, 2026-11-06): *always give back
to anything we can; unused compute should always be used to make things
better.* When fleet research produces data an upstream project lacks —
measurements, bug reproductions, validation on hardware maintainers don't
own — the contribution is **drafted as a matter of course**.

**Posting is different from drafting.** Anything posted publicly under the
owner's GitHub account (RayJoeMan) takes the owner's per-item OK first.
A row below is a candidate, never an authorization.

The fleet's comparative advantage is not kernel authorship — it is
**hardware access + measurement discipline**: controlled, replicated,
log-attached measurements on the hardware cells public benchmarks skip
(Maxwell sm_50/sm_52, Pascal, dual-socket AVX-only Xeons behind DDR3,
WSL2 with real NUMA topology).

## Tracker

| # | Project | Contribution | Evidence state | Status |
|---|---|---|---|---|
| C1 | llama.cpp (`ggml-org/llama.cpp`) | Bug report: internal `--numa distribute` mode wedges generation on dual-socket WSL2 (zero tokens in 14 min) while external NUMA placement works | Data exists in the fleet record (platform hazard, Fortress pre-build) | **DRAFT — NOT SENT** ([draft](llama-cpp-numa-distribute-wedge-DRAFT.md)) |

*Further ready candidates exist in the fleet's private contribution map
(bundled-backend behavior on Maxwell, quantized-KV failure envelopes, a
silent serving-config breakage class). They enter this tracker as their
drafts are written and checked against the upstream trackers — duplication
checks happen at draft time, not before.*
