#!/usr/bin/env python3
"""Fleet Bus v3 scoring analysis. Reads the six runs' metrics + call
logs + verdicts + C3 staging artifacts from ./metrics and computes:
the win bar (C3 vs fresh B), the improvement yardstick (C3 vs C2ref),
per-class tokens-per-error-free-job, B per-task attribution, the
C3-attempt-1-shipped counterfactual (A6), per-rung VERIFY pass rates,
kill-adjusted walls, and per-task token tables. All definitions per
DESIGN.md §5 as amended."""
import json, os, sys, glob

HERE = os.path.dirname(os.path.abspath(__file__))
M = os.path.join(HERE, "metrics")
sys.path.insert(0, os.path.join(HERE, "..", "code"))
import validators

WL = json.load(open(os.path.join(HERE, "..", "code", "workload.json")))
KIND = {t["id"]: t["kind"] for t in WL["tasks"]}
GOLD = WL["gold"]
TASKS = {t["id"]: t for t in WL["tasks"]}
CLASSES = ("CLASSIFY", "DRAFT", "VERIFY")

def load(name):
    return json.load(open(os.path.join(M, name)))

RUNS = {
    "B1": load("B-run1-metrics.json"), "B2": load("B-run2-metrics.json"),
    "C2ref1": load("C2ref-run1-metrics.json"), "C2ref2": load("C2ref-run2-metrics.json"),
    "C31": load("C3-run1-metrics.json"), "C32": load("C3-run2-metrics.json"),
}
ARM_RUNS = {"B": ["B1", "B2"], "C2ref": ["C2ref1", "C2ref2"], "C3": ["C31", "C32"]}

def correct(m):
    return m["tasks_terminal"] - len(m.get("shipped_wrong", []))

def agg(arm):
    ms = [RUNS[r] for r in ARM_RUNS[arm]]
    return {
        "wall": sum(m["wall_s"] for m in ms),
        "tokens": sum(m["work_tokens"] for m in ms),
        "calls": sum(m["work_calls"] for m in ms),
        "correct": sum(correct(m) for m in ms),
        "accounted": sum(m["tasks_accounted"] for m in ms),
        "shipped_wrong": sum(len(m.get("shipped_wrong", [])) for m in ms),
        "dlq": sum(len(m.get("deadlettered", [])) for m in ms),
        "lost": sum(len(m["lost"]) for m in ms),
    }

# ---------- B per-task attribution (call ts <-> result-file mtime zip,
# validated by prompt length against the C-arm reference table) ----------
PROMPT_CHARS = {}
for r in ("C2ref1", "C2ref2", "C31", "C32"):
    for line in open(os.path.join(M, dict(C2ref1="C2ref-run1", C2ref2="C2ref-run2", C31="C3-run1", C32="C3-run2")[r] + "-call_log.jsonl")):
        e = json.loads(line)
        if e.get("task"):
            PROMPT_CHARS.setdefault(e["task"], set()).add(e["prompt_chars"])
PROMPT_CHARS = {k: sorted(v) for k, v in PROMPT_CHARS.items()}

B_FILES = {  # (mtime, task) from the on-box ls of runs/B-run<n>/results
    "B1": [(1794715335, "v3"), (1794715403, "d6"), (1794715508, "d4"), (1794715600, "v4"),
           (1794715702, "d1"), (1794715748, "c4"), (1794716382, "v1"), (1794715837, "v2"),
           (1794716037, "c3"), (1794716181, "d3"), (1794716573, "c2"), (1794716775, "d2"),
           (1794716869, "v5"), (1794717045, "d5"), (1794717247, "v6"), (1794717290, "c5"),
           (1794717330, "c1"), (1794717388, "c6")],
    "B2": [(1794728557, "c5"), (1794728755, "d4"), (1794728847, "v2"), (1794728994, "v3"),
           (1794729136, "d5"), (1794729187, "c2"), (1794729245, "c6"), (1794729442, "d1"),
           (1794729615, "c4"), (1794729812, "d6"), (1794729850, "c1"), (1794729989, "v5"),
           (1794730186, "v6"), (1794730384, "v1"), (1794730455, "d3"), (1794730602, "v4"),
           (1794730777, "d2"), (1794730973, "c3")],
}

def b_per_task(run):
    calls = []
    for line in open(os.path.join(M, f"B-run{run[-1]}-call_log.jsonl")):
        e = json.loads(line)
        if e.get("purpose") == "work":
            calls.append(e)
    calls.sort(key=lambda e: e["ts"])
    files = sorted(B_FILES[run])
    assert len(calls) == len(files) == 18, (len(calls), len(files))
    out, mismatches = {}, 0
    for e, (mt, tid) in zip(calls, files):
        if e["prompt_chars"] not in PROMPT_CHARS.get(tid, []):
            mismatches += 1
        out[tid] = {"tokens": e["prompt_eval_count"] + e["eval_count"], "calls": 1,
                    "by_model": {e["model"]: e["prompt_eval_count"] + e["eval_count"]}}
    total = sum(v["tokens"] for v in out.values())
    assert total == RUNS[run]["work_tokens"], (total, RUNS[run]["work_tokens"])
    return out, mismatches

PER_TASK = {}
for r in ("B1", "B2"):
    PER_TASK[r], mm = b_per_task(r)
    print(f"[attribution] {r}: 18 tasks, prompt-length mismatches={mm}, totals exact")
for r in ("C2ref1", "C2ref2", "C31", "C32"):
    PER_TASK[r] = RUNS[r]["per_task_tokens"]

def class_correct(arm):
    out = {c: 0 for c in CLASSES}
    for r in ARM_RUNS[arm]:
        m = RUNS[r]
        wrong = set(m.get("shipped_wrong", []))
        for tid, st in m["task_states"].items():
            if st == "done" and tid not in wrong:
                out[KIND[tid]] += 1
    return out

def class_tokens(arm):
    out = {c: 0 for c in CLASSES}
    for r in ARM_RUNS[arm]:
        for tid, v in PER_TASK[r].items():
            out[KIND[tid]] += v["tokens"]
    return out

def efj_table(arm):
    ct, cc = class_tokens(arm), class_correct(arm)
    rows = {}
    for c in CLASSES:
        rows[c] = (ct[c], cc[c], round(ct[c] / cc[c], 1) if cc[c] else None)
    a = agg(arm)
    rows["ALL"] = (a["tokens"], a["correct"], round(a["tokens"] / a["correct"], 1))
    return rows

# ---------- win bar: C3 vs fresh B ----------
A_B, A_C3, A_C2 = agg("B"), agg("C3"), agg("C2ref")
bar = {}
bar[1] = all(RUNS[r]["lost"] == [] and RUNS[r]["duplicated_work"] == {} for r in ARM_RUNS["C3"])
bar[2] = all(RUNS[r]["tasks_accounted"] == 18 for r in ARM_RUNS["C3"]) and A_C3["accounted"] >= A_B["accounted"]
bar[3] = A_C3["shipped_wrong"] < A_B["shipped_wrong"]
bar[4] = A_C3["dlq"] <= 4 and all(len(RUNS[r].get("deadlettered", [])) <= 3 for r in ARM_RUNS["C3"])
bar[5] = A_C3["wall"] <= 1.25 * A_B["wall"]
bar[6] = all(RUNS[r]["coord_tokens"] == 0 for r in ARM_RUNS["C3"])
bar[7] = True  # interventions: 0 for both arms in all scored runs (run ledger)
bar[8] = json.load(open(os.path.join(M, "gate-results3.json")))["gate_pass"] is True

# ---------- yardstick: C3 vs C2ref ----------
c3_efj = A_C3["tokens"] / A_C3["correct"]
c2_efj = A_C2["tokens"] / A_C2["correct"]
c3_ratio = A_C3["wall"] / A_B["wall"]
c2_ratio = A_C2["wall"] / A_B["wall"]
cc3, cc2 = class_correct("C3"), class_correct("C2ref")
yard = {
    "(i) no bar leg lost vs v2 pass set": all(bar[i] for i in (1, 2, 3, 4, 6, 7, 8)),
    "(ii) tok/efj beats C2ref by >=3%": c3_efj < c2_efj * 0.97,
    "(iii) wall ratio beats C2ref by >=0.05": c3_ratio < c2_ratio - 0.05,
    "(iv) correct >= C2ref and shipped-wrong == 0": A_C3["correct"] >= A_C2["correct"] and A_C3["shipped_wrong"] == 0,
    "(v) class floors (within 1 of C2ref)": all(cc3[c] >= cc2[c] - 1 for c in CLASSES),
}

# ---------- C3-attempt-1-shipped counterfactual (A6) ----------
def counterfactual(run):
    sdir = os.path.join(M, f"C3-run{run[-1]}-staging")
    first = {}
    for p in glob.glob(os.path.join(sdir, "*.txt")):
        base = os.path.basename(p)
        tid = base.split("__")[0]
        att = int(base.rsplit("__a", 1)[1].split(".")[0])
        if tid not in first or att < first[tid][0]:
            first[tid] = (att, open(p).read())
    calls = {}
    for line in open(os.path.join(M, f"C3-run{run[-1]}-call_log.jsonl")):
        e = json.loads(line)
        if e.get("task"):
            calls.setdefault(e["task"], []).append(e)
    tokens, wrong, corr = 0, [], 0
    for tid, (att, art) in sorted(first.items()):
        spent = sum(e["prompt_eval_count"] + e["eval_count"]
                    for e in calls.get(tid, []) if e["attempt"] <= att)
        tokens += spent
        ok, _ = validators.validate(TASKS[tid], GOLD[tid], art)
        if ok:
            corr += 1
        else:
            wrong.append(tid)
    return {"tasks_shipped": len(first), "tokens": tokens, "correct": corr,
            "shipped_wrong": sorted(wrong),
            "tok_per_efj": round(tokens / corr, 1) if corr else None}

CF = {r: counterfactual(r) for r in ("C31", "C32")}
CF_AGG = {"tokens": sum(v["tokens"] for v in CF.values()),
          "correct": sum(v["correct"] for v in CF.values()),
          "shipped_wrong": sum(len(v["shipped_wrong"]) for v in CF.values())}
CF_AGG["tok_per_efj"] = round(CF_AGG["tokens"] / CF_AGG["correct"], 1)

# ---------- VERIFY/CLASSIFY/DRAFT pass by (attempt, model) ----------
def ladder(arm, kind, attempt):
    if arm == "C2ref":
        return "qwen3:4b" if attempt <= 2 else "qwen3:8b"
    strong_first = kind in ("VERIFY", "CLASSIFY")
    odd = attempt % 2 == 1
    return ("qwen3:8b" if odd else "qwen3:4b") if strong_first else ("qwen3:4b" if odd else "qwen3:8b")

def rung_stats(arm):
    stats = {}
    for r in ARM_RUNS[arm]:
        fn = dict(C2ref1="C2ref-run1", C2ref2="C2ref-run2", C31="C3-run1", C32="C3-run2")[r]
        for line in open(os.path.join(M, fn + "-verdicts.jsonl")):
            e = json.loads(line)
            key = (KIND[e["task"]], e["attempt"], ladder(arm, KIND[e["task"]], e["attempt"]))
            s = stats.setdefault(key, {"n": 0, "pass": 0})
            s["n"] += 1
            s["pass"] += 1 if e["passed"] else 0
    return stats

# ---------- report ----------
print("\n=== AGGREGATES ===")
for arm in ("B", "C2ref", "C3"):
    a = agg(arm)
    print(f"{arm}: wall {a['wall']} | tokens {a['tokens']} | calls {a['calls']} | correct {a['correct']} "
          f"| accounted {a['accounted']} | shipped_wrong {a['shipped_wrong']} | dlq {a['dlq']} | lost {a['lost']} "
          f"| tok/efj {a['tokens']/a['correct']:.1f}")
print("\n=== WIN BAR (C3 vs fresh B) ===")
for i in range(1, 9):
    print(f"leg {i}: {'PASS' if bar[i] else 'FAIL'}")
print("BAR:", "CLEARED" if all(bar.values()) else "NOT CLEARED",
      f"| wall ratio C3/B = {c3_ratio:.3f} (cap 1.25) | C2ref/B = {c2_ratio:.3f}")
print("\n=== YARDSTICK (C3 vs C2ref) ===")
for k, v in yard.items():
    print(f"{k}: {'PASS' if v else 'FAIL'}")
print(f"tok/efj: C3 {c3_efj:.2f} vs C2ref {c2_efj:.2f} ({(1-c3_efj/c2_efj)*100:.1f}% better)")
print(f"class correct: C3 {cc3} vs C2ref {cc2}")
print("\n=== TOK/EFJ PER CLASS (tokens, correct, efj) ===")
for arm in ("B", "C2ref", "C3"):
    print(arm, efj_table(arm))
print("\n=== PER-RUN TOK/EFJ ===")
for r, m in RUNS.items():
    print(f"{r}: wall {m['wall_s']} tokens {m['work_tokens']} correct {correct(m)} efj {m['work_tokens']/correct(m):.1f}")
print("\n=== KILL-ADJUSTED WALLS (run 1s) ===")
for r in ("B1", "C2ref1", "C31"):
    m = RUNS[r]
    rec = m["recovery"]["latency_s"] if m.get("recovery") else None
    print(f"{r}: wall {m['wall_s']} recovery {rec} adjusted {round(m['wall_s']-rec,1) if rec else None}")
print("\n=== COUNTERFACTUAL C3-attempt-1-shipped (A6) ===")
print("per run:", CF)
print("aggregate:", CF_AGG, "vs B shipped_wrong", A_B["shipped_wrong"], "tok/efj", round(A_B['tokens']/A_B['correct'], 1))
print("\n=== RUNG STATS (kind, attempt, model) -> pass/n ===")
for arm in ("C2ref", "C3"):
    print(arm, dict(sorted(rung_stats(arm).items())))
print("\n=== PER-TASK TOKENS ===")
for r in ("B1", "B2", "C2ref1", "C2ref2", "C31", "C32"):
    print(r, {t: PER_TASK[r].get(t, {}).get("tokens", 0) for t in sorted(PER_TASK[r])})
print("\n=== DLQ PRICING ===")
for r in ("C2ref1", "C2ref2", "C31", "C32"):
    m = RUNS[r]
    print(r, "dlq:", m.get("deadlettered"), "dlq_tokens:", m.get("dlq_tokens"),
          {t: PER_TASK[r].get(t, {}).get("tokens") for t in m.get("deadlettered", [])},
          "early:", m.get("early_dlq"))
