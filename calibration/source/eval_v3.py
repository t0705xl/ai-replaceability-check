from cards_v3 import CALIB, BLINDC
from outcomes_blind import OUTCOMES
import score_v3 as v3, score_v2 as v2
from products import card as card1
from products_blind import card as cardb
from calibrate_v1 import spearman
COMPAT={"高风险":{1,2},"有一条护城河":{2,3},"较难替代":{3,4}}
def mark(level,o):
    if o in COMPAT[level]: return "✓"
    if (level=="高风险" and o>=3) or (level=="较难替代" and o<=2): return "✗"
    return "△"
def outcome(p): return p.get("outcome") or OUTCOMES[p["name"]][0]
def report(label, rows):
    out=[outcome(p) for p,_ in rows]; ok=sum(1 for p,r in rows if mark(r["final"],outcome(p))=="✓")
    sev=[p["name"] for p,r in rows if mark(r["final"],outcome(p))=="✗"]; mild=[p["name"] for p,r in rows if mark(r["final"],outcome(p))=="△"]
    print(f"{label:<26} 兼容 {ok}/{len(rows)}  ρ={spearman([r['overall'] for _,r in rows],out):.3f}  严重失准：{'、'.join(sev) or '无'}  轻度：{'、'.join(mild) or '无'}")
v2c=[(p,v2.score(card1(p,"v2"))) for p,_ in CALIB]; v2b=[(p,v2.score(cardb(p))) for p,_ in BLINDC]
v3c=[(p,v3.score(c)) for p,c in CALIB]; v3b=[(p,v3.score(c)) for p,c in BLINDC]
report("v2 · 第一轮样本",v2c); report("v2 · 盲测样本",v2b); report("v2 · 合计 28",v2c+v2b)
report("v3 · 第一轮样本",v3c); report("v3 · 盲测样本",v3b); report("v3 · 合计 28",v3c+v3b)
print()
for p,r in v3c+v3b:
    print(f"{p['name']:<20} 实际{outcome(p)} {mark(r['final'],outcome(p))} {r['final']:<7} 关系分{r['rel']:<5} 综合{r['overall']:<5} 护城河{r['moats']}{' 剔除'+str(r['excluded']) if r['excluded'] else ''}")
