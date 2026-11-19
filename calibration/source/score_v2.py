"""打分规则 v2：在原型基础上加入校准结论。opts 控制各项改动，便于对比。"""
import score_prototype as v1
from score_prototype import FE, BIZ, FE_LABEL, BIZ_LABEL, sub_score, LEVELS, MOAT

POTENTIAL = dict(v1.POTENTIAL, practice=3)
TYPE_LABEL = dict(v1.TYPE_LABEL, practice="练习/养成型")
#                    input freq prec intent cons scen dev exp
FE_W = dict(v1.FE_W, practice=[1,3,1,1,2,2,2,3])
#                    data state action network workflow trust
BIZ_W = dict(v1.BIZ_W, practice=[2,3,1,2,1,1])
# 校准系数：按各项与实际结果的相关强度分档
CAL = {"state":1.5, "input":1.25, "data":1.25, "workflow":1.25,
       "experience":1.0, "network":1.0, "frequency":1.0, "action":1.0, "intent":1.0,
       "trust":0.85, "consumption":0.85, "precision":0.6,
       "scenario":1.0, "device":1.0}   # 场景、设备：样本不足，暂不调整
REL_SCORE = {"A":0,"B":0,"C":50,"F":50,"D":100,"E":100}

def blend(table,p,s,keys,cal):
    base = table[p] if not s else [(0.7)*a+0.3*b for a,b in zip(table[p],table[s])]
    return [w*(CAL[k] if cal else 1) for w,k in zip(base,keys)]

def score(card, uniform=False, cal=True, rel_moat=True, mix=(0.15,0.35,0.35,0.15)):
    p,s = card["primary_type"], card.get("secondary_type")
    fe={a:0.0 for a in FE}
    for m in card["modes"]:
        for a in FE:
            if a in v1.STEP_LEVEL: fe[a]+=m["share"]*sum(st["share"]*sub_score(a,st[a]) for st in m["steps"])
            else: fe[a]+=m["share"]*sub_score(a,m[a])
    fe={a:round(v,2) for a,v in fe.items()}
    biz={d:int(card["business"][d]["level"][1]) for d in BIZ}
    if uniform: fw=[1.0]*8; bw=[1.0]*6
    else: fw=blend(FE_W,p,s,FE,cal); bw=blend(BIZ_W,p,s,BIZ,cal)
    fe_score=sum(w*fe[a] for w,a in zip(fw,FE))/(5*sum(fw))*100
    biz_score=sum(w*biz[d] for w,d in zip(bw,BIZ))/(5*sum(bw))*100
    potential=POTENTIAL[p] if not s else 0.7*POTENTIAL[p]+0.3*POTENTIAL[s]
    rel=card["ai_relation"]["class"]
    items={**{FE_LABEL[a]:fe[a] for a in FE},**{BIZ_LABEL[d]:biz[d] for d in BIZ}}
    moats=[k for k,v in items.items() if v>=MOAT]
    n=len(moats)+(1 if rel_moat and rel in "DE" else 0)
    base=0 if n==0 else (1 if n==1 else 2)
    final=max(0,base-1) if rel in "AB" else base
    a,b,c,d=mix
    overall=a*potential/5*100+b*biz_score+c*fe_score+d*REL_SCORE[rel]
    weights={**{FE_LABEL[k]:w for k,w in zip(FE,fw)},**{BIZ_LABEL[k]:w for k,w in zip(BIZ,bw)}}
    near=sorted(((weights[k]/max(MOAT-v,0.1),k,v) for k,v in items.items() if v<MOAT),reverse=True)[:3]
    return dict(potential=round(potential,1),biz=round(biz_score,1),fe=round(fe_score,1),overall=round(overall,1),
                moats=moats+(["与 AI 客户端互补（D/E）"] if rel_moat and rel in "DE" else []),
                final=LEVELS[final],relation=rel,fe_items=fe,biz_items=biz,nearest=[(k,v) for _,k,v in near])
