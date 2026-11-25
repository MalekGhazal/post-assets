import sys, os, json
from PIL import Image, ImageDraw, ImageFont
FD = os.environ.get("FONTDIR", "fonts"); OUT = os.environ.get("OUTDIR", "out")
S = 2; W, H = 1080*S, 1350*S
BG, INK, LIME, SKY, PEACH, MINT, LILAC, BUTTER, PINK, WHITE = "#EDEFF5", "#14151A", "#C8FF3D", "#C7E4FF", "#FFD3C2", "#C5F2DC", "#D9D2FF", "#FFE9A8", "#FFC7E4", "#FFFFFF"
def F(n, s, basic=False): return ImageFont.truetype(f"{FD}/{n}.ttf", int(s*S), layout_engine=(ImageFont.Layout.BASIC if basic else ImageFont.Layout.RAQM))
class C:
    def __init__(s): s.im = Image.new("RGB", (W, H), BG); s.d = ImageDraw.Draw(s.im)
    def rr(s, x0, y0, x1, y1, r, fill): s.d.rounded_rectangle([x0*S, y0*S, x1*S, y1*S], radius=r*S, fill=fill)
    def tx(s, x, y, t, f, fill, a="la", **k): s.d.text((x*S, y*S), t, font=f, fill=fill, anchor=a, **k)
    def circ(s, cx, cy, r, fill): s.d.ellipse([(cx-r)*S, (cy-r)*S, (cx+r)*S, (cy+r)*S], fill=fill)
    def line(s, pts, fill, w): s.d.line([(x*S, y*S) for x, y in pts], fill=fill, width=int(w*S))
    def pill(s, right, cy, label, bg, fg, size=26):
        f = F("JB", size); w = f.getlength(label)/S+48; s.rr(right-w, cy-26, right, cy+26, 26, bg); s.tx(right-w/2, cy+1, label, f, fg, "mm")
    def head(s, x, y, lines, size, fill, step):
        for ln in lines: s.tx(x, y, ln, F("J", size, True), fill); y += step
    def wrap(s, x, y, t, fp, size, fill, maxw, step):
        f = F(fp, size); line = ""
        for w in t.split():
            q = (line+" "+w).strip()
            if f.getlength(q)/S > maxw: s.tx(x, y, line, f, fill); y += step; line = w
            else: line = q
        if line: s.tx(x, y, line, f, fill)
    def bottom(s, n, tot, label, tile=INK, fg=WHITE, pb=LIME, pf=INK, cta=None):
        s.rr(48, 1176, 1032, 1302, 44, tile); s.tx(96, 1240, label, F("JB", 40), fg, "lm")
        if cta: s.rr(734, 1203, 998, 1275, 36, pb); s.tx(866, 1240, cta, F("J", 33), pf, "mm")
        else:
            lw = F("JB", 40).getlength(label)/S; ax = 96+lw+48
            s.line([(ax-26, 1240), (ax+24, 1240)], fg, 7); s.line([(ax+6, 1222), (ax+24, 1240), (ax+6, 1258)], fg, 7)
            s.pill(996, 1240, f"{n} / {tot}", pb, pf, 30)
    def hero(s, bg, y1, label, dark=False):
        s.rr(48, 48, 1032, y1, 44, bg); s.tx(96, 92, "WeBelle", F("J", 54), WHITE if dark else INK)
        s.pill(984, 118, label, LIME if dark else INK, INK if dark else WHITE)
    def save(s, name): s.im.resize((1080, 1350), Image.LANCZOS).convert("RGB").save(name, "JPEG", quality=92)
CY = (916+1160)/2
COLS = [LIME, SKY, PEACH, LILAC, MINT, BUTTER, PINK]
def g_chips(c, items, **k):
    fn = F("JB", 44); ws = [fn.getlength(t)/S+80 for t in items]
    rows, cur, curw = [], [], 0
    for t, w in zip(items, ws):
        if curw+w > 880 and cur: rows.append(cur); cur, curw = [], 0
        cur.append((t, w)); curw += w+20
    rows.append(cur)
    y = CY-(len(rows)*98-20)/2
    for r in rows:
        tw = sum(w for _, w in r)+20*(len(r)-1); x = 540-tw/2
        for i, (t, w) in enumerate(r):
            c.rr(x, y, x+w, y+78, 39, COLS[(items.index(t)) % 5]); c.tx(x+w/2, y+40, t, fn, INK, "mm"); x += w+20
        y += 98
def g_steps(c, active=1, **k):
    for i in range(4):
        cx = 210+i*220; col = LIME if i+1 == active else "#E3E5EC"
        if i < 3: c.line([(cx+46, CY), (cx+174, CY)], "#E3E5EC", 6)
        c.circ(cx, CY, 46, INK if i+1 == active else col); c.tx(cx, CY+2, str(i+1), F("J", 44, True), LIME if i+1 == active else "#9a9ca6", "mm")
def g_rtl(c, en="Home", ar="الرئيسية", **k):
    c.rr(120, CY-90, 520, CY+90, 36, BG); c.tx(320, CY+4, en, F("J", 64, True), INK, "mm")
    c.tx(540, CY+4, "→", F("J", 54, True), INK, "mm")
    c.rr(560, CY-90, 960, CY+90, 36, LILAC); c.tx(760, CY+6, ar, F("R", 70), INK, "mm", direction="rtl", language="ar")
def g_ar(c, ar="", **k):
    c.rr(180, CY-90, 900, CY+90, 40, LILAC); c.tx(540, CY+6, ar, F("R", 78), INK, "mm", direction="rtl", language="ar")
GR = {"chips": g_chips, "steps": g_steps, "rtl": g_rtl, "ar": g_ar}
def render(post, tag):
    os.makedirs(OUT, exist_ok=True); cv = post["cover"]; n = 7
    c = C(); c.rr(48, 48, 1032, 1160, 44, cv["color"]); c.tx(96, 92, "WeBelle", F("J", 54), INK); c.pill(984, 118, cv["pill"], INK, WHITE)
    c.rr(96, 200, 984, 480, 56, WHITE)
    g = cv["graphic"]; CYsave = CY
    globals()["CY"] = 340; GR[g["kind"]](c, **{k: v for k, v in g.items() if k != "kind"}); globals()["CY"] = CYsave
    c.head(96, 560, cv["head"], 104, INK, 114)
    c.tx(984, 910, cv["ar"], F("R", 44), INK, "ra", direction="rtl", language="ar")
    c.tx(96, 1040, cv["sub"], F("JM", 34), "#3a3a44"); c.bottom(1, n, "Swipe", LIME, INK, INK, LIME); c.save(f"{OUT}/{tag}_01.jpg")
    for i, s in enumerate(post["slides"], 2):
        c = C(); c.hero(s["color"], 900, s["kicker"])
        c.head(96, 250, s["head"], 92, INK, 104)
        c.wrap(96, 250+len(s["head"])*104+36, s["body"], "JM", 36, "#2e2f38", 880, 52)
        c.rr(48, 916, 1032, 1160, 44, WHITE); g = s["graphic"]; GR[g["kind"]](c, **{k: v for k, v in g.items() if k != "kind"})
        c.bottom(i, n, "Swipe"); c.save(f"{OUT}/{tag}_{i:02d}.jpg")
    t = post["cta"]; c = C(); c.hero(LIME, 900, "Your move")
    c.head(96, 190, t["head"], 104, INK, 114); c.wrap(96, 190+len(t["head"])*114+40, t["body"], "JM", 34, "#2a3010", 880, 49)
    def stat(x0, x1, bg, num, lab, fg):
        c.rr(x0, 916, x1, 1160, 44, bg); c.tx(x0+32, 936, num, F("J", 96, True), fg); c.tx(x0+32, 1130, lab, F("JB", 28), fg, "ls")
    stat(48, 524, INK, "EN+AR", "built in both languages", WHITE); stat(540, 1032, SKY, "UAE", "based in Dubai", INK)
    c.bottom(7, n, "Start a conversation", INK, WHITE, LIME, INK, cta="webelle.ae"); c.save(f"{OUT}/{tag}_07.jpg")
if __name__ == "__main__":
    posts = json.load(open(sys.argv[1]))
    for k in (sys.argv[2:] or posts.keys()): render(posts[k], k)
