"""打分环节原型：读拆解卡 JSON，按 scoring.md 的规则计算。仅用于验证规则。"""
import json, re, sys

POTENTIAL = {"generate":1,"retrieve":1,"community_info":2,"transact_front":2,
             "tool":3,"record":3,"transact_own":4,"community_social":4}
TYPE_LABEL = {"generate":"生成/建议型","retrieve":"检索/聚合型","community_info":"信息型社区",
              "transact_front":"交易前端","tool":"工具/编辑器型","record":"记录/管理型",
              "transact_own":"成交方","community_social":"关系/身份型社区"}

FE = ["input","frequency","precision","intent","consumption","scenario","device","experience"]
FE_LABEL = dict(zip(FE,["输入成本比","频次与反馈速度","精确控制","目的型还是闲逛型",
                        "一次性读还是持续看","场景与设备","设备能力","体验是目的还是手段"]))
SCORES = {
 "input":{"A":0,"B":1,"C":1,"D":3,"E":4,"F":5},
 "frequency":{"A":0,"B":1,"C":2,"D":4,"E":5},
 "precision":{"A":0,"B":1,"C":3,"D":4,"E":5},
 "intent":{"A":0,"B":1,"C":3,"D":4},
 "consumption":{"A":0,"B":1,"C":3,"D":4,"E":5},
 "scenario":{"A":0,"B":1,"C":3,"D":4,"E":4},
 "device":{"A":0,"B":2,"C":4,"D":5},
 "experience":{"A":0,"B":1,"C":3,"D":4,"E":5},
}
STEP_LEVEL = {"input","precision","consumption","device"}
#          input freq prec intent cons scen dev exp
FE_W = {
 "generate":        [3,2,2,1,2,1,1,3],
 "retrieve":        [2,2,1,3,3,2,1,1],
 "community_info":  [1,2,1,3,2,1,1,2],
 "community_social":[1,3,1,3,2,1,2,3],
 "tool":            [3,2,3,1,1,1,1,2],
 "record":          [2,3,2,1,3,2,2,1],
 "transact_front":  [2,2,1,3,2,2,1,1],
 "transact_own":    [2,2,2,2,3,3,2,1],
}
BIZ = ["data","state","action","network","workflow","trust"]
BIZ_LABEL = dict(zip(BIZ,["独有数据","状态积累","执行闭环","网络与协作","工作流嵌入与分发","信任与责任"]))
#          data state action network workflow trust
BIZ_W = {
 "generate":        [3,3,3,1,2,2],
 "retrieve":        [3,1,2,1,3,2],
 "community_info":  [3,1,1,3,1,2],
 "community_social":[2,2,1,3,1,2],
 "tool":            [1,3,1,2,3,1],
 "record":          [2,3,1,1,3,2],
 "transact_front":  [2,1,3,2,2,2],
 "transact_own":    [2,1,3,3,1,3],
}
SECONDARY = 0.3
MOAT = 4.0
LEVELS = ["高风险","有一条护城河","较难替代"]

def blend(table, p, s):
    if not s: return list(map(float, table[p]))
    return [(1-SECONDARY)*a + SECONDARY*b for a,b in zip(table[p], table[s])]

def sub_score(aspect, item):
    c = item["class"]; sc = SCORES[aspect][c]
    if aspect=="frequency" and c in "DE" and item.get("automatable")=="automatable":
        sc = {"D":2,"E":4}[c]
    if aspect=="precision" and c=="E" and item.get("recurring") is False:
        sc = 1
    if aspect=="intent" and c in "CD" and item.get("content_source")=="ai_or_scraped":
        sc = {"C":1,"D":3}[c]
    if aspect=="device" and c in "BCD" and item.get("platform_generic") is True:
        sc = {"B":0,"C":2,"D":4}[c]
    if aspect=="experience" and item.get("chat_reproducible") is True:
        sc = min(sc,1)
    return sc

def score(card):
    p, s = card["primary_type"], card.get("secondary_type")
    fe = {a:0.0 for a in FE}
    for m in card["modes"]:
        for a in FE:
            if a in STEP_LEVEL:
                fe[a] += m["share"]*sum(st["share"]*sub_score(a, st[a]) for st in m["steps"])
            else:
                fe[a] += m["share"]*sub_score(a, m[a])
    fe = {a:round(v,2) for a,v in fe.items()}
    biz = {d:int(card["business"][d]["level"][1]) for d in BIZ}

    fw, bw = blend(FE_W,p,s), blend(BIZ_W,p,s)
    fe_score = sum(w*fe[a] for w,a in zip(fw,FE))/(5*sum(fw))*100
    gates = card.get("quality_gates",{})
    if any(v=="fail" for v in gates.values()): fe_score *= 0.8
    biz_score = sum(w*biz[d] for w,d in zip(bw,BIZ))/(5*sum(bw))*100
    potential = POTENTIAL[p] if not s else (1-SECONDARY)*POTENTIAL[p]+SECONDARY*POTENTIAL[s]

    items = {**{FE_LABEL[a]:fe[a] for a in FE}, **{BIZ_LABEL[d]:biz[d] for d in BIZ}}
    weights = {**{FE_LABEL[a]:w for a,w in zip(FE,fw)}, **{BIZ_LABEL[d]:w for d,w in zip(BIZ,bw)}}
    moats = [k for k,v in items.items() if v >= MOAT]
    base = 0 if not moats else (1 if len(moats)==1 else 2)
    relation = "替代" if card["ai_relation"]["class"] in "AB" else "互补"
    final = max(0, base-1) if relation=="替代" else base
    high_pot = potential >= 3
    diag = {(True,True):"结构和兑现一致",(True,False):"方向对，护城河还没建起来",
            (False,True):"方向危险，靠单项硬实力撑着",(False,False):"方向本身容易被替代"}[(high_pot, bool(moats))]
    overall = potential/5*100*0.2 + biz_score*0.4 + fe_score*0.4
    near = sorted(((weights[k]/max(MOAT-v,0.1),k,v) for k,v in items.items() if v<MOAT), reverse=True)[:3]
    return dict(potential=round(potential,1), biz=round(biz_score,1), fe=round(fe_score,1),
                overall=round(overall,1), fe_items=fe, biz_items=biz, moats=moats,
                relation=relation, base=LEVELS[base], final=LEVELS[final], diag=diag,
                nearest=[(k,v,round(r,2)) for r,k,v in near])

if __name__=="__main__":
    for path in sys.argv[1:]:
        txt=open(path,encoding="utf-8").read()
        m=re.search(r"```json\n(.*?)```",txt,re.S)
        card=json.loads(m.group(1) if m else txt)
        r=score(card)
        print(f"\n== {card['project']['one_liner']} ==")
        for k,v in r.items(): print(f"{k}: {v}")
