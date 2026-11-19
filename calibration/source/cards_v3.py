"""v3 拆解卡：在原卡上补充按模式的关系、交易标的标记，并按澄清后的硬件规则修正。"""
import copy
from products import PRODUCTS, card as card1
from products_blind import BLIND, card as cardb
B = lambda d,s,a,n,w,t: {k:{"level":f"L{v}"} for k,v in zip(["data","state","action","network","workflow","trust"],[d,s,a,n,w,t])}
MODE_REL = {   # 每个使用模式与 AI 客户端的关系，顺序同拆解卡里的 modes
 "Chegg（作业答案）":["A"], "Stack Overflow":["A","A"], "Tome（AI 生成幻灯片）":["A"], "Jasper（早期 AI 文案）":["A"],
 "Quizlet（学习卡片）":["A","F"], "Grammarly":["B"], "Duolingo":["F"], "Pinterest":["F","F"],
 "Booking.com":["D","D"], "Strava":["E","F"], "Reddit":["F","C"], "Figma":["D","E"], "Canva":["D"], "Notion":["E","E"],
 "Uber（打车）":["D"], "美团外卖":["D"], "Roblox":["F","F"], "Spotify":["D"], "Oura 智能戒指":["E"], "有道词典笔":["A"],
 "知乎":["A","F"], "小红书":["F","A"], "Fiverr（自由职业外包）":["A"], "Shutterstock（图库）":["A"], "Yelp（本地点评）":["C"],
 "Udemy（视频课程）":["A"], "Keep（健身跟练）":["F","F"], "Wix（建站）":["B","E"],
}
DELIVERABLE_REPLACEABLE = {"Fiverr（自由职业外包）","Shutterstock（图库）","Udemy（视频课程）"}
def build(p, base_card):
    c = copy.deepcopy(base_card)
    for m,r in zip(c["modes"], MODE_REL[p["name"]]): m["relation"]=r
    c["deliverable_ai_replaceable"] = p["name"] in DELIVERABLE_REPLACEABLE
    # 硬件澄清：卖硬件不算执行闭环；手机 + AI 能做到的硬件功能按 A；查询类动作算 automatable
    if p["name"]=="有道词典笔":
        c["business"]=B(2,1,0,0,1,2)
        for m in c["modes"]:
            m["frequency"]["automatable"]="automatable"
            for st in m["steps"]: st["device"]={"class":"A"}
    if p["name"]=="Oura 智能戒指":
        c["business"]=B(4,4,0,1,2,3)
    return c
CALIB = [(p, build(p, card1(p,"v2"))) for p in PRODUCTS]
BLINDC = [(p, build(p, cardb(p))) for p in BLIND]
