#!/usr/bin/env python3
"""AI replaceability scorer (rules v4).

Reads one or more decomposition cards (JSON, schema in references/decompose.md),
applies the scoring rules in references/scoring.md, and prints the result.
Standard library only.

Usage:
    python3 score.py card.json                     # human-readable summary
    python3 score.py card.json --json              # machine-readable result
    python3 score.py card.json --svg radar.svg     # also draw the chart
    python3 score.py a.json b.json c.json          # score several and rank them
    python3 score.py a.json b.json --svg-dir out/  # one chart per card

All tables (scores, weights, thresholds) live in config.json next to this file.
"""

import argparse
import json
import math
import sys
from pathlib import Path
from xml.sax.saxutils import escape

CONFIG = json.loads((Path(__file__).resolve().parent / "config.json").read_text(encoding="utf-8"))
FE = CONFIG["frontend"]
BIZ = CONFIG["business"]
FE_KEYS = [a["key"] for a in FE]
BIZ_KEYS = [d["key"] for d in BIZ]
LABEL = {**{a["key"]: a["label"] for a in FE}, **{d["key"]: d["label"] for d in BIZ}}
LEVELS = CONFIG["levels"]
RELATION_NAMES = {"A": "replaced directly", "B": "callable but thin", "C": "data source",
                  "D": "executor", "E": "system of record", "F": "parallel"}


class CardError(ValueError):
    pass


# ---------------------------------------------------------------- helpers
def cls(field, where):
    """Return the class letter of a field that may be a string or {"class": ...}."""
    if isinstance(field, str):
        return field
    if isinstance(field, dict) and "class" in field:
        return field["class"]
    raise CardError(f"{where}: missing class")


def check_share(items, where):
    total = sum(i.get("share", 0) for i in items)
    if abs(total - 1.0) > 0.02:
        raise CardError(f"{where}: shares add up to {total:.2f}, expected 1.0")


def sub_score(aspect, field, where):
    """Score one frontend sub-category, including its modifier."""
    c = cls(field, where)
    table = next(a["scores"] for a in FE if a["key"] == aspect)
    if c not in table:
        raise CardError(f"{where}: '{c}' is not a valid class for {aspect} ({'/'.join(table)})")
    s = table[c]
    f = field if isinstance(field, dict) else {}
    if aspect == "frequency" and c in "DE" and f.get("automatable") == "automatable":
        s = {"D": 2, "E": 4}[c]
    if aspect == "precision" and c == "E" and f.get("recurring") is False:
        s = 1
    if aspect == "intent" and c in "CD" and f.get("content_source") == "ai_or_scraped":
        s = {"C": 1, "D": 3}[c]
    if aspect == "device" and c in "BCD" and f.get("platform_generic") is True:
        s = {"B": 0, "C": 2, "D": 4}[c]
    if aspect == "experience" and f.get("chat_reproducible") is True:
        s = min(s, 1)
    return s


def blend(table, primary, secondary, keys):
    """Type weights (primary 70% / secondary 30%) times calibration factors."""
    r = CONFIG["secondary_ratio"]
    base = table[primary] if not secondary else [(1 - r) * a + r * b for a, b in zip(table[primary], table[secondary])]
    return [w * CONFIG["calibration_factors"][k] for w, k in zip(base, keys)]


# ---------------------------------------------------------------- scoring
def score(card):
    name = (card.get("project") or {}).get("one_liner") or card.get("name") or "Untitled project"
    p, s = card.get("primary_type"), card.get("secondary_type")
    for t, field in ((p, "primary_type"), (s, "secondary_type")):
        if t is not None and t not in CONFIG["types"]:
            raise CardError(f"{field}: unknown type '{t}' (valid: {', '.join(CONFIG['types'])})")
    if p is None:
        raise CardError("primary_type is required")
    if s == p:
        s = None

    modes = card.get("modes") or []
    if not modes:
        raise CardError("modes: at least one usage mode is required")
    check_share(modes, "modes")

    # Frontend layer: share-weighted sub-category scores
    fe = {k: 0.0 for k in FE_KEYS}
    rel = 0.0
    mode_rel = []
    for i, m in enumerate(modes):
        where = f"modes[{i}] ({m.get('name', '?')})"
        steps = m.get("steps") or []
        if not steps:
            raise CardError(f"{where}: at least one step is required")
        check_share(steps, f"{where}.steps")
        for a in FE:
            k = a["key"]
            if a["level"] == "mode":
                fe[k] += m["share"] * sub_score(k, m.get(k), f"{where}.{k}")
            else:
                fe[k] += m["share"] * sum(st["share"] * sub_score(k, st.get(k), f"{where}.step.{k}") for st in steps)
        r_field = m.get("relation", card.get("ai_relation"))
        if r_field is None:
            raise CardError(f"{where}: relation is required")
        r = cls(r_field, f"{where}.relation")
        if r not in CONFIG["relation_scores"]:
            raise CardError(f"{where}.relation: '{r}' is not one of A-F")
        rel += m["share"] * CONFIG["relation_scores"][r]
        mode_rel.append({"name": m.get("name", f"mode {i + 1}"), "share": m["share"], "relation": r})
    fe = {k: round(v, 2) for k, v in fe.items()}

    # Business layer: level number is the score
    biz = {}
    for d in BIZ_KEYS:
        try:
            lv = card["business"][d]["level"] if isinstance(card["business"][d], dict) else card["business"][d]
            biz[d] = int(str(lv).lstrip("Ll"))
        except (KeyError, TypeError, ValueError):
            raise CardError(f"business.{d}: a level L0-L5 is required")
        if not 0 <= biz[d] <= 5:
            raise CardError(f"business.{d}: level must be L0-L5")

    fw = blend(CONFIG["frontend_weights"], p, s, FE_KEYS)
    bw = blend(CONFIG["business_weights"], p, s, BIZ_KEYS)
    fe_score = sum(w * fe[k] for w, k in zip(fw, FE_KEYS)) / (5 * sum(fw)) * 100
    gates = card.get("quality_gates") or {}
    failed_gates = [g for g, v in gates.items() if v == "fail"]
    if failed_gates:
        fe_score *= CONFIG["quality_gate_factor"]
    biz_score = sum(w * biz[k] for w, k in zip(bw, BIZ_KEYS)) / (5 * sum(bw)) * 100

    types = CONFIG["types"]
    r_ratio = CONFIG["secondary_ratio"]
    potential = types[p]["potential"] if not s else (1 - r_ratio) * types[p]["potential"] + r_ratio * types[s]["potential"]

    # Moat items (any item scoring >= threshold)
    items = {**fe, **biz}
    moats = [k for k, v in items.items() if v >= CONFIG["moat_threshold"]]
    excluded = []
    if card.get("deliverable_ai_replaceable"):
        excluded = [k for k in moats if k in CONFIG["transaction_dims"]]
        moats = [k for k in moats if k not in CONFIG["transaction_dims"]]
    complement = rel >= CONFIG["complement_at"]
    substitute = rel < CONFIG["substitute_below"]
    n = len(moats) + (1 if complement else 0)

    steps_log = []
    level = 0 if n == 0 else (1 if n == 1 else 2)
    steps_log.append(f"{n} moat item(s) -> {LEVELS[level]}")
    if substitute and level > 0:
        level -= 1
        steps_log.append(f"relation score {rel:.1f} < {CONFIG['substitute_below']} (substitute) -> {LEVELS[level]}")
    search = bool(card.get("search_acquisition") or (card.get("project") or {}).get("search_acquisition"))
    if search and substitute and level > 0:
        level -= 1
        steps_log.append(f"search-dependent acquisition + substitute relation -> {LEVELS[level]}")

    high_potential = potential >= 3
    diagnosis = {
        (True, True): "Structure and execution agree",
        (True, False): "Right direction, but the moat is not built yet (cold-start risk)",
        (False, True): "Risky direction, held up by a single strength",
        (False, False): "The direction itself is easy to replace",
    }[(high_potential, n > 0)]

    mix = CONFIG["overall_mix"]
    overall = (mix["potential"] * potential / 5 * 100 + mix["business"] * biz_score
               + mix["frontend"] * fe_score + mix["relation"] * rel)

    weights = {**dict(zip(FE_KEYS, fw)), **dict(zip(BIZ_KEYS, bw))}
    thr = CONFIG["moat_threshold"]
    nearest = sorted(((weights[k] / max(thr - v, 0.1), k, v) for k, v in items.items() if v < thr), reverse=True)[:3]

    risks = []
    if search and not substitute:
        risks.append("Search-dependent acquisition: AI search is taking answer-seeking traffic; watch the share of direct visits.")
    if card.get("ai_habit") and cls(card["ai_habit"], "ai_habit") in ("C", "D"):
        risks.append("Target users rarely use AI clients today. That is a time window, not a moat.")
    for g in failed_gates:
        risks.append(f"Quality gate failed: {g} (frontend score x{CONFIG['quality_gate_factor']}).")

    return {
        "name": name,
        "primary_type": types[p]["label"],
        "secondary_type": types[s]["label"] if s else None,
        "potential": round(potential, 1),
        "frontend": {LABEL[k]: v for k, v in fe.items()},
        "business": {LABEL[k]: v for k, v in biz.items()},
        "frontend_score": round(fe_score, 1),
        "business_score": round(biz_score, 1),
        "relation_score": round(rel, 1),
        "relation_by_mode": mode_rel,
        "relation_effect": "substitute" if substitute else ("complement" if complement else "neutral"),
        "moat_items": [LABEL[k] for k in moats] + (["Complementary to AI clients (D/E)"] if complement else []),
        "excluded_moats": [LABEL[k] for k in excluded],
        "verdict_steps": steps_log,
        "level": LEVELS[level],
        "diagnosis": diagnosis,
        "overall": round(overall, 1),
        "nearest_moats": [{"item": LABEL[k], "score": v, "priority": round(pr, 2)} for pr, k, v in nearest],
        "risks": risks,
        "assumptions": card.get("assumptions", []),
    }


# ---------------------------------------------------------------- output
def print_summary(r):
    print(f"\n=== {r['name']} ===")
    t = r["primary_type"] + (f" + {r['secondary_type']}" if r["secondary_type"] else "")
    print(f"Type: {t}   Structural potential: {r['potential']}")
    print(f"LEVEL: {r['level']}   ({r['diagnosis']})")
    for s in r["verdict_steps"]:
        print(f"  - {s}")
    print("Relation by usage mode:")
    for m in r["relation_by_mode"]:
        print(f"  {m['share']:>4.0%}  {m['relation']} ({RELATION_NAMES[m['relation']]})  {m['name']}")
    print(f"  relation score {r['relation_score']} -> {r['relation_effect']}")
    print("Frontend layer:")
    for k, v in r["frontend"].items():
        print(f"  {k:<26}{v:>5.2f}  {'#' * round(v)}")
    print("Business layer:")
    for k, v in r["business"].items():
        print(f"  {k:<26}{v:>5}  {'#' * v}")
    print(f"Moat items (>= {CONFIG['moat_threshold']:g}): {', '.join(r['moat_items']) or 'none'}")
    if r["excluded_moats"]:
        print(f"Excluded (deliverable is AI-replaceable): {', '.join(r['excluded_moats'])}")
    print(f"Scores: frontend {r['frontend_score']}  business {r['business_score']}  overall {r['overall']} (ranking only)")
    print("Nearest moats: " + "; ".join(f"{n['item']} ({n['score']})" for n in r["nearest_moats"]))
    for risk in r["risks"]:
        print(f"Risk: {risk}")


REL_COLOR = {"A": "#dc2626", "B": "#dc2626", "C": "#f59e0b", "F": "#9ca3af", "D": "#16a34a", "E": "#16a34a"}
FONT = "-apple-system,'Segoe UI','PingFang SC','Microsoft YaHei','Noto Sans CJK SC',sans-serif"


def _radar(out, cx, cy, radius, labels, values, title, color):
    n = len(labels)

    def pt(i, v):
        a = -math.pi / 2 + 2 * math.pi * i / n
        return cx + radius * v / 5 * math.cos(a), cy + radius * v / 5 * math.sin(a)

    out.append(f'<text x="{cx}" y="{cy - radius - 46}" text-anchor="middle" font-size="15" font-weight="600" fill="#111827">{escape(title)}</text>')
    for lv in range(1, 6):
        pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in (pt(i, lv) for i in range(n)))
        dash = ' stroke-dasharray="4 3"' if lv == 4 else ""
        out.append(f'<polygon points="{pts}" fill="none" stroke="{"#9ca3af" if lv == 4 else "#e5e7eb"}"{dash}/>')
    for i in range(n):
        x, y = pt(i, 5)
        out.append(f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" stroke="#e5e7eb"/>')
    pts = [pt(i, v) for i, v in enumerate(values)]
    out.append(f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="{color}" fill-opacity="0.18" stroke="{color}" stroke-width="2"/>')
    for x, y in pts:
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3" fill="{color}"/>')
    for i, (lab, v) in enumerate(zip(labels, values)):
        x, y = pt(i, 5.9)
        anchor = "middle" if abs(x - cx) < 5 else ("start" if x > cx else "end")
        weight = "700" if v >= CONFIG["moat_threshold"] else "400"
        out.append(f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" font-size="12" font-weight="{weight}" fill="#374151">{escape(lab)}</text>')
        out.append(f'<text x="{x:.1f}" y="{y + 15:.1f}" text-anchor="{anchor}" font-size="11" fill="#6b7280">{v:g}</text>')


def svg(r):
    w, h = 1080, 640
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="{FONT}">',
           f'<rect width="{w}" height="{h}" fill="#ffffff"/>',
           f'<text x="40" y="44" font-size="22" font-weight="700" fill="#111827">{escape(r["name"])}</text>',
           f'<text x="40" y="72" font-size="14" fill="#374151">Level: <tspan font-weight="700">{escape(r["level"])}</tspan>'
           f'  ·  {escape(r["diagnosis"])}  ·  overall {r["overall"]}</text>']
    _radar(out, 300, 315, 130, list(r["frontend"]), list(r["frontend"].values()), "Frontend layer", "#2563eb")
    _radar(out, 790, 315, 130, list(r["business"]), list(r["business"].values()), "Business layer", "#7c3aed")
    # relation bar
    y0, x0, bw = 560, 40, w - 80
    out.append(f'<text x="{x0}" y="{y0 - 12}" font-size="13" fill="#374151">Relation with AI clients by usage mode '
               f'(score {r["relation_score"]} → {r["relation_effect"]})</text>')
    x = x0
    for m in r["relation_by_mode"]:
        seg = bw * m["share"]
        out.append(f'<rect x="{x:.1f}" y="{y0}" width="{seg:.1f}" height="26" fill="{REL_COLOR[m["relation"]]}" fill-opacity="0.85" stroke="#fff"/>')
        label = f'{m["relation"]} · {m["name"]}'
        out.append(f'<text x="{x + 6:.1f}" y="{y0 + 17}" font-size="12" fill="#ffffff">{escape(label[: max(4, int(seg / 7.5))])}</text>')
        x += seg
    out.append(f'<text x="{w - 40}" y="{h - 14}" text-anchor="end" font-size="10" fill="#9ca3af">dashed ring = 4 (moat line) · '
               f'red = replaced/thin · amber = data source · gray = parallel · green = executor/system of record</text>')
    out.append("</svg>")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description="Score AI replaceability from decomposition cards (rules v4).")
    ap.add_argument("cards", nargs="+", help="decomposition card JSON file(s)")
    ap.add_argument("--json", action="store_true", help="print results as JSON")
    ap.add_argument("--svg", help="write a chart for the (single) card to this path")
    ap.add_argument("--svg-dir", help="write one chart per card into this directory")
    args = ap.parse_args()

    results = []
    for path in args.cards:
        try:
            card = json.loads(Path(path).read_text(encoding="utf-8"))
            results.append(score(card))
        except (CardError, json.JSONDecodeError) as e:
            sys.exit(f"{path}: {e}")

    if args.json:
        print(json.dumps(results if len(results) > 1 else results[0], ensure_ascii=False, indent=2))
    else:
        for r in results:
            print_summary(r)
        if len(results) > 1:
            print("\nRanking by overall score (for comparison only; the level is the verdict):")
            for i, r in enumerate(sorted(results, key=lambda x: -x["overall"]), 1):
                print(f"  {i}. {r['name']}: {r['overall']} ({r['level']})")

    if args.svg:
        Path(args.svg).write_text(svg(results[0]), encoding="utf-8")
    if args.svg_dir:
        d = Path(args.svg_dir)
        d.mkdir(parents=True, exist_ok=True)
        for path, r in zip(args.cards, results):
            (d / (Path(path).stem + ".svg")).write_text(svg(r), encoding="utf-8")


if __name__ == "__main__":
    main()
