#!/usr/bin/env python3
"""Reproduce the calibration numbers with the shipped scorer.

    python3 calibration/run_calibration.py

1. Scores every card in calibration/cards with ai-replaceability-check/scripts/score.py
   and checks the result against the expected values recorded at export time.
2. Reports compatibility and rank correlation per round.
3. Recomputes the SHA-256 fingerprints of the two locked blind-test predictions.
"""
import hashlib, json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent / "ai-replaceability-check" / "scripts"))
import score  # noqa: E402

COMPAT = {"High risk": {1, 2}, "One moat": {2, 3}, "Hard to replace": {3, 4}}

def rank(xs):
    order = sorted(range(len(xs)), key=lambda i: xs[i]); r = [0.0] * len(xs); i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        for k in range(i, j + 1):
            r[order[k]] = (i + j) / 2 + 1
        i = j + 1
    return r

def spearman(a, b):
    ra, rb = rank(a), rank(b); n = len(a); ma, mb = sum(ra) / n, sum(rb) / n
    cov = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
    return cov / ((sum((x - ma) ** 2 for x in ra) * sum((y - mb) ** 2 for y in rb)) ** 0.5)

index = json.loads((ROOT / "cards" / "outcomes.json").read_text(encoding="utf-8"))
regress = 0
by_round = {}
for e in index:
    r = score.score(json.loads((ROOT / "cards" / e["file"]).read_text(encoding="utf-8")))
    if r["level"] != e["expected_level"] or abs(r["overall"] - e["expected_overall"]) > 0.05:
        regress += 1
        print(f"REGRESSION {e['name']}: {r['level']} {r['overall']} vs {e['expected_level']} {e['expected_overall']}")
    by_round.setdefault(e["round"], []).append((e, r))
print(f"Regression check: {len(index) - regress}/{len(index)} match the recorded results\n")

def report(label, rows):
    ok = [e for e, r in rows if e["outcome"] in COMPAT[r["level"]]]
    miss = [f"{e['name']} ({r['level']} vs {e['outcome_label']})" for e, r in rows if e["outcome"] not in COMPAT[r["level"]]]
    rho = spearman([r["overall"] for _, r in rows], [e["outcome"] for e, _ in rows])
    print(f"{label:<34} compatible {len(ok)}/{len(rows)}   rho={rho:.3f}   misses: {'; '.join(miss) or 'none'}")

for rnd, label in [("round1", "Round 1 (in-sample calibration)"), ("round2", "Round 2 (blind, rules now v4)"), ("round3", "Round 3 (blind, rules now v4)")]:
    report(label, by_round[rnd])
report("All 41", [x for rows in by_round.values() for x in rows])

print("\nLocked out-of-sample results (the rules in force when predictions were locked):")
print("  Round 2, rules v2: 10/14 compatible, rho 0.720")
print("  Round 3, rules v3: 10/13 compatible, rho 0.622")

src = ROOT / "source"
h2 = hashlib.sha256((src / "products_blind.py").read_bytes() + (src / "blind_predictions.md").read_bytes()).hexdigest()
h3 = hashlib.sha256((src / "products_blind2.py").read_bytes() + (src / "blind2_predictions.md").read_bytes() + (src / "score_v3.py").read_bytes()).hexdigest()
print(f"\nFingerprints of the locked predictions:")
print(f"  Round 2: {h2}  {'OK' if h2.startswith('dffe3cf5') else 'MISMATCH'}")
print(f"  Round 3: {h3}  {'OK' if h3.startswith('12f9f6e9') else 'MISMATCH'}")
