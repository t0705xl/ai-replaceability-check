"""盲测样本：14 个新产品。拆解卡在查任何结果数据之前写定。
按产品结构拆解，规则同 decompose-prompt.md（v2：含 practice 类型和 F 关系）。"""
from products import M, S, B

BLIND = [
 # 线下履约
 dict(name="Uber（打车）", primary="transact_own", secondary=None, business=B(5,2,4,5,2,4), relation="D", habit="B",
      modes=[M("叫车出行",1.0,"C","A","D","A",[S(.2,"A","B","A","A"),S(.1,"C","B","A","A"),
              S(.6,"A","A","D","C"),S(.1,"C","E","A","A",recurring=True)])]),
 dict(name="美团外卖", primary="transact_own", secondary=None, business=B(5,2,5,5,3,3), relation="D", habit="B",
      modes=[M("点外卖",1.0,"D","C","A","B",[S(.5,"D","A","A","A"),S(.2,"C","E","A","A",recurring=True),
              S(.3,"A","A","D","B")],auto="must_do_yourself")]),
 # 游戏 / 娱乐
 dict(name="Roblox", primary="community_social", secondary=None, business=B(4,3,3,5,1,2), relation="F", habit="B",
      modes=[M("玩游戏",.8,"E","D","A","E",[S(1,"F","D","E","A")],auto="must_do_yourself"),
             M("逛游戏和换装",.2,"D","D","B","D",[S(1,"D","A","C","B")],auto="must_do_yourself")]),
 dict(name="Spotify", primary="retrieve", secondary="record", business=B(5,4,4,3,3,1), relation="D", habit="B",
      modes=[M("听歌",1.0,"D","D","C","E",[S(.7,"C","A","D","B"),S(.3,"D","A","B","A")],auto="must_do_yourself")]),
 # 硬件
 dict(name="Oura 智能戒指", primary="record", secondary="practice", business=B(4,4,5,1,2,3), relation="E", habit="B",
      modes=[M("每天看身体数据",1.0,"D","A","B","C",[S(.6,"A","A","D","D"),S(.4,"A","A","B","D")],auto="must_do_yourself")]),
 dict(name="有道词典笔", primary="retrieve", secondary="generate", business=B(2,1,5,0,1,2), relation="A", habit="C",
      modes=[M("读书时扫词",1.0,"D","A","E","A",[S(.6,"A","A","A","D"),S(.4,"A","A","A","D")],auto="must_do_yourself")]),
 # 国内社区
 dict(name="知乎", primary="community_info", secondary=None, business=B(2,2,0,4,1,1), relation="A", habit="B",
      modes=[M("搜索看回答",.6,"C","A","B","A",[S(1,"A","A","A","A")]),
             M("刷推荐流",.4,"D","D","B","D",[S(1,"D","A","C","B")],auto="must_do_yourself")]),
 dict(name="小红书", primary="community_social", secondary="community_info", business=B(5,3,2,5,1,2), relation="F", habit="B",
      modes=[M("刷推荐",.6,"D","D","B","D",[S(.8,"D","A","C","B"),S(.2,"A","A","C","A")],auto="must_do_yourself"),
             M("搜索攻略",.4,"C","B","B","A",[S(1,"D","A","A","A")])]),
 # 交易标的本身可能被 AI 替代的平台
 dict(name="Fiverr（自由职业外包）", primary="transact_own", secondary="retrieve", business=B(3,2,4,4,1,3), relation="A", habit="B",
      modes=[M("找人做事",1.0,"A","B","A","A",[S(.4,"D","A","A","A"),S(.3,"B","C","C","A"),S(.3,"C","C","C","A")])]),
 dict(name="Shutterstock（图库）", primary="retrieve", secondary="transact_own", business=B(3,1,3,4,2,4), relation="A", habit="A",
      modes=[M("找图",1.0,"B","B","A","A",[S(.7,"D","A","A","A"),S(.3,"C","E","A","A",recurring=True)])]),
 dict(name="Yelp（本地点评）", primary="community_info", secondary=None, business=B(4,1,1,4,1,2), relation="C", habit="B",
      modes=[M("找本地商家",1.0,"C","B","B","A",[S(.5,"C","A","A","A"),S(.5,"D","A","A","A")])]),
 # 学习 / 工具
 dict(name="Udemy（视频课程）", primary="practice", secondary="transact_own", business=B(2,2,3,4,2,2), relation="A", habit="A",
      modes=[M("学课程",1.0,"B","A","A","C",[S(.7,"A","A","A","A"),S(.3,"C","A","B","A")],chat=True)]),
 dict(name="Keep（健身跟练）", primary="practice", secondary="retrieve", business=B(3,3,2,2,1,1), relation="F", habit="B",
      modes=[M("跟练课程",.7,"B","A","C","C",[S(.2,"C","A","A","A"),S(.8,"A","A","D","A")]),
             M("跑步记录",.3,"B","A","C","C",[S(1,"A","A","D","C")])]),
 dict(name="Wix（建站）", primary="tool", secondary=None, business=B(2,4,3,1,3,2), relation="B", habit="B",
      modes=[M("建站与修改",.4,"A","B","A","B",[S(.3,"D","A","A","A"),S(.7,"F","D","A","A")]),
             M("日常运营",.6,"C","A","B","A",[S(1,"A","B","C","B")])]),
]

def card(p):
    return {"project":{"one_liner":p["name"]},"primary_type":p["primary"],"secondary_type":p["secondary"],
            "business":p["business"],"modes":p["modes"],"ai_relation":{"class":p["relation"]},"quality_gates":{}}
