# B4 stack brief — gold example + hook-reminder, at temp 0.3 only

- **Date:** 2026-11-05 (adopted)
- **Platform:** Mint — see `platforms/mint.md`
- **Source record:** TUNING #138; experiments E103, E134 (limits: E99, E118, E132)

## Question

A packet-shaped drafting class suffered two defect families: **sport-bleed**
(action vocabulary from the wrong sport) and **hero-opening drift**. A gold
example alone reached the action but did none of the contract work; a
reminder alone suppressed drift inconsistently. Does the *stack* — gold
example **plus** hook-reminder final line — beat both?

## Method

qwen3:8b, temp 0.3, the B4 packet fixed set, replication at n=3 per arm
against a pre-registered bar (bleed ≤1/5 on 2 of 3 calls; edits clearly
below the reminder-alone record).

## Measured result (E134 replication)

- **Stack:** bleed **0 / 0 / 2** per call; editorial edits mean **2.0/5**
- **Reminder alone:** edits mean **4.67/5**; its earlier drift suppression
  did **not** replicate (drift on 9/9 hero entries; bleed 2/2/2)
- Stack drift: present on exactly 1 of 3 calls — and **bimodal** (all-3
  or none per call), so the standard editorial pass is not optional on
  this lane

## Scope limits (measured, part of the adoption)

- **B4-class briefs only** — no transfer to the standard drafting brief
  (E118).
- **Temp 0.3 only** — the stack does not survive 0.7 (E132). Later
  measurements closed the other side too (0.2 also fails), so 0.3 is a
  measured lock, not a default.

## Verdict

**ADOPTED:** B4-class briefs use the E103 stack (gold example +
hook-reminder) on qwen3:8b at temp 0.3.
