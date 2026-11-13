# A guarded instance restart is not a session variable (F-97)

- **Date:** 2026-11-12 (certified)
- **Platform:** Fortress — Windows/Vulkan Ollama lane, the
  :11435 (serve-second) instance only; see
  `platforms/fortress-provisional.md` for the machine
- **Source record:** FORTRESS-BACKLOG-2026-11-12.md item
  A28; on-box RESULTS, run `backlog-a-2026-11-12`

## Question

Does restarting the serving instance itself (stop the
:11435 process, relaunch via the captured recipe)
re-draw outputs — beyond what a model reload does?

## Method

Guarded restart per the item (only the :11435 PID
stopped; relaunch via the captured serve recipe;
`/api/tags` verified), then 3B Trap-60 ×2 + 8B Trap-60
×1, across the item's restart blocks. Bar: restart is
the session variable iff its hash-change rate exceeds
A5's reload rate (which was 0 — F-74).

## Measured result

- 3B trap hashes after restart: `b6db228d…`,
  `b6db228d…`, `b6db228d…` — **changes = false**. The
  post-restart draw is the same draw the reload cycles
  serve (F-74).

## Verdict

**CERTIFIED.** Instance restart changes nothing the
reload doesn't — which is nothing. The lane can be
restarted operationally without invalidating any
session read taken on it.
