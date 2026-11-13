# Per-label isolation: two of Qwythos's trap misses are item-intrinsic, one is context-induced (F-88)

- **Date:** 2026-11-12 (certified)
- **Platform:** Fortress — Windows/Vulkan Ollama lane, the
  :11435 (serve-second) instance only; see
  `platforms/fortress-provisional.md` for the machine
- **Source record:** FORTRESS-BACKLOG-2026-11-12.md item
  A19; on-box RESULTS, run `backlog-a-2026-11-12`

## Question

For each of Qwythos's standing Trap-60 misses, is the
miss a property of the item (misses alone too) or of
the bulk context (passes in isolation)?

## Method

Trap-60 split into its 5 gold label groups (12 titles
each, count-adjusted sub-prompts), one call per group.
Each baseline miss is classified item-intrinsic (misses
in both) or context-induced (passes in isolation).
Evaluation-only; nothing entered any prompt or training
set.

## Measured result

- Baseline misses under classification: titles **11,
  23, 49**.
- Per-group strict in isolation: TEACHING **11/12**,
  COMEDY **6/12**, GRAPHIC-NOVEL ACTION **10/12**,
  SPOT-THE-MISTAKE **12/12**, SEASONAL **10/12**.
- Classifications as recorded: title 49 (COMEDY) —
  **item-intrinsic**; title 11 (GRAPHIC-NOVEL ACTION) —
  **item-intrinsic**; title 23 (SEASONAL) —
  **context-induced**.

## Verdict

**CERTIFIED.** Qwythos's trap misses are mostly items,
not context: two of the three named misses fail in
isolation too. The COMEDY group's weak isolation score
(6/12) is recorded as measured — isolation is a
different, harder read for that label, and no stronger
claim is filed from it.
