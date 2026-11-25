import os, sys, json
from PIL import Image, ImageDraw, ImageFont
FD=os.environ.get("FONTDIR","fonts"); OUT=os.environ.get("OUTDIR","out"); S=2; W,H=1080*S,1350*S
TD,TM,VI,LAV,BONE,MINT,WH="#021615","#033432","#6030F0","#CFC3FF","#EAF1EF","#8DF2D2","#FFFFFF"
WT={"J":("PJS",800),"JB":("PJS",700),"JM":("PJS",500),"AR":("Cairo",700)}
_c={}
def F(n,s,basic=False):
    k=(n,s,basic)
    if k in _c: return _c[k]
    fn,w=WT[n]; f=ImageFont.truetype(f"{FD}/{fn}.ttf",int(s*(1.05 if n=="AR" else 1)*S),layout_engine=(ImageFont.Layout.BASIC if basic else ImageFont.Layout.RAQM))
    vals=[w if "eight" in (a["name"].decode() if isinstance(a["name"],bytes) else a["name"]) else a["default"] for a in f.get_variation_axes()]
    f.set_variation_by_axes(vals); _c[k]=f; return f
class C:
    def __init__(s,bg): s.im=Image.new("RGB",(W,H),bg); s.d=ImageDraw.Draw(s.im)
    def rr(s,x0,y0,x1,y1,r,fill): s.d.rounded_rectangle([x0*S,y0*S,x1*S,y1*S],radius=r*S,fill=fill)
    def tx(s,x,y,t,f,fill,a="la",**k): s.d.text((x*S,y*S),t,font=f,fill=fill,anchor=a,**k)
    def ar(s,x,y,t,size,fill): s.tx(x,y,t,F("AR",size),fill,"rm",direction="rtl",language="ar")
    def circ(s,cx,cy,r,fill): s.d.ellipse([(cx-r)*S,(cy-r)*S,(cx+r)*S,(cy+r)*S],fill=fill)
    def poly(s,p,fill): s.d.polygon([(x*S,y*S) for x,y in p],fill=fill)
    def line(s,p,fill,w): s.d.line([(x*S,y*S) for x,y in p],fill=fill,width=int(w*S),joint="curve")
    def pill(s,right,cy,label,bg,fg,size=26):
        f=F("JB",size); w=f.getlength(label)/S+48; s.rr(right-w,cy-26,right,cy+26,26,bg); s.tx(right-w/2,cy+1,label,f,fg,"mm")
    def pillL(s,left,cy,label,bg,fg,size=26):
        f=F("JB",size); w=f.getlength(label)/S+48; s.rr(left,cy-26,left+w,cy+26,26,bg); s.tx(left+w/2,cy+1,label,f,fg,"mm")
    def hl(s,x,y,pre,word,post,size,fill,hbg,hfg,pad=20):
        f=F("J",size,True); pw=f.getlength(pre)/S; ww=f.getlength(word)/S
        s.tx(x,y,pre,f,fill); s.rr(x+pw-4,y+size*0.06,x+pw+ww+pad*2-4,y+size*1.12,28,hbg); s.tx(x+pw+pad-4,y,word,f,hfg); s.tx(x+pw+ww+pad*2,y,post,f,fill)
    def wrap(s,x,y,t,fp,size,fill,maxw,step):
        f=F(fp,size); line=""
        for w in t.split():
            q=(line+" "+w).strip()
            if f.getlength(q)/S>maxw: s.tx(x,y,line,f,fill); y+=step; line=w
            else: line=q
        if line: s.tx(x,y,line,f,fill)
    def save(s,n): s.im.resize((1080,1350),Image.LANCZOS).save(n,"JPEG",quality=92)
def phones(c,cx,cy,big,small,arrow):
    c.rr(cx-330,cy-62,cx-170,cy+62,16,big); c.poly([(cx-266,cy-26),(cx-266,cy+26),(cx-224,cy)],arrow)
    c.line([(cx-136,cy),(cx-80,cy)],arrow,8); c.line([(cx-98,cy-20),(cx-76,cy),(cx-98,cy+20)],arrow,8)
    for i in range(4):
        x=cx-40+i*92; sc=small[i%len(small)]; c.rr(x,cy-80,x+72,cy+80,16,sc); c.poly([(x+27,cy-14),(x+27,cy+14),(x+48,cy)],big if sc!=big else arrow)
def g_bars(c,cy):
    c.rr(120,cy-24,960,cy+24,24,"#0B2A28")
    for x0,x1,col in [(180,300,MINT),(470,620,LAV),(760,880,MINT)]: c.rr(x0,cy-24,x1,cy+24,24,col)
    for x in (240,545,820): c.circ(x,cy+62,6,WH)
def g_chart(c,cy):
    for i,h in enumerate([50,80,115,150,190]):
        x=240+i*130; c.rr(x,cy+95-h,x+90,cy+95,18,MINT if i==4 else (VI if i>=2 else LAV))
def g_tiles(c,cy):
    for i in range(7):
        x=120+i*122; c.rr(x,cy-70,x+100,cy+70,20,[MINT,LAV,WH,VI][i%4]); c.poly([(x+38,cy-18),(x+38,cy+18),(x+68,cy)],TD if i%4!=3 else WH)
def g_phones(c,cy): phones(c,540,cy,VI,[MINT,LAV,WH,MINT],WH)
def g_phones2(c,cy): phones(c,540,cy,VI,[MINT,LAV,WH,MINT],MINT)
def g_dots(c,cy):
    for i in range(5):
        x=200+i*170; c.circ(x,cy,52,[MINT,LAV,WH,VI,MINT][i]); c.poly([(x-14,cy-22),(x-14,cy+22),(x+24,cy)],TD if i!=3 else WH)
        if i<4: c.line([(x+64,cy),(x+106,cy)],"#0B2A28",8)
G={"bars":g_bars,"chart":g_chart,"tiles":g_tiles,"phones":g_phones,"phones2":g_phones2,"dots":g_dots}
def bar(c,n,tot,tile,fg,pbg,pfg,label="Swipe",y0=1176):
    c.rr(48,y0,1032,y0+126,44,tile); c.tx(96,y0+64,label,F("JB",40),fg,"lm")
    lw=F("JB",40).getlength(label)/S; ax=96+lw+48
    c.line([(ax-26,y0+64),(ax+24,y0+64)],fg,7); c.line([(ax+6,y0+46),(ax+24,y0+64),(ax+6,y0+82)],fg,7)
    c.pill(996,y0+64,f"{n} / {tot}",pbg,pfg,30)
def render(p,tag):
    os.makedirs(OUT,exist_ok=True); cv=p["cover"]
    c=C(VI); c.tx(64,72,"SADA",F("J",54),WH); c.pill(1016,98,"CLIPPING · UGC",TD,WH)
    y=190
    for ln in cv["head"]: c.tx(64,y,ln,F("J",120,True),WH); y+=142
    c.rr(48,540,1032,930,44,TD); phones(c,540,735,VI,[MINT,LAV,WH,MINT],WH)
    c.rr(48,950,1032,1160,44,TD); c.ar(996,1010,cv["ar"],58,WH); c.ar(996,1084,cv["arsub"],36,MINT); c.tx(96,1125,"sadaclips.com",F("JB",28),LAV,"lm")
    bar(c,1,7,BONE,TD,VI,WH); c.save(f"{OUT}/{tag}_01.jpg")
    for i,s in enumerate(p["slides"],2):
        c=C(BONE); c.pillL(64,98,s["k"],TD,WH); c.tx(1016,98,"SADA",F("J",50),VI,"rm")
        y=190
        for ln in s["h"]:
            if isinstance(ln,str): c.tx(64,y,ln,F("J",100,True),TD)
            else: c.hl(64,y,ln[0],ln[1],ln[2],100,TD,VI,WH)
            y+=114
        c.wrap(64,y+24,s["b"],"JM",34,"#33423f",900,48)
        c.rr(48,730,1032,866,36,VI)
        for k,t in enumerate(s["ar"]): c.ar(996,768+k*58,t,42,WH)
        c.rr(48,880,1032,1160,44,TD); G[s["g"]](c,1020); bar(c,i,7,TD,WH,VI,WH); c.save(f"{OUT}/{tag}_{i:02d}.jpg")
    t=p["cta"]; c=C(VI); c.tx(64,72,"SADA",F("J",54),WH); c.pill(1016,98,"YOUR MOVE",TD,WH)
    c.tx(64,230,"READY TO",F("J",150,True),WH); c.tx(64,380,"BE",F("J",150,True),WH); c.hl(64,575,"","EVERYWHERE?","",112,WH,TD,MINT)
    c.wrap(64,740,"Book a free call and we will map your first campaign. Content in Arabic and English.","JM",38,"#E6DFFF",900,56)
    c.rr(48,930,1032,1160,44,TD); c.ar(996,985,"جاهز لتنتشر في كل مكان؟",54,WH); c.ar(996,1052,"احجز مكالمتك المجانية مع SADA",36,MINT); c.tx(96,1128,"sadaclips.com",F("J",36,True),LAV,"lm")
    bar(c,7,7,BONE,TD,VI,WH,"Book a call"); c.save(f"{OUT}/{tag}_07.jpg")
if __name__=="__main__":
    posts=json.load(open(sys.argv[1]))
    for tag in sys.argv[2:]: render(posts[tag],tag)
