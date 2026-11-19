from products import PRODUCTS, card
from score_prototype import score
LBL={1:"崩塌",2:"受压",3:"稳健",4:"受益"}
rows=[]
for p in PRODUCTS:
    r=score(card(p,"v1")); rows.append((p,r))
    print(f"{p['name']:<22}{LBL[p['outcome']]}  等级={r['final']:<8} 潜力={r['potential']:<4} 业务={r['biz']:<5} 前端={r['fe']:<5} 综合={r['overall']:<5} 护城河项={r['moats']}")
# 排序一致性（Spearman）
def rank(xs):
    s=sorted(range(len(xs)),key=lambda i:xs[i]); r=[0]*len(xs); i=0
    while i<len(s):
        j=i
        while j+1<len(s) and xs[s[j+1]]==xs[s[i]]: j+=1
        for k in range(i,j+1): r[s[k]]=(i+j)/2+1
        i=j+1
    return r
def spearman(a,b):
    ra,rb=rank(a),rank(b); n=len(a); ma=sum(ra)/n; mb=sum(rb)/n
    cov=sum((x-ma)*(y-mb) for x,y in zip(ra,rb)); va=sum((x-ma)**2 for x in ra)**.5; vb=sum((y-mb)**2 for y in rb)**.5
    return cov/(va*vb)
out=[p["outcome"] for p,_ in rows]
print("\nSpearman(综合分, 实际结果) =", round(spearman([r["overall"] for _,r in rows],out),3))
lv={"高风险":0,"有一条护城河":1,"较难替代":2}
ok=sum(1 for p,r in rows if (p["outcome"]<=2)==(r["final"]=="高风险"))
print(f"等级与结果方向一致：{ok}/{len(rows)}（崩塌/受压应为高风险，稳健/受益应不是高风险）")
