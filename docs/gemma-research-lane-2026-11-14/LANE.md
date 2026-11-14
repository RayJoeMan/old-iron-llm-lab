# Gemma Research Lane — Fortress (established Nov 14, 2026)

**Model:** `gemma4:e4b` (Gemma 4 E4B, Q4_K_M, 7.5B on disk, ~4.5B active + vision/audio towers)
**Serving:** Fortress **system** Ollama 0.40.16 — store `/usr/share/ollama/.ollama`, endpoint `http://100.103.255.114:11434` (tailnet only)
**Status:** KEPT as the fleet's specialist research lane per Joe's ruling (Nov 14, 2026), under the specialists doctrine. This is a routing option, not a default — no other lane's behavior changes. qwen3:4b remains the drafting worker; llama3.2:3b remains the classification champion.

## Scope — what this lane is FOR

- **Multi-step research tasks**: questions that need 2–3 chained searches, where each hop depends on an entity revealed by the previous result, ending in a synthesized answer with **per-fact source attribution**.
- Tasks where the caller has **already decided search is needed** (see non-scope: the search/no-search decision is not Gemma's).
- Long, reasoning-heavy research work where end-to-end wall time matters: Gemma's advantage is that it spends its budget on tool calls and synthesis instead of burning it inside a think block.

## Non-scope — what this lane is NOT for

- **NOT classification** (llama3.2:3b's job) and **NOT general drafting** (qwen3:4b's job).
- **NOT single-shot tool-decision / "should I search at all" gating.** In the trial's Arm A KNOWN class, Gemma scored **1/10** — it searched for the chemical symbol for gold and the capital of Japan. Over-calling under a "search when you don't know" prompt is a class-wide 4B behavior, and Gemma is no exception. The caller gates; Gemma chains.
- NOT a qwen3:4b replacement: the trial's pre-registered verdict was **NO WIN** (F-75). This lane exists because Gemma dominated the one battery that matches this scope (Arm B), not because it won overall.

## How to call it

- Direct: `POST http://100.103.255.114:11434/api/chat` with `"model": "gemma4:e4b"`.
- Or via the fleet helper: `~/workspace/.tools/fortress_ask.py --model gemma4:e4b` (it sends `think: false` by default on the generate route).
- **`"think": false` is REQUIRED on every call.** It is the lane's load-bearing property and it binds through the system service (smoke-proven, below). By default Gemma streams reasoning through Ollama (smoke G1 route: 0/6 clean, 250–1,375 thinking chars per prompt); `think: true` is a no-op. With `think: false`: zero reasoning in the thinking field, zero think-blocks or prose reasoning in content, answers concluded.
- Trial-proven task settings: temperature 0, seed 42, num_ctx 4096, num_predict 768 per tool round, up to 5 tool rounds. The system service's own placement/threading applies — do not force `num_gpu` or `num_thread` for this lane.
- The model loads on first call and unloads after the system service's 30-minute keep-alive, like every other system model.

## Smoke results (Nov 14, 2026 — system service, first-hand)

Harness: the trial's own battery code (`battery.py` from the F-75 trial), re-pointed at the system endpoint with `num_gpu`/`num_thread` forcing REMOVED (the lane takes the system service as it is). Box load during the run: ~21–26 (Tranche B and other tenants active) — figures are as-measured on the working box, same caveat as the trial.

| Check | Result | Trial comparison (CPU-only, private instance) |
|---|---|---|
| **Think control** (`think: false`, 6 reasoning prompts, Arm C G3 route) | **6/6 clean — 0 thinking chars on every prompt; answers concluded and content-audited** ("$0.05", "5", "67", "9", "They weigh the same.") | 6/6 clean — **binds identically through the system path** |
| Think control, default route (G1) | 0/6 clean — reasoning streams by default | 5/6 leaked — same behavior |
| **Multi-step research** (full Arm B, 8 staged chained-search tasks) | **8/8 completion · 8/8 synthesis · 8/8 attribution**, exactly the minimum searches (2,2,2,2,3,2,2,2); rounds wall sum 180.5 s | 8/8 · 8/8 · 8/8, same search counts; Arm B wall 347.5 s |
| **Eval speed** (Arm D, 3 fixed ~150-word prompts) | **17.38 tok/s mean** (17.10 / 19.38 / 15.65) | 6.64 tok/s CPU-only — this serving shape is ~2.6× faster |
| Arm B counterpart (context) | qwen3:4b in the trial: 0/8 as-run at the 768-token budget; 3/8 at 2048 | — |

**Residency (per-bus `memory.used`, the fleet's residency standard):** the system service's own scheduler placed the model mostly on the **M4000 (bus 06:00.0)** — 10 MiB before load → **4,968 MiB** resident, steady through the whole run; the remainder of the 6,584 MB footprint sits in system RAM (partial offload). Both RTX 4000s were untouched by this lane (bus 05:00.0 held a pre-existing tenant at 6,783 MiB throughout; bus 41:00.0 stayed at 7 MiB). No placement was forced. (Note: `/api/ps` in this build reports `size = size_vram = 430 MB`, which undercounts the real footprint — the per-bus delta is the trustworthy figure.)

## Provenance — the bits are the trial's bits

- Imported on-box from the trial store (`~/flane/trials/gemma4-e4b-2026-11-14/ollama-models/`) into the system store: manifest + all 9 referenced blobs + 2 metadata files, copied (no re-download), ownership set to `ollama`. The trial store is untouched (still 20 files / 8.5 GB) and the trial instance remains stopped.
- Manifest is **byte-identical** to the trial store's (`cmp` clean). Weights blob verified by direct hash: `sha256:370c2879f17648d337b0ab4e208fdce348e24d1060064e93d7645daafd56d39c` in both stores.
- Digest bookkeeping: `/api/tags` on the system service reports `gemma4:e4b` digest `ccd2e5fbe4af129173bfdbabe85a93e195c01460860a8a2066efe4d9362dc6f2` (Q4_K_M, 7.5B, 6,584 MB) — that is the sha256 of the local manifest file. The trial record's headline sha `dc35e8d9c606…` is the upstream platform-manifest digest, which sits as a layer inside that same manifest (its blob was imported too). Same manifest, same layers, same weights — the two numbers name different levels of the same object.

## Evidence pointers

- Trial (pre-registered, full record): `~/workspace/your_files/gemma4-e4b-trial-2026-11-14/` — SPEC.md, RESULTS.md, battery.py, results*.json, transcripts*.jsonl. Filed as **F-75** in `~/workspace/your_files/fortress-llm-lane-2026-11-04/FORTRESS-TUNING.md`; published at RayJoeMan/old-iron-llm-lab `docs/gemma4-e4b-trial-2026-11-14/` @ da69e63d.
- This lane's smoke run: transcripts + harness in this folder (`smoke-transcripts.jsonl`, `smoke.py`); on-box originals at `~/flane/gemma-lane-smoke-2026-11-14/` on Fortress. (The harness's closing summary-print threw a KeyError after all arms completed — a patching artifact in the smoke copy, not a run failure; every score above is computed from the complete per-item transcripts.)
