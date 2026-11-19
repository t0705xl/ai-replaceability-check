"""打分规则 v3：在 v2 基础上，根据盲测失准修订。
1. 与 AI 客户端的关系改为按使用模式判断，再按占比合成关系分
2. C（数据方）不再中性：关系分 25
3. 交易标的检查：用户买的东西 AI 能直接生成时，执行/网络/信任不计为护城河项
（硬件相关的澄清写在拆解规则里，体现在拆解卡上）"""
import score_v2 as v2
from score_prototype import FE, BIZ, FE_LABEL, BIZ_LABEL, sub_score, LEVELS, MOAT
REL_SCORE = {"A":0,"B":0,"C":25,"F":50,"D":100,"E":100}
SUBST, COMPL = 35, 75
TXN_DIMS = {"执行闭环","网络与协作","信任与责任"}

def relation_score(card):
    if any("relation" in m for m in card["modes"]):
        return sum(m["share"]*REL_SCORE[m["relation"]] for m in card["modes"])
    return REL_SCORE[card["ai_relation"]["class"]]

def score(card, mix=(0.15,0.35,0.35,0.15)):
    p,s=card["primary_type"],card.get("secondary_type")
    fe={a:0.0 for a in FE}
    for m in card["modes"]:
        for a in FE:
            if a in v2.v1.STEP_LEVEL: fe[a]+=m["share"]*sum(st["share"]*sub_score(a,st[a]) for st in m["steps"])
            else: fe[a]+=m["share"]*sub_score(a,m[a])
    fe={a:round(v,2) for a,v in fe.items()}
    biz={d:int(card["business"][d]["level"][1]) for d in BIZ}
    fw=v2.blend(v2.FE_W,p,s,FE,True); bw=v2.blend(v2.BIZ_W,p,s,BIZ,True)
    fe_score=sum(w*fe[a] for w,a in zip(fw,FE))/(5*sum(fw))*100
    biz_score=sum(w*biz[d] for w,d in zip(bw,BIZ))/(5*sum(bw))*100
    potential=v2.POTENTIAL[p] if not s else 0.7*v2.POTENTIAL[p]+0.3*v2.POTENTIAL[s]
    rel=relation_score(card)
    items={**{FE_LABEL[a]:fe[a] for a in FE},**{BIZ_LABEL[d]:biz[d] for d in BIZ}}
    moats=[k for k,v in items.items() if v>=MOAT]
    excluded=[]
    if card.get("deliverable_ai_replaceable"):
        excluded=[k for k in moats if k in TXN_DIMS]; moats=[k for k in moats if k not in TXN_DIMS]
    n=len(moats)+(1 if rel>=COMPL else 0)
    base=0 if n==0 else (1 if n==1 else 2)
    final=max(0,base-1) if rel<SUBST else base
    a,b,c,d=mix
    overall=a*potential/5*100+b*biz_score+c*fe_score+d*rel
    return dict(potential=round(potential,1),biz=round(biz_score,1),fe=round(fe_score,1),overall=round(overall,1),
                rel=round(rel,1),moats=moats+(["与 AI 客户端互补"] if rel>=COMPL else []),excluded=excluded,
                final=LEVELS[final],fe_items=fe,biz_items=biz)
