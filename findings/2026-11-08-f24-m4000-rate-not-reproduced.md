# Correction: F-24's M4000 8B all-GPU rate (≈35.3 tok/s) is NOT REPRODUCED — the cross-checked figure is ≈11.5

- **Date:** 2026-11-08 (certified)
- **Platform:** Fortress — see `platforms/fortress-provisional.md`
- **Source record:** FORTRESS-TUNING.md **F-36** (and the correction note
  now carried on F-24 itself); experiments R10-0b, R10-0c, R10-1
  (on-box results `r10_0c.json`, `r10_0b.json`, `r10_1.json`)

## Question

An earlier fleet entry (F-24) recorded qwen3:8b fully resident on the
Quadro M4000 decoding at **≈35.3 tok/s** (prompt ≈124 tok/s) on the
llama.cpp lane — about 3.2× the Ollama-side figure for the same card
and model, explained at the time as a "lane-accounting difference."
Which number is right?

## Method

A bisect (R10-0b/R10-0c) on the same binary (llama.cpp b12136) and the
same model blob as F-24, varying one factor at a time: device
addressing (`-dev CUDA1` vs `CUDA_VISIBLE_DEVICES` mask), load mode
(`-lm none` — the exact F-24 bridge flags — vs automatic), and
single-device visibility. Residency was VRAM-verified, and the server
log's own `print_timing` lines were cross-checked against the client
timings — the check F-24 never made.

(A first bisect pass repeated the harness's mask-order error — mask 0
is the RTX on this stack — and is recorded in the ledger as an
operator error, not a result; the corrected arms below isolate the
M4000 via mask 1.)

## Measured result

**Four independent reads agree at 11.0–11.6 eval tok/s** for qwen3:8b
fully resident on the M4000:

| Read | Eval tok/s |
|---|---|
| Ollama GPU-era B3 (F-16/F-34) | 11.01 |
| llama-server, `-dev CUDA1` (R10-1) | 11.4 |
| llama-server, device mask only (R10-0c X3b) | 11.55 |
| llama-server, mask + `-lm none` — exact bridge replica (R10-0c X1b) | 11.53 |

The server log cross-checks the client numbers (87.5 ms/tok at 11.4).
Neither load mode, device addressing, nor single-device visibility
moves the number.

**Why 35.3 was never credible:** it is ~96% of the M4000's theoretical
192 GB/s memory-bandwidth peak for a ~5 GB Q4_K_M decode stream. F-24
verified residency (VRAM + GPU-Util) but never cross-checked the
server log's timing lines; the likely failure mode is a harness-side
timing read, not a residency error.

**Side finding from the same bisect:** `-dev CUDA1` + `-lm none`
**hangs at load** (no /health within 300 s, log stops mid-load); the
same `-lm none` under a device mask loads fine. The wedge is that flag
combination — recorded so future bridge work avoids it.

## Verdict

**CERTIFIED — the flag is upheld.** F-24's 8B eval figure (≈35.3
tok/s) and its prompt figure (≈124 tok/s) are marked **not
reproduced**, and F-24 carries the correction note on its face. What
F-24 actually established — all-layers GPU residency is placeable on
this card, and its prefix-cache verdict (identical repeats cost
~100× less prompt processing with `cache_prompt=true`; no lane
prompt-eval number is cache-inflated) — is unaffected, is re-confirmed
by this battery, and stands.
