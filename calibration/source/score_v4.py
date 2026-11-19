"""打分规则 v4 = v3 + 搜索获客双重暴露：
主要靠搜索引擎带来"找答案"流量（search_acquisition=True），且关系分 < 35 时，再降一级。"""
import score_v3 as v3
LEVELS=v3.LEVELS
def score(card):
    r=v3.score(card)
    if card.get("search_acquisition") and r["rel"]<v3.SUBST and r["final"]!="高风险":
        r=dict(r); r["final"]=LEVELS[LEVELS.index(r["final"])-1]; r["seo_downgrade"]=True
    return r
