# RESULTS — Gemma 4 E4B vs qwen3:4b (research / tool-calling lane trial, 2026-11-14)

Pre-registered in SPEC.md (same folder) before any run. Harness: Ollama 0.40.16, private CPU-only instance on Fortress (127.0.0.1:11440, own store, `CUDA_VISIBLE_DEVICES=`, `OLLAMA_VULKAN=0`, `num_gpu: 0` on every request — post-run `nvidia-smi` confirms zero GPU contact; both RTX 4000s stayed with G2, M4000 with lane-b). Identical prompts, mock tool, and settings both arms: temperature 0, seed 42, num_ctx 4096, num_thread 12, num_predict 768 (Arms A/B), 512 (Arm C), 256 (Arm D).

Models (digests from the trial store):
- Challenger: `gemma4:e4b` — sha256 dc35e8d9c6061baa6f0fa870975ab6932e2542b579b13ea0f199fa4bb7300c9c, Q4_K_M, 7.5B params on disk (6,278 MB; ~4.5B active language model + vision/audio towers), capabilities: completion, vision, audio, tools, thinking.
- Incumbent: `qwen3:4b` — sha256 359d7dd4bcdab3d86b87d73ac27966f4dbb9f5efdfcc75d34a8764a09474fae7 (identical blob to the fleet system store), Q4_K_M, 4.0B, 2,381 MB, capabilities: completion, tools, thinking.

## Scorecard (as-run, mechanical scoring)

| Arm | gemma4:e4b | qwen3:4b |
|---|---|---|
| A EXT (call when a fresh fact is needed) | **10/10** (facts in answer 10/10) | **10/10** (facts 10/10) |
| A KNOWN (answer directly, no call) | **1/10** | **1/10** |
| A UNK (abstain, no fabrication) | **9/10** | **8/10** |
| **A overall** (mean of classes) | **66.7** | **63.3** |
| B completion / synthesis / attribution | **8/8 · 8/8 · 8/8** | **0/8 · 0/8 · 0/8** (see §B) |
| C working think-control | **YES — `think: false` binds, 6/6 clean** | **NO route binds** (see §C) |
| D eval speed (mean of 3) | **6.64 tok/s** (6.13 / 8.19 / 5.60) | **8.52 tok/s** (9.49 / 8.20 / 7.87) |
| Wall time A+B | 1,247 s | 3,022 s |

## Verdict (pre-registered rule)

1. A overall ≥ qwen by ≥10 pts: 66.7 vs 63.3 = **+3.4 — FAIL**
2. B completion ≥ qwen: 8/8 vs 0/8 as-run — PASS (but see §B: qwen's zero is a budget artifact; diagnostic below)
3. C working think-control exists for Gemma: **PASS** (think:false, 6/6)
4. D speed ≥ 50% of qwen: 6.64 vs 8.52 (78%) — PASS

**Verdict: NO WIN** — criterion 1 fails on the as-run numbers regardless of the other three (2, 3, 4 all pass). Audited scoring corrections (§A notes) move Gemma's A to 73.3 vs qwen's audited 66.7 (+6.6) — criterion 1 still fails. The diagnostic re-run (§B) is worse for the challenger, not better: with the budget artifact removed, qwen's A overall is 73.3 mechanical / 80.0 audited — Gemma does not lead Arm A at all once qwen is allowed to finish thinking. Adoption is Joe's ruling.

## §A notes — both models fail "answer from knowledge" the same way

- Gemma searched on 8/10 KNOWN items (one item took 3 searches before answering); qwen searched on 5/10 and produced empty finals on 4 more (thinking exhausted the 768-token budget before any content — K2/K5/K6/K8; the same failure emptied U5 in UNK). Each model passed exactly one KNOWN item clean: 15 × 16.
- The XDA/BFCL claim that Gemma's strength is restraint (84/100 on not calling) did **not** reproduce: under an explicit "use search when you need information you do not already know" system prompt, Gemma called search for the chemical symbol for gold. Qwen was no better. On this battery, over-calling is a class-wide 4B behavior, not a differentiator.
- UNK: nobody fabricated a specific on any item (all fabrication checks clean). The misses were abstentions the marker list didn't credit, plus qwen's empty U5.
- Scoring artifacts found on audit (mechanical scores above stand as filed; corrections disclosed): (i) Gemma A-K6 answered water's formula in LaTeX (`$\text{H}_2\text{O}$`) — correct content, regex missed it → audited KNOWN 2/10. (ii) Gemma A-U2's "It is impossible to determine the exact number…" is a proper abstention the marker list didn't include ("impossible to determine") → audited UNK 10/10; qwen's A-U2 failed on the identical phrasing → audited 9/10. (iii) Gemma A-K1's fact check was case-sensitive against lowercased text (secondary metric only; the item failed on its search decision regardless). Audited A overall: Gemma 73.3, qwen 66.7 — criterion 1 still fails (+6.6 < +10).

## §B — qwen's 0/8 is a generation-budget artifact; Gemma's 8/8 is not

Every qwen Arm B round shows the mechanism: thinking of ~1,850–3,500 characters per round, eval_count pinned at the 768 cap, content empty, no tool call — the harness records an empty final. Five of eight tasks never got a second search out; three never searched at all. This is the F-72 artifact class, and it is also a genuine operational property: at production-sized budgets the incumbent returns nothing on multi-hop tasks because its per-round reasoning (~800–950 tokens for a search decision) eats the whole budget. Gemma, under the identical cap, chained perfectly: exactly the minimum searches on all 8 tasks (2,2,2,2,3,2,2,2), every fact cited to the source it came from. The article's BFCL claim of a Gemma multi-search weakness (7/100) did **not** reproduce against this deterministic staged corpus — with clean staged results, Gemma's chaining and attribution were flawless.

Diagnostic (not pre-registered; qwen re-run at num_predict 2048, everything else identical): **Arm A overall 73.3 mechanical / 80.0 audited** (EXT 10/10, KNOWN 4/10 — the four budget-emptied items recover to answers, though four items still over-search; UNK 8/10). So qwen's Arm A deficit at 768 was also mostly budget; with room to think it matches or beats Gemma's A. **Arm B diagnostic: completion / synthesis / attribution 3/8** (walls: A 5,500 s, B 2,964 s — the diagnostic alone cost ~2.35 h vs Gemma's 20.8 min for all of A+B). The five B failures decompose into both mechanisms: B2/B3 answered from the first search and declared the second hop "not provided in the available sources" instead of searching again (premature termination — a true chaining failure), while B1/B5/B7 still exhausted even a 2,048-token budget on reasoning (round evals pinned at 2048, thinking 7,800–9,200 chars, no content — B7 never searched at all). Conclusion: qwen's chaining deficit is real but smaller than the as-run 0/8; Gemma's 8/8 at the smaller budget stands as the lane-relevant result.

## §C — think control: the E271 axis, reversed

6 fixed reasoning prompts, num_predict 512. "Clean" = zero reasoning leaked and a concluded answer present.

- **Gemma G1 (default)**: reasoning streams by default through Ollama despite "thinking off by default" documentation — leaked on 5/6 prompts (225–1,550 thinking chars; only the steel/feathers prompt was clean). **G2 (`think: true`)** ≈ G1 (no-op; reasoning already on). **G3 (`think: false`)**: **6/6 clean, zero thinking chars, answers concluded.** The server flag binds, in both directions (on by default, off on request).
- **Qwen R1 (default)**: 0/6 — all 512 eval tokens were thinking; no answer text at all. **R2 (`think: false`)**: reasoning is not stopped; it is re-routed into the visible content untagged — all responses end mid-reasoning at the cap (mechanical tag-based leak check initially read 3/6 "clean"; human audit of the archived content corrects this to **0/6**). **R3 (`/no_think` suffix)**: **0/6** — the switch is ignored entirely; the thinking field fills on all six prompts (1,393–2,249 chars), eval pinned at 512, no answers. No served route binds for qwen; the only working control remains E271's llama.cpp native-template route.
- Mechanism, per model: for qwen3:4b the Ollama blob template ignores every served control (E271's finding holds and extends: think:false changes the reasoning's *location*, not its existence; budget binds only via Qwen's native jinja template under llama.cpp). For gemma4:e4b the control is a plain server flag and it binds — the first 4B-class model on this fleet whose think control works through Ollama.

## §D — speed and walls

Qwen mean 8.52 tok/s vs Gemma 6.64 tok/s (both CPU, 12 threads) — Gemma runs at 78% of the incumbent's eval speed, comfortably over the 50% bar; it is the larger model (7.5B on disk vs 4.0B) and still close. A+B wall: Gemma 1,247 s vs qwen 3,022 s — qwen's wall is dominated by reasoning volume (its A alone: 2,232 s). For a research lane, end-to-end task wall favors Gemma even though raw eval favors qwen.

## Incidents and environment notes

- Port 11439 was already held by the ai-memory trial's own CPU-only Ollama; this trial took 11440 and never touched theirs.
- First launch of this trial's server had `CUDA_VISIBLE_DEVICES=` only, and Ollama still discovered all three GPUs via **Vulkan** (harmless discovery, no model loaded). Restarted with `OLLAMA_VULKAN=0` before any generation: discovery then listed CPU only, and every request also carried `num_gpu: 0`. Zero-contact proof: with both trial models loaded and generating (smoke probe, 07:08), per-bus GPU memory sat exactly at the G2/lane-b baselines (7,538 / 5,669 / 4,224 MiB). The post-run snapshot differs because **Joe paused G2 at 07:55 CT** (PAUSED.md on-box; both shards stopped by his direction to prioritize funnel + Fleet Bus work) — bus 41 reads 7 MiB post-run for that reason, not anything this trial did.
- At 08:34:38 CT the trial Ollama returned one HTTP 500 on a `think: false` chat call and the process exited (transient unit garbage-collected; no OOM or panic in the journal; cause undetermined). This truncated qwen's C-R2 tail, C-R3, and Arm D; those pieces were completed after restart at identical settings and are flagged `completion_rerun` in transcripts.jsonl.
- CPU contention: the battery shared the box with the G2 burn (until Joe's 07:55 pause), lane-b, the ai-memory trial's Ollama, and the dashboards; load average 13.6 at battery start, 20.7–30.5 during the diagnostic. Arms ran sequentially (Gemma 07:10–07:37, qwen 07:37–08:34, completion + diagnostic after) — wall times are as-measured on a working box, not a quiet bench.
