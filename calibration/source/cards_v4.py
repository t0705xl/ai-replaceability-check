"""v4 拆解卡：在 v3 卡上统一补充获客渠道，并按两条新拆解规则修正：
(1) 判 A 之前先问 AI 拿不拿得到答案所需的信息——只存在于产品内的实时、本地、私密信息，不判 A；
(2) 比较/导购类产品里，在产品内完成的预审、匹配或持牌代办环节要单独拆成一个模式。"""
import copy
from cards_v3 import CALIB, BLINDC
from products_blind2 import BLIND2, card as card3
from products import M, S, B
SEARCH = {"Chegg（作业答案）","Stack Overflow","Quizlet（学习卡片）","Pinterest","Reddit","Canva",
          "知乎","Fiverr（自由职业外包）","Shutterstock（图库）","Yelp（本地点评）","Udemy（视频课程）",
          "Quora","什么值得买","Wikipedia（阅读端）","Tripadvisor（点评主站）","Glassdoor（公司点评）","NerdWallet（金融产品比较）","Zillow（房源）","Etsy（手工品市场）"}
def tag(p,c):
    c=copy.deepcopy(c); c["search_acquisition"]= p["name"] in SEARCH; return c
ROUND1=[(p,tag(p,c)) for p,c in CALIB]
ROUND2=[(p,tag(p,c)) for p,c in BLINDC]
def r3(p, corrected):
    c=card3(p)
    if corrected and p["name"]=="Nextdoor（邻里社区）":      # 规则 (1)：邻里实时信息只在产品内
        c["modes"][1]["relation"]="F"
    if corrected and p["name"]=="NerdWallet（金融产品比较）":  # 规则 (2)：拆出预审匹配与持牌代办
        c["business"]=B(3,2,2,2,1,4)
        rel=lambda m,x: (m.__setitem__("relation",x), m)[1]
        c["modes"]=[rel(M("读比较文章",.5,"A","B","A","A",[S(1,"C","B","A","A")]),"C"),
                    rel(M("预审匹配与持牌代办",.3,"A","A","A","A",[S(1,"B","E","C","B",recurring=True)]),"D"),
                    rel(M("App 看信用分",.2,"C","A","B","A",[S(1,"A","A","C","B")]),"B")]
    return tag(p,c)
ROUND3_STRICT=[(p,r3(p,False)) for p in BLIND2]
ROUND3=[(p,r3(p,True)) for p in BLIND2]
