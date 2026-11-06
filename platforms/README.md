# Platforms

A finding is only as portable as its fingerprint. Every entry in `findings/`
names the platform page (and fingerprint state) it was measured under.

| Platform | State | Notes |
|---|---|---|
| [Mint](mint.md) | **Settled** | Hardware static; the experiment program's home. All 13 seeded findings were measured here. |
| [Fortress (provisional)](fortress-provisional.md) | **PROVISIONAL / PRE-BUILD** | Hardware not settled (CPU swap + GPU installs pending; tuning chain still running at staging). Platform facts only — no findings seeded. |

Fingerprint discipline, learned the hard way: a silent platform change can
break a lane without any visible failure — on the Mint, a quantized-KV-cache
setting shipped without its required flash-attention flag left one model
unloadable while every health check still answered. Rule since then: **after
any serving-environment change, smoke-test a real generation on every model**;
a model list endpoint proves nothing about loadability. Fingerprint changes
are recorded on the platform page with dates.
