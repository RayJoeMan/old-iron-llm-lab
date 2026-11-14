# SPEC — Gemma 4 E4B vs qwen3:4b head-to-head (research / tool-calling lane)

**Pre-registered 2026-11-14, before any battery run.** Joe-approved trial (Nov 14, 2026) following the XDA article by Nolen Jonker (Nov 13, 2026) claiming Gemma 4 E4B replaced a Gemini subscription for research, with tool calling as its strongest skill and a buried weakness: Berkeley Function Calling Leaderboard web category 7/100 (multi-search chaining) vs 84/100 on knowing when NOT to call a tool. Fleet stake: E271 / TUNING #288 proved qwen3:4b's reasoning-budget controls do not bind through its Ollama blob template — think-control is a known 4B pain axis on this fleet.

## Venue and hard constraints

- Fortress (HP Z820, 2× E5-2660 v2, 40 threads, 128 GB RAM), **CPU-only**. Both RTX 4000s belong to the G2 number-reader burn and the M4000 to lane-b; no GPU is touched. The trial runs as ONE private Ollama instance: user unit `gemma4-e4b-ollama.service`, `OLLAMA_HOST=127.0.0.1:11440`, private store `~/flane/trials/gemma4-e4b-2026-11-14/ollama-models`, `CUDA_VISIBLE_DEVICES=` (empty), `OLLAMA_NUM_PARALLEL=1`.
- Port note: 11439 was found occupied by the ai-memory trial's own CPU-only Ollama (`ollama-trial.service`, started 06:29 CT) — not touched; this trial took 11440.
- Model downloads run over Fortress's own internet connection, sequential (fleet discipline), never over the SSH bridge.

## Arms (same harness, same serving configuration — model-vs-model)

| Arm | Model | Source | Quant |
|---|---|---|---|
| Challenger | `gemma4:e4b` (Google Gemma 4 E4B, `google/gemma-4-E4B-it`) | Ollama library | Q4_K_M (library default) |
| Incumbent | `qwen3:4b` | Ollama library | Q4_K_M |

Exact digests recorded from the private store's `/api/tags` in results.json. Harness: Python 3 stdlib client on-box against `/api/chat`, identical for both arms. Fixed settings both arms: temperature 0, seed 42, num_ctx 4096, num_thread 12, one request at a time. System prompt (identical, verbatim in the harness): the model is a research assistant with a `web_search` tool returning sources with ids [S1], [S2]…; use it when it needs information it does not already know or that may have changed; cite source ids used; if it cannot find or does not know an answer, say so plainly instead of guessing.

## The mock tool (deterministic, offline)

`web_search(query)` is a local function with a canned corpus of fictional documents. Matching is by per-document trigger keywords (case-insensitive substring on the query); matching documents are returned in fixed corpus order, at most 3, each with a source id assigned in order of first presentation within the task (S1, S2, …). A query matching nothing returns an explicit "No results." There is no network access and no randomness: identical queries always return identical results.

## Arm A — TOOL-DECISION (30 prompts)

Three classes of 10. Each item allows up to 3 tool rounds; the decision and the final answer are both logged.

- **EXT** — the answer exists only in the mock corpus (fictional entities/events: a ferry fare, a zoning vote, a firmware version…). Correct decision = call `web_search` at least once. Secondary metric: final answer contains the canned fact string.
- **KNOWN** — timeless general knowledge (chemical symbol for gold, capital of Japan, 15 × 16…). Correct = answer directly with NO tool call, and the answer contains the expected fact.
- **UNK** — unknowable (my breakfast on a 2019 date, tomorrow's lottery numbers, a private diary's contents…). The mock returns no results for these even if searched. Correct = the final answer expresses uncertainty / declines (marker phrases) AND contains no fabricated specific (per-item fabrication patterns: specific values, quotes, counts, food items stated as fact).

Scores: per-class accuracy (correct/10), overall = mean of the three class accuracies, expressed in points (0–100).

## Arm B — MULTI-STEP RESEARCH (8 tasks)

Each task needs 2–3 chained searches: the mock returns the stage-(n+1) document only when the query contains the entity revealed by the stage-n document, so chaining is enforced by construction. Up to 5 tool rounds per task. Scored per task on three binary axes:

- **Completion** — final answer contains the terminal fact string.
- **Synthesis** — final answer contains every sub-fact string (each hop's fact).
- **Attribution** — final answer cites, for each fact, the source id of the document that actually contained it (citation ids checked mechanically against the presentation log).

## Arm C — THINK CONTROL (the E271 axis; 6 fixed reasoning prompts)

Prompts: bat-and-ball, machines/widgets, a syllogism trap, 17 + 25 × 2, sheep runaway, steel vs feathers. num_predict 512. Leak metric per response = tokens in the API `thinking` field + any think-block content inside the visible message; a route "binds" on a prompt iff leak = 0 and the visible answer is present.

Routes — qwen3:4b: **R1** chat default (no think field) · **R2** chat with `"think": false` · **R3** user prompt suffixed with `/no_think` (documented Qwen switch).
Routes — gemma4:e4b: **G1** chat default (Gemma 4 thinking is off by default per Google/docs) · **G2** chat with `"think": true` (does the documented enable actually produce reasoning? — proves the switch exists) · **G3** chat with `"think": false` (must match G1).

A model has a *working think-control configuration* iff at least one documented route yields leak = 0 on ≥5/6 prompts with answers intact (for Gemma, G2 must also show reasoning appears when explicitly enabled, i.e. the control binds in both directions). The exact mechanism per model (server flag vs prompt switch vs template property) is recorded either way. E271's llama.cpp native-template result for qwen3:4b is prior evidence and is cited, not re-run.

## Arm D — SPEED

3 fixed generation prompts (~150-word outputs, no tools), num_predict 256. Metric: eval tok/s from the API's own eval_count/eval_duration per prompt + mean. Also recorded: wall-clock duration of Arms A+B per arm (harness timestamps), host load average before/after the battery, and a post-run `nvidia-smi` check that all GPU memory figures are unchanged from pre-run (proving zero GPU contact).

## Pre-registered verdict rule

Gemma 4 E4B scores a **WIN** for the research lane only if ALL four hold:

1. Arm A overall ≥ qwen3:4b's overall **by ≥10 points**.
2. Arm B completion ≥ qwen3:4b's completion (task count, /8).
3. Arm C: a working think-control configuration exists for gemma4:e4b and is documented.
4. Arm D: gemma4:e4b mean eval speed ≥ **50%** of qwen3:4b's on the same lane.

Anything else = **NO WIN**, filed as measured. Adoption is Joe's ruling, never the trial's.

## Artifacts

Harness + battery definition: `~/flane/trials/gemma4-e4b-2026-11-14/work/` on Fortress, copied to this folder. Per-item transcripts + scores: `results.json` + `transcripts.jsonl` in this folder. Filing: F-75 in FORTRESS-TUNING.md; repo record under docs/gemma4-e4b-trial-2026-11-14/ in RayJoeMan/old-iron-llm-lab.
