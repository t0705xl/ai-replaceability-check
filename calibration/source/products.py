"""14 个真实产品的拆解卡（按 AI 客户端普及时的核心产品拆）。outcome: 1 崩塌 2 受压 3 稳健 4 受益"""
def M(name, share, freq, intent, scen, exp, steps, auto=None, src="human_or_real", chat=False):
    f = {"class": freq}
    if auto: f["automatable"] = auto
    i = {"class": intent, "content_source": src}
    return {"name": name, "share": share, "frequency": f, "intent": i,
            "scenario": {"class": scen}, "experience": {"class": exp, "chat_reproducible": chat},
            "steps": steps}
def S(share, inp, prec, cons, dev, recurring=None, generic=False):
    p = {"class": prec}
    if recurring is not None: p["recurring"] = recurring
    return {"share": share, "input": {"class": inp}, "precision": p,
            "consumption": {"class": cons}, "device": {"class": dev, "platform_generic": generic}}
def B(data, state, action, network, workflow, trust):
    return {k: {"level": f"L{v}"} for k, v in zip(
        ["data","state","action","network","workflow","trust"], [data,state,action,network,workflow,trust])}

PRODUCTS = [
 # ---------- 1 崩塌 ----------
 dict(name="Chegg（作业答案）", outcome=1, primary="retrieve", secondary=None,
      business=B(2,1,0,0,1,1), relation="A", relation_v2="A",
      modes=[M("做作业时查题",1.0,"B","A","A","A",[S(.3,"A","A","A","A"),S(.7,"A","B","A","A")])]),
 dict(name="Stack Overflow", outcome=1, primary="community_info", secondary=None,
      business=B(2,2,0,4,1,1), relation="A", relation_v2="A",
      modes=[M("搜索答案",.8,"D","A","A","A",[S(1,"A","B","A","A")],auto="automatable"),
             M("提问与回答",.2,"B","A","A","B",[S(1,"A","B","C","A")])]),
 dict(name="Tome（AI 生成幻灯片）", outcome=1, primary="generate", secondary="tool",
      business=B(0,1,0,1,0,0), relation="A", relation_v2="A",
      modes=[M("做演示",1.0,"A","A","A","A",[S(.4,"A","A","A","A"),S(.4,"C","C","A","A"),S(.2,"A","A","B","A")])]),
 dict(name="Jasper（早期 AI 文案）", outcome=1, primary="generate", secondary=None,
      business=B(0,1,0,1,1,1), relation="A", relation_v2="A",
      modes=[M("写营销文案",1.0,"B","A","A","A",[S(.3,"B","A","A","A"),S(.4,"C","A","A","A"),S(.3,"B","B","A","A")])]),
 # ---------- 2 受压 ----------
 dict(name="Quizlet（学习卡片）", outcome=2, primary="record", secondary="retrieve", primary_v2="practice",
      business=B(2,3,0,2,2,0), relation="A", relation_v2="F",
      modes=[M("查现成学习集",.4,"C","A","A","A",[S(1,"A","A","A","A")]),
             M("背卡片练习",.6,"E","A","B","C",[S(1,"C","A","A","A")],auto="must_do_yourself")]),
 dict(name="Grammarly", outcome=2, primary="generate", secondary=None,
      business=B(2,2,2,1,3,1), relation="B", relation_v2="B",
      modes=[M("写作时实时检查",1.0,"D","A","A","A",[S(.6,"A","C","D","A"),S(.4,"C","C","A","A")],auto="automatable")]),
 # ---------- 3 稳健 ----------
 dict(name="Duolingo", outcome=3, primary="record", secondary=None, primary_v2="practice",
      business=B(4,4,0,2,0,1), relation="A", relation_v2="F",
      modes=[M("每日练习",1.0,"E","A","B","C",[S(.8,"C","A","A","A"),S(.2,"A","A","C","B")],auto="must_do_yourself")]),
 dict(name="Pinterest", outcome=3, primary="retrieve", secondary="record",
      business=B(5,3,1,2,0,0), relation="B", relation_v2="F",
      modes=[M("刷灵感",.6,"C","D","B","D",[S(.7,"D","A","A","A"),S(.3,"C","A","B","A")]),
             M("带目的搜索",.4,"C","B","A","B",[S(1,"D","A","A","A")])]),
 dict(name="Booking.com", outcome=3, primary="transact_own", secondary="retrieve",
      business=B(4,3,4,4,2,4), relation="D", relation_v2="D",
      modes=[M("搜索与预订",.6,"A","B","A","A",[S(.4,"B","B","A","A"),S(.4,"D","A","A","A"),S(.2,"B","E","C","A",recurring=True)]),
             M("行程中",.4,"C","A","C","A",[S(.7,"A","A","C","B"),S(.3,"B","E","C","A",recurring=True)])]),
 dict(name="Strava", outcome=3, primary="record", secondary="community_social",
      business=B(5,5,0,5,4,1), relation="E", relation_v2="E",
      modes=[M("运动记录",.5,"D","A","E","C",[S(.6,"A","A","D","C"),S(.4,"A","A","B","A")],auto="must_do_yourself"),
             M("社交动态",.5,"D","D","B","D",[S(.7,"C","A","C","B"),S(.3,"A","A","C","A")],auto="must_do_yourself")]),
 dict(name="Reddit", outcome=3, primary="community_social", secondary="community_info",
      business=B(5,3,0,5,1,2), relation="C", relation_v2="C",
      modes=[M("刷社区",.6,"D","D","B","D",[S(.7,"D","A","C","B"),S(.3,"A","A","C","A")],auto="must_do_yourself"),
             M("从搜索来找答案",.4,"C","A","A","A",[S(1,"A","A","A","A")])]),
 # ---------- 4 受益 ----------
 dict(name="Figma", outcome=4, primary="tool", secondary=None,
      business=B(2,5,0,3,4,1), relation="D", relation_v2="D",
      modes=[M("设计",.8,"E","A","A","B",[S(.6,"F","D","A","A"),S(.4,"E","D","A","A")],auto="must_do_yourself"),
             M("评审与交付",.2,"D","A","A","A",[S(1,"C","C","C","A")],auto="must_do_yourself")]),
 dict(name="Canva", outcome=4, primary="tool", secondary="retrieve",
      business=B(3,3,2,2,3,1), relation="D", relation_v2="D",
      modes=[M("做设计",1.0,"B","B","A","B",[S(.3,"D","A","A","A"),S(.5,"F","C","A","A"),S(.2,"A","B","A","A")])]),
 dict(name="Notion", outcome=4, primary="record", secondary="tool",
      business=B(3,5,2,3,4,2), relation="E", relation_v2="E",
      modes=[M("日常记录",.6,"D","A","A","B",[S(.5,"B","C","B","A"),S(.5,"C","B","C","A")],auto="must_do_yourself"),
             M("团队查阅",.4,"C","A","A","A",[S(1,"A","A","C","A")])]),
]

def card(p, version="v1"):
    prim = p.get("primary_v2", p["primary"]) if version=="v2" else p["primary"]
    rel = p["relation_v2"] if version=="v2" else p["relation"]
    return {"project":{"one_liner":p["name"]}, "primary_type":prim, "secondary_type":p["secondary"],
            "business":p["business"], "modes":p["modes"], "ai_relation":{"class":rel},
            "quality_gates":{}}
