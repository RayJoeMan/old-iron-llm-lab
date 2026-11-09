# The expert-cache ceiling on an 8 GB card sits between 4096 and 6144 MiB — and the cache also pays on the M4000 (+57%)

- **Date:** 2026-11-08 (certified)
- **Platform:** Fortress — see `platforms/fortress-provisional.md`
- **Source record:** FORTRESS-TUNING.md **F-44**; experiment R11-2
  (on-box results `r11_2.json`)

## Question

F-39 mapped the MoE expert cache's capacity curve on the RTX
4000 up to 4096 MiB (the biggest one-card lever in the R10
battery) but did not find the ceiling. Where does the legal
cache range end on an 8 GB card — and is the lever specific to
the Turing card, or does it also pay on the Maxwell M4000?

## Method

llama.cpp b12136, ud-qwen3-30b-a3b-2507, `-cmoe`, ctx 8192, B3
probe. Two arms: RTX 4000 + `--moe-cache-mib 6144` (the next step
above the certified 4096), and M4000 + `--moe-cache-mib 4096`
against its certified no-cache arm (F-38 arm d: prompt 22.83 /
eval 4.98).

## Measured result

**RTX + 6144 MiB cache: context init fails** —
`llama_init_from_model: failed to initialize the context:
failed to allocate buffer for MoE cache`. The F-39 capacity
curve therefore terminates: on the RTX 4000 the legal cache
range ends **between 4096 MiB (works; total VRAM 5,971 MiB) and
6144 MiB (cannot allocate)** at ctx 8192. F-39's
size-to-working-set guidance stands, with 4096 MiB the practical
maximum on this card.

**M4000 + 4096 MiB cache: prompt 26.38 / eval 7.83** vs its
no-cache arm 22.83 / 4.98 — **+57% decode** — at 6,292 MiB
VRAM, RSS 13,407 MiB. The cache lever is card-agnostic: it pays
proportionally *more* than nothing on the Maxwell card, while
absolutely less than everywhere else (7.83 vs RTX + 4096 at
17.71 vs the dual split at 22.57). F-38's placement ordering is
unchanged.

## Verdict

**CERTIFIED.** The expert-cache sizing rule is now bounded on
both ends on an 8 GB card: below the working set it thrashes
(F-39), at 4096 MiB it pays on either card, and above ~4096
MiB it cannot be allocated at all on the RTX. When the M4000 is
the only card available for a one-card MoE placement, enabling
the 4096 MiB cache (+57%) is the correct default.
