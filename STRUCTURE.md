# Structure

```
fleet-findings-repo/
├── README.md                  — what this is, honesty rules, scope
├── STRUCTURE.md               — this file
├── methodology/
│   └── methodology.md         — experiment design, checker rules, adoption standard
├── platforms/
│   ├── README.md              — why fingerprints gate every finding
│   ├── mint.md                — Mint (ASUS ROG GL752VW) fingerprint + baselines — SETTLED
│   └── fortress-provisional.md— Fortress (HP Z820) fingerprint — SETTLED (filename kept from the provisional era)
├── findings/
│   ├── README.md              — index of seeded findings + what's not seeded (and why)
│   └── YYYY-MM-DD-<slug>.md   — one adopted/certified result per file
├── contributions/
│   ├── README.md              — upstream tracker (drafted / sent / status)
│   └── <slug>-DRAFT.md        — individual contribution drafts, clearly marked
└── evals/
    └── README.md              — frozen eval set descriptions (what + size, not raw text)
```

## Conventions

- **One finding per file**, dated by its adoption/certification date, named
  `YYYY-MM-DD-<short-slug>.md`.
- Every finding carries the same fields: **Platform fingerprint · Question ·
  Method · Measured result · Verdict · Source record** (the private ledger entry
  it was exported from, cited by experiment id + tuning entry number).
- A finding is eligible only when it is **ADOPTED or CERTIFIED** in the working
  program. Proposed, bar-met-but-unadopted, and pending-decision results do not
  appear as findings (they may appear in `contributions/` if an upstream draft
  depends on them).
- Platform pages are versioned by the fingerprint itself: any change to driver,
  serving-stack version, or service environment is a fingerprint change and is
  recorded on the platform page with its date.
- Contribution drafts live in `contributions/` until sent; the tracker records
  where each was sent and its upstream status. **Drafting is automatic;
  posting is per-item owner-approved. Nothing in this folder is sent by
  being written.**
