# Platforms

A finding is only as portable as its fingerprint. Every entry in `findings/`
names the platform page (and fingerprint state) it was measured under.

| Platform | State | Notes |
|---|---|---|
| [Mint](mint.md) | **Settled** | Hardware static; the experiment program's home. 16 of the seeded findings were measured here. |
| [Fortress](fortress-provisional.md) | **Settled — 2026-11-10 fingerprint** | Filename kept from the provisional era. Hardware settled 2026-11-09 (E5-2660 v2 pair, 3 GPUs: 2× RTX 4000 + M4000, NVMe model drive). The page records both the current fingerprint and the 2026-11-08 fingerprint the R10–R17 findings cite. |

Fingerprint discipline, learned the hard way: a silent platform change can
break a lane without any visible failure — on the Mint, a quantized-KV-cache
setting shipped without its required flash-attention flag left one model
unloadable while every health check still answered. Rule since then: **after
any serving-environment change, smoke-test a real generation on every model**;
a model list endpoint proves nothing about loadability. Fingerprint changes
are recorded on the platform page with dates.
