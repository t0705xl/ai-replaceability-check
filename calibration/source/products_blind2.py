"""第三轮盲测：13 个产品，重点是信息+社区混合型和数据方（C）型。按 v3 拆解规则写定，查结果前锁定。"""
from products import M, S, B
def R(mode, rel): mode["relation"]=rel; return mode

BLIND2 = [
 # ---- 信息 + 社区混合型 ----
 dict(name="B站（哔哩哔哩）", primary="community_social", secondary="community_info", business=B(5,3,2,5,1,1), acq="应用直接打开", habit="B",
      modes=[R(M("刷推荐看视频",.7,"D","D","B","E",[S(.3,"D","A","C","A"),S(.7,"A","A","A","A")],auto="must_do_yourself"),"F"),
             R(M("搜索学习类视频",.3,"C","A","A","B",[S(1,"A","A","A","A")]),"A")]),
 dict(name="LinkedIn", primary="community_social", secondary="retrieve", business=B(5,5,2,5,4,3), acq="人脉邀请、应用直接打开", habit="A",
      modes=[R(M("刷职场动态",.4,"C","D","B","B",[S(1,"D","A","C","B")]),"F"),
             R(M("找工作投递",.35,"A","B","A","A",[S(.5,"B","A","A","A"),S(.5,"C","B","C","B")]),"D"),
             R(M("维护档案和人脉",.25,"A","A","A","B",[S(1,"B","B","B","A")]),"E")]),
 dict(name="Nextdoor（邻里社区）", primary="community_social", secondary="community_info", business=B(3,2,1,4,1,2), acq="邮件通知、邻居邀请", habit="C",
      modes=[R(M("刷本地动态",.6,"C","C","B","B",[S(1,"C","A","C","B")]),"F"),
             R(M("问邻居求推荐",.4,"A","A","A","A",[S(1,"A","A","C","B")]),"A")]),
 dict(name="Substack（付费订阅写作）", primary="community_social", secondary=None, business=B(3,2,3,4,2,2), acq="社交分享、邮件", habit="A",
      modes=[R(M("读订阅文章",.7,"C","B","B","B",[S(1,"A","A","A","A")]),"F"),
             R(M("刷 Notes 发现作者",.3,"C","D","B","B",[S(1,"C","A","C","B")]),"F")]),
 dict(name="Discord", primary="community_social", secondary=None, business=B(3,4,1,5,3,1), acq="好友邀请", habit="A",
      modes=[R(M("群聊和语音",.8,"E","A","A","D",[S(1,"A","A","C","B")],auto="must_do_yourself"),"F"),
             R(M("逛服务器频道",.2,"D","C","A","D",[S(1,"C","A","C","B")],auto="must_do_yourself"),"F")]),
 dict(name="Quora", primary="community_info", secondary=None, business=B(2,1,0,4,0,1), acq="搜索引擎", habit="B",
      modes=[R(M("从搜索来看回答",.8,"C","A","B","A",[S(1,"A","A","A","A")]),"A"),
             R(M("刷动态",.2,"C","D","B","B",[S(1,"C","A","C","B")]),"F")]),
 dict(name="什么值得买", primary="community_info", secondary="retrieve", business=B(3,1,1,4,1,2), acq="应用直接打开、搜索引擎", habit="B",
      modes=[R(M("刷好价",.6,"D","D","B","B",[S(1,"D","A","C","B")],auto="automatable"),"A"),
             R(M("搜索看评测",.4,"A","B","A","A",[S(1,"A","A","A","A")]),"A")]),
 # ---- 数据方（C）型 ----
 dict(name="Wikipedia（阅读端）", primary="community_info", secondary=None, business=B(4,1,0,4,1,3), acq="搜索引擎", habit="B",
      modes=[R(M("查资料阅读",.9,"C","A","A","A",[S(1,"A","A","A","A")]),"C"),
             R(M("编辑条目",.1,"B","A","A","C",[S(1,"B","C","C","A")]),"F")]),
 dict(name="Tripadvisor（点评主站）", primary="community_info", secondary="retrieve", business=B(4,1,1,4,1,2), acq="搜索引擎", habit="B",
      modes=[R(M("查评价做决定",.7,"A","B","A","A",[S(.5,"C","A","A","A"),S(.5,"D","A","A","A")]),"C"),
             R(M("比价跳转预订",.3,"A","B","A","A",[S(1,"C","B","A","A")]),"A")]),
 dict(name="Glassdoor（公司点评）", primary="community_info", secondary=None, business=B(4,1,0,3,1,2), acq="搜索引擎", habit="A",
      modes=[R(M("查公司评价和薪资",1.0,"A","A","A","A",[S(1,"A","A","A","A")]),"C")]),
 dict(name="NerdWallet（金融产品比较）", primary="retrieve", secondary=None, business=B(3,2,1,2,1,3), acq="搜索引擎", habit="B",
      modes=[R(M("搜索比较金融产品",.8,"A","B","A","A",[S(1,"C","B","A","A")]),"C"),
             R(M("App 看信用分",.2,"C","A","B","A",[S(1,"A","A","C","B")]),"B")]),
 dict(name="Zillow（房源）", primary="retrieve", secondary="transact_front", business=B(4,2,2,4,2,2), acq="应用直接打开、搜索引擎", habit="B",
      modes=[R(M("刷房源",.7,"C","C","B","B",[S(1,"D","A","C","B")]),"C"),
             R(M("联系经纪人约看房",.3,"A","A","A","A",[S(1,"B","B","C","B")]),"D")]),
 # ---- 交易标的检查 ----
 dict(name="Etsy（手工品市场）", primary="transact_own", secondary="retrieve", business=B(4,2,4,4,1,3), acq="搜索引擎、购物广告、直接打开", habit="B",
      deliverable=False,
      modes=[R(M("逛和搜索商品",.7,"A","C","B","B",[S(1,"D","A","A","A")]),"C"),
             R(M("下单购买",.3,"A","A","A","A",[S(1,"B","E","C","B",recurring=True)]),"D")]),
]
def card(p):
    return {"project":{"one_liner":p["name"],"acquisition":p["acq"]},"primary_type":p["primary"],"secondary_type":p["secondary"],
            "business":p["business"],"modes":p["modes"],"deliverable_ai_replaceable":p.get("deliverable",False),"quality_gates":{}}
