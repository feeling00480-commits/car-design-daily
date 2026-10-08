#!/usr/bin/env python3
"""Render static pages from issues/<date>/data.json.
Outputs: issues/<date>/index.html for every issue, root index.html (= latest issue), archive/index.html.
Usage: python3 tools/build.py [--site-url https://xxxx.flypod.page]"""
import json, os, glob, html, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = ""
if "--site-url" in sys.argv: SITE = sys.argv[sys.argv.index("--site-url")+1].rstrip("/")
e = html.escape
WD = ["週一","週二","週三","週四","週五","週六","週日"]

def switcher(root, mode):
    """Segmented section switcher shown on every page. root = relative path to site root."""
    car = ' aria-current="page" class="on"' if mode == "car" else ''
    ai = ' aria-current="page" class="on"' if mode == "ai" else ''
    return (f'<nav class="modes" aria-label="切換日報"><a href="{root}"{car}><i class="dot"></i>汽車設計</a>'
            f'<a href="{root}ai/"{ai}><i class="dot"></i>AI 模型</a></nav>')

def topbar(root, mode, brand_href, nav_html=""):
    brand = ('CAR DESIGN <span>DAILY</span>' if mode == "car" else 'AI MODEL <span>DAILY</span>')
    return (f'<header class="topbar"><div class="wrap"><a class="brand" href="{brand_href}">{brand}</a>'
            f'{switcher(root, mode)}{nav_html}<button class="toggle" id="tg" aria-label="切換深淺色">◐<span class="tl"> 深／淺</span></button></div></header>')

def theme_init(mode):
    key = "cdd-theme-ai" if mode == "ai" else "cdd-theme"
    dflt = "'dark'" if mode == "ai" else "null"
    return f"<script>(function(){{var t=localStorage.getItem('{key}')||{dflt};if(t)document.documentElement.setAttribute('data-theme',t);}})();</script>"

def theme_toggle(mode):
    key = "cdd-theme-ai" if mode == "ai" else "cdd-theme"
    return ("<script>document.getElementById('tg').onclick=function(){var r=document.documentElement,c=r.getAttribute('data-theme');"
            "var dark=c?c==='dark':matchMedia('(prefers-color-scheme: dark)').matches;var n=dark?'light':'dark';"
            f"r.setAttribute('data-theme',n);localStorage.setItem('{key}',n);}};</script>")

def issues():
    out = []
    for p in sorted(glob.glob(f"{ROOT}/issues/*/data.json"), reverse=True):
        out.append(json.load(open(p, encoding="utf-8")))
    return out

DIAGRAM = '''<svg class="diagram" viewBox="0 0 520 150" width="100%" role="img" aria-label="dash-to-axle 示意圖">
<path d="M30,112 C30,96 40,88 70,84 L170,76 L230,46 L380,44 C430,46 460,62 480,80 L492,112 Z" fill="none" stroke="currentColor" stroke-width="2.5"/>
<circle cx="110" cy="114" r="20" fill="none" stroke="currentColor" stroke-width="2.5"/><circle cx="420" cy="114" r="20" fill="none" stroke="currentColor" stroke-width="2.5"/>
<line x1="110" y1="20" x2="110" y2="140" stroke="#f08a5d" stroke-dasharray="4 4" stroke-width="1.5"/><line x1="200" y1="20" x2="200" y2="140" stroke="#f08a5d" stroke-dasharray="4 4" stroke-width="1.5"/>
<line x1="110" y1="28" x2="200" y2="28" stroke="#f08a5d" stroke-width="2"/><text x="155" y="20" fill="#f08a5d" font-size="12" text-anchor="middle">dash-to-axle</text>
<text x="200" y="146" fill="currentColor" font-size="11" text-anchor="middle" opacity=".7">A 柱底／儀表板</text><text x="110" y="146" fill="currentColor" font-size="11" text-anchor="middle" opacity=".7">前軸</text></svg>'''

def page(d, base, all_issues, is_root):
    date = d["date"]; y, m, dd = date.split("-")
    img = f"{base}issues/{date}/img/" if is_root else "img/"
    css = f"{base}assets/style.css"
    title = f"汽車設計日報 Car Design Daily · {y}.{m}.{dd}"
    desc = d["lede"]
    lead = d["design_news"][0].get("image")
    ogimg = (f"{SITE}/issues/{date}/img/{lead['file']}" if lead else f"{SITE}/issues/{date}/img/{d['moodboards'][0]['images'][0][0]}.webp") if SITE else ""
    canon = (f"{SITE}/issues/{date}/" if SITE else "")
    H = []
    H.append(f'''<!doctype html><html lang="zh-Hant-TW"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(title)}</title><meta name="description" content="{e(desc)}">
<meta property="og:type" content="article"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}">
{f'<meta property="og:image" content="{ogimg}"><meta name="twitter:card" content="summary_large_image">' if ogimg else ''}
{f'<link rel="canonical" href="{canon}">' if canon else ''}
<meta name="theme-color" content="#111114">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Noto+Sans+TC:wght@400;600&family=Noto+Serif+TC:wght@600;700&family=Playfair+Display:ital,wght@0,700;0,800;1,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{css}">
{theme_init("car")}
</head><body class="mode-car">
{topbar(base, "car", base, f'<nav class="nav"><a href="#design">設計新聞</a><a href="#knowledge">汽車新知</a><a href="#mood">情緒板</a><a href="{base}archive/">往期</a></nav>')}
<main class="wrap">
<div class="mast"><div class="kicker">Issue No. {d['issue_no']:03d} · Global Car Design Digest</div>
<h1>Car Design Daily<span class="zh">汽車設計日報</span></h1>
<div class="meta"><span><b>{y} 年 {int(m)} 月 {int(dd)} 日</b> {d['weekday']}</span><span>設計新聞 {len(d['design_news'])} 則</span><span>汽車新知 {len(d['knowledge'])} 則</span><span>情緒板 {len(d['moodboards'])} 組</span></div>
<p class="lede">{e(d['lede'])}</p></div>''')
    # design news
    H.append('<section id="design"><div class="sec-head"><span class="num">01</span><h2>設計新聞</h2><span class="en">Design News</span></div><div class="news">')
    for i, s in enumerate(d["design_news"]):
        an = "".join(f'<li><b>{e(k)}</b><span>{e(v)}</span></li>' for k, v in s["analysis"])
        src = "".join(f'<a href="{e(u)}" target="_blank" rel="noopener">{e(n)} ↗</a>' for n, u in s["sources"])
        im = s.get("image")
        fig = (f'<figure class="news-img"><div class="ratio"><img src="{img}{e(im["file"])}" alt="{e(im["alt"])}" loading="{"eager" if i == 0 else "lazy"}" decoding="async" width="1600" height="900"></div>'
               f'<figcaption>圖片來源：<a href="{e(im["credit_url"])}" target="_blank" rel="noopener">{e(im["credit"])}</a></figcaption></figure>') if im else ""
        head = f'<div class="shead"><span class="tag">{e(s["brand"])} · {e(s["tag"])}</span><span class="date">{e(s["date"])}</span><h3>{e(s["title"])}</h3><p class="orig">{e(s["orig"])}</p><p class="sum">{e(s["summary"])}</p>'
        if i == 0:
            H.append(f'<article class="story feature" id="{s["id"]}">{fig}{head}<div class="src">來源：{src}</div></div><div class="fan"><p class="alabel">設計解析 Design Notes</p><ul class="analysis">{an}</ul></div></article>')
        else:
            H.append(f'<article class="story" id="{s["id"]}">{fig}{head}</div><p class="alabel">設計解析 Design Notes</p><ul class="analysis">{an}</ul><div class="src">來源：{src}</div></article>')
    H.append('</div></section>')
    # knowledge
    H.append('<section id="knowledge"><div class="sec-head"><span class="num">02</span><h2>汽車新知</h2><span class="en">Industry &amp; Tech</span></div><div class="kgrid">')
    for k in d["knowledge"]:
        src = "".join(f'<a href="{e(u)}" target="_blank" rel="noopener">{e(n)} ↗</a>' for n, u in k["sources"])
        H.append(f'<article class="k"><span class="tag">{e(k["tag"])}</span><span class="date" style="font-size:12px;color:var(--muted);margin-left:8px">{e(k["date"])}</span><h3>{e(k["title"])}</h3><p>{e(k["summary"])}</p><div class="src">{src}</div></article>')
    t = d["term"]
    H.append(f'</div><div class="term"><div><div class="lab">今日設計名詞 · Term of the Day</div><h3>{e(t["name"])}</h3><div class="zh">{e(t["zh"])}</div>{DIAGRAM}</div><p>{e(t["body"])}</p></div></section>')
    # mood boards
    H.append('<section id="mood"><div class="sec-head"><span class="num">03</span><h2>情緒板</h2><span class="en">Mood Boards</span></div>')
    H.append('<p class="note">情緒板裡的車輛都是原創虛構的概念設計，不代表任何真實車款或品牌。圖像為程式生成的插畫和材質紋理，主題每期隨機抽選。</p>')
    for b in d["moodboards"]:
        figs = "".join(f'<figure class="tile{" hero" if h else ""}"><img src="{img}{n}.webp" alt="{e(c)}" loading="lazy" decoding="async"><figcaption>{e(c)}</figcaption></figure>' for n, c, h in b["images"])
        pal = "".join(f'<div class="sw"><i style="background:{hx}"></i><span>{e(nm)}<br><code>{hx}</code></span></div>' for nm, hx in b["palette"])
        kw = "".join(f'<span>{e(k)}</span>' for k in b["keywords"])
        mt = "".join(f'<li>{e(x)}</li>' for x in b["materials"])
        H.append(f'<div class="board"><div class="board-head"><div><div class="kicker">Random Theme</div><h3>{e(b["theme"])}</h3><div class="zh">{e(b["zh"])}</div></div><p>{e(b["intro"])}</p></div><div class="mgrid">{figs}</div><div class="bwrap"><div class="palette">{pal}</div><div class="bmeta"><div><h4>關鍵字 Keywords</h4><div class="chips">{kw}</div></div><div><h4>材質筆記 Material Notes</h4><ul>{mt}</ul></div></div></div></div>')
    H.append('</section>')
    # archive
    li = "".join(f'<li><a href="{base}issues/{x["date"]}/">No.{x["issue_no"]:03d} · {x["date"]}</a> — {e(x["design_news"][0]["title"])}</li>' for x in all_issues)
    H.append(f'<section class="archive" id="archive"><div class="sec-head"><span class="num">∞</span><h2>往期</h2><span class="en">Archive</span></div><ul>{li}</ul></section>')
    H.append(f'''</main><footer><div class="wrap">Car Design Daily · 每日整理全球汽車設計新聞、產業新知與隨機情緒板。內容摘要與分析為編輯整理，事實以原始來源為準；新聞圖片取自車廠官方新聞室／原報導，版權屬原權利人，均標示來源並連結原頁。<br>Issue {d["issue_no"]:03d} · {date}</div></footer>
{theme_toggle("car")}
</body></html>''')
    return "\n".join(H)

def archive_page(all_issues):
    li = "".join(f'<li><a href="../issues/{x["date"]}/">No.{x["issue_no"]:03d} · {x["date"]} {x["weekday"]}</a> — {e(x["design_news"][0]["title"])}</li>' for x in all_issues)
    return f'''<!doctype html><html lang="zh-Hant-TW"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>往期 · Car Design Daily</title><link rel="stylesheet" href="../assets/style.css">
{theme_init("car")}</head>
<body class="mode-car">{topbar("../", "car", "../")}
<main class="wrap"><section class="archive"><div class="sec-head"><span class="num">∞</span><h2>往期</h2><span class="en">Archive</span></div><ul>{li}</ul></section></main>{theme_toggle("car")}</body></html>'''

if __name__ == "__main__":
    al = issues()
    for d in al:
        open(f"{ROOT}/issues/{d['date']}/index.html", "w", encoding="utf-8").write(page(d, "../../", al, False))
    open(f"{ROOT}/index.html", "w", encoding="utf-8").write(page(al[0], "./", al, True))
    os.makedirs(f"{ROOT}/archive", exist_ok=True)
    open(f"{ROOT}/archive/index.html", "w", encoding="utf-8").write(archive_page(al))
    print("built", [d["date"] for d in al])
