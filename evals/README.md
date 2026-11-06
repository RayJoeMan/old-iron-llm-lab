# Frozen eval sets — descriptions

An agent without a fixed eval is a habit, so every finding names its set.
This page describes **what each set measures and how big it is**. 

> **Inclusion rule applied at staging:** raw eval text (prompts, title lists,
> source paragraphs, ruler value lists, cover images) is **excluded** from
> this scaffold in every case where there is any doubt about sensitivity.
> The sets live with the private working ledgers. What *is* reproduced in
> `findings/` is limited to adopted brief/instruction lines — fixed,
> non-sensitive instructional text that is itself the finding (e.g. the
> summary coverage line). If this repo is ever published, each set below
> gets a fresh sensitivity pass before any raw text is added.

| Set | Used by | Size | What it measures |
|---|---|---|---|
| **B1 benchmark** | Structured drafting | 2 fixed entries, validator-scored; production read = full 20-entry blocks | Format-contract compliance as-emitted (fixed strings, numbering, per-entry hook line), plus editorial-edit load |
| **B2 benchmark** | Summary | 1 fixed source paragraph | Exactly-3-bullets discipline + **zero invented facts** |
| **Standard summary set (E93 set)** | Summary | Fixed multi-paragraph sources, 30 scored facts | Numeric/factual coverage under the adopted brief; the set behind the 27/30 (champion) and 30/30 (fallback) records |
| **55-value ruler (E111)** | Summary, long-input | 55 scored numeric values in one long source | Single-pass vs chunked coverage (9/55 vs 50/55 union) — the set that proved the chunking rule |
| **25-value ruler (E151/E167)** | Summary merge loop | 25 scored values across chunked finals | Merge-stage coverage pre/post repair (25/25 post-repair is the adopted bar) |
| **Coverage curve set (E130)** | Summary | Sources at 10 / 20 / 40 / 60 figures | Where single-pass coverage collapses (100% → 37% at 60 figures) |
| **B3 benchmark** | Classification | 10 fixed titles | Lane-label accuracy against a fixed key (monthly-loop probe) |
| **Standard classification set** | Classification | 30 fixed titles | Accuracy on a *pattern-built* set — the instrument that exposed the zero-anchor positional-cycle failure (see the gemma fallback finding) |
| **Hard classification set** | Classification | 60 fixed titles, key registered before the run | Accuracy on *irregular* titles; per-family scores across 5 labels, 12 each |
| **B4 packet set** | Packet drafting | 1 fixed packet, scored per 5 entries | Sport-bleed (wrong-sport vocabulary), hero-opening drift, editorial edits /5 |
| **Metadata protocol (E81)** | Metadata | 8 fixed batch prompts × 5 pairs = 40 pairs | Pairs delivered, Title:/Description: label compliance, hook-form rate, word limits, forbidden content |
| **Filler-fact gold set** | Summary QA scanner | Definition-built gold set, 11 filler instances | Scanner precision/recall against a *definition*, not against another model's opinion |
| **VL cover set** | Vision alt-text | 20 fixed cover images, human-verified ground truth | Clean descriptions, ≤30-word length compliance, zero marketing language, correct people counts, cross-sport confusion |
| **Hook-bank instrument** | Hook generation | The 50-item production brief itself | Hook-form compliance, length rate, forbidden content, near-duplicate pairs (embedding + token-overlap), shared openers |
| **Judge-pair QA set** | Checker protocol | 20 fixed entries with a planted-defect key | Guest-judge agreement, false positives, recall — the set that validated (and bounded) the judge pair |

## Notes

- **Deterministic lanes pin seed 42** for benchmark/QA runs (production
  draws on creative lanes stay unseeded where variety is the point).
- **Strict = semantic** on classification since the hard-set work:
  abbreviations count; the fixed key is the checker — no model grades
  classification.
- The B2/B3 sets double as the monthly regression probes; the certification
  wave re-runs champion contracts verbatim against the recorded scores and
  reports regressions instead of repairing them mid-run.
