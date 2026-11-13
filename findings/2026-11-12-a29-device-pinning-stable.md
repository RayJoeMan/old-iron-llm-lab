# Device pinning: stable hashes under single-device visibility, clean restore (F-98)

- **Date:** 2026-11-12 (certified)
- **Platform:** Fortress — Windows/Vulkan Ollama lane, the
  :11435 (serve-second) instance only; see
  `platforms/fortress-provisional.md` for the machine
- **Source record:** FORTRESS-BACKLOG-2026-11-12.md item
  A29; on-box RESULTS, run `backlog-a-2026-11-12`

## Question

Is device placement the hidden variable behind the
two-draw behavior (F-71) — i.e. do pinned launches hold
one hash while default launches wander?

## Method

Relaunch with single-device visibility
(GGML_VULKAN_DEVICE), server log checked to confirm the
change took; 3B Trap-60 ×2; then restore the default
launch and re-verify `/api/tags`. Bar: placement is the
variable iff pinned hashes are stable across relaunches
while default-launch hashes vary.

## Measured result

- Pinned hashes: `b6db228d…`, `b6db228d…` —
  **pinned_stable = true**; the default launch was
  restored and verified (**restored = true,
  ok_all = true**).
- The pinned draw is the battery's usual opening draw —
  the same hash reloads (F-74), restarts (F-97), and
  solo sessions serve. Default-launch hashes in this
  battery took both values (`b6db228d…` and
  `3c06f862…`, F-71/F-72), and the recorded mechanism
  for moving between them is session history (prefix,
  co-residency), measured directly.

## Verdict

**CERTIFIED.** Pinning is stable and operationally
clean, and it lands on the standard draw — but the
battery's own evidence assigns the two-draw selection
to session history, not to device placement wandering.
Pinning remains available as a hygiene measure; it is
not the explanation.
