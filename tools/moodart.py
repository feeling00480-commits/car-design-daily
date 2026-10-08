#!/usr/bin/env python3
"""Procedural mood-board artwork (original, fictional, logo-free).
Generates SVG illustrations + numpy material textures, renders to WebP.
Usage: python3 tools/moodart.py issues/2026-10-08/img
Fallback used when no AI image-generation tool is available."""
import sys, os, subprocess, math, numpy as np
from PIL import Image, ImageDraw, ImageFilter
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
TMP = "/tmp/moodart"; os.makedirs(TMP, exist_ok=True)
rng = np.random.default_rng(20261008)

def render_svg(name, svg, w, h):
    p = f"{TMP}/{name}.svg"; open(p, "w").write(svg)
    png = f"{TMP}/{name}.png"
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                    f"--window-size={w},{h}", f"--screenshot={png}", "file://" + p],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    im = Image.open(png).convert("RGB").crop((0, 0, w, h))
    save(name, im)

def save(name, im):
    im.thumbnail((1400, 1400))
    dst = f"{OUT}/{name}.webp"; im.save(dst, "WEBP", quality=82, method=6)
    print("ok", dst, im.size, os.path.getsize(dst))

def svg_wrap(w, h, body, defs=""):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><defs>{defs}</defs>{body}</svg>'

def palm(x, y, s, col):
    trunk = f'<path d="M{x},{y} C{x+10*s},{y-120*s} {x+30*s},{y-220*s} {x+55*s},{y-300*s}" stroke="{col}" stroke-width="{11*s}" fill="none" stroke-linecap="round"/>'
    tx, ty = x+55*s, y-300*s
    fr = ""
    for a in [-160, -125, -95, -60, -25, 10, 200, 235]:
        r = math.radians(a); ex, ey = tx+150*s*math.cos(r), ty+150*s*math.sin(r)*0.7+40*s
        cx, cy = tx+80*s*math.cos(r), ty-50*s
        fr += f'<path d="M{tx},{ty} Q{cx},{cy} {ex},{ey}" stroke="{col}" stroke-width="{9*s}" fill="none" stroke-linecap="round"/>'
    return trunk + fr

def wheel(cx, cy, r, rim, tyre="#1d1d1f", white=False, mesh=False):
    s = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{tyre}"/>'
    if white: s += f'<circle cx="{cx}" cy="{cy}" r="{r*0.74}" fill="#f4efe4"/>'
    s += f'<circle cx="{cx}" cy="{cy}" r="{r*0.58}" fill="{rim}"/>'
    if mesh:
        for i in range(18):
            a = math.radians(i*20)
            s += f'<line x1="{cx}" y1="{cy}" x2="{cx+r*0.58*math.cos(a)}" y2="{cy+r*0.58*math.sin(a)}" stroke="#8a6a1f" stroke-width="2.2"/>'
        s += f'<circle cx="{cx}" cy="{cy}" r="{r*0.4}" fill="none" stroke="#8a6a1f" stroke-width="2"/>'
    else:
        s += f'<circle cx="{cx}" cy="{cy}" r="{r*0.42}" fill="none" stroke="#ffffff" stroke-opacity=".5" stroke-width="3"/>'
    s += f'<circle cx="{cx}" cy="{cy}" r="{r*0.14}" fill="#d9d9d9"/>'
    return s

# ---------------- Theme A: Mid-century Californian surf wagon ----------------
def a_hero():
    W, H = 1600, 900
    defs = '''<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f7d9b5"/><stop offset=".55" stop-color="#f2a07b"/><stop offset="1" stop-color="#e98a6a"/></linearGradient>
    <linearGradient id="sea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4f8ea8"/><stop offset="1" stop-color="#2f6f8f"/></linearGradient>
    <linearGradient id="body" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#a9d8ca"/><stop offset="1" stop-color="#6fae9c"/></linearGradient>
    <linearGradient id="roof" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fbf5e9"/><stop offset="1" stop-color="#e9dcc3"/></linearGradient>
    <linearGradient id="glass" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffe2c7"/><stop offset=".5" stop-color="#7fb2c4"/><stop offset="1" stop-color="#2c5568"/></linearGradient>
    <pattern id="wood" width="600" height="14" patternUnits="userSpaceOnUse"><rect width="600" height="14" fill="#a8693a"/><path d="M0,4 C150,2 300,7 600,3" stroke="#7d4a25" stroke-width="1.6" fill="none"/><path d="M0,10 C200,12 380,8 600,11" stroke="#c48a55" stroke-width="1.2" fill="none"/></pattern>
    <filter id="soft"><feGaussianBlur stdDeviation="6"/></filter>'''
    b = f'<rect width="{W}" height="{H}" fill="url(#sky)"/>'
    b += '<circle cx="1180" cy="520" r="120" fill="#fff1d6" opacity=".9"/>'
    b += f'<rect y="560" width="{W}" height="120" fill="url(#sea)"/>'
    for i in range(9):
        y = 575 + i*12; b += f'<path d="M0,{y} Q400,{y-4} 800,{y} T1600,{y}" stroke="#ffe7cf" stroke-opacity="{0.35-i*0.03:.2f}" stroke-width="2" fill="none"/>'
    b += f'<rect y="680" width="{W}" height="220" fill="#ecd3ad"/><rect y="680" width="{W}" height="10" fill="#d8b98d"/>'
    b += palm(120, 700, 1.25, "#5b3a2e") + palm(1450, 700, 1.0, "#5b3a2e") + palm(1530, 710, 0.75, "#6b4636")
    b += '<ellipse cx="800" cy="738" rx="560" ry="22" fill="#000" opacity=".18" filter="url(#soft)"/>'
    # surfboard + rack
    b += '<rect x="720" y="452" width="10" height="18" fill="#c0c0c0"/><rect x="1120" y="450" width="10" height="20" fill="#c0c0c0"/>'
    b += '<path d="M640,447 C760,420 1150,418 1250,440 C1150,458 760,462 640,447 Z" fill="#c8643b"/><path d="M660,446 C800,436 1100,434 1230,440" stroke="#f2e8d5" stroke-width="5" fill="none"/>'
    # body
    body = 'M300,690 C292,660 292,622 306,600 C330,585 420,572 540,566 L600,560 C625,520 650,490 676,474 L1230,468 C1262,470 1280,490 1288,540 L1296,640 C1298,670 1292,688 1282,690 Z'
    b += f'<path d="{body}" fill="url(#body)"/>'
    b += '<path d="M676,474 L1230,468 C1262,470 1280,490 1286,528 L590,560 C620,520 648,490 676,474 Z" fill="url(#roof)"/>'
    b += '<path d="M624,548 L686,486 L1210,482 C1236,484 1250,505 1256,540 Z" fill="url(#glass)"/>'
    b += '<rect x="860" y="482" width="16" height="64" fill="url(#roof)"/><rect x="1060" y="482" width="16" height="62" fill="url(#roof)"/>'
    b += '<path d="M300,606 C420,580 900,556 1290,548" stroke="#e6e6e6" stroke-width="5" fill="none"/>'
    b += '<rect x="640" y="572" width="610" height="70" rx="14" fill="url(#wood)" stroke="#f4efe4" stroke-width="5"/>'
    b += '<line x1="860" y1="572" x2="860" y2="642" stroke="#f4efe4" stroke-width="4"/><line x1="1060" y1="572" x2="1060" y2="642" stroke="#f4efe4" stroke-width="4"/>'
    b += '<circle cx="470" cy="690" r="78" fill="#2a3b38"/><circle cx="1130" cy="690" r="78" fill="#2a3b38"/>'
    b += '<rect x="290" y="676" width="1010" height="16" rx="8" fill="#e8e8e8"/>'
    b += '<ellipse cx="316" cy="616" rx="14" ry="20" fill="#fff6dc" stroke="#e6e6e6" stroke-width="4"/>'
    b += '<rect x="1278" y="560" width="14" height="44" rx="6" fill="#c8643b"/>'
    b += wheel(470, 700, 64, "#d9d4c7", white=True) + wheel(1130, 700, 64, "#d9d4c7", white=True)
    render_svg("mb1-1", svg_wrap(W, H, b, defs), W, H)

def a_tailgate():
    W, H = 1000, 750
    defs = '''<linearGradient id="cream" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f7efe0"/><stop offset="1" stop-color="#e4d5bb"/></linearGradient>
    <linearGradient id="chrome" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset=".45" stop-color="#a9adb3"/><stop offset=".55" stop-color="#e5e7ea"/><stop offset="1" stop-color="#7d8288"/></linearGradient>
    <radialGradient id="lamp" cx=".4" cy=".35" r=".7"><stop offset="0" stop-color="#ffd2b8"/><stop offset=".5" stop-color="#d85a3a"/><stop offset="1" stop-color="#8e2f1d"/></radialGradient>'''
    b = f'<rect width="{W}" height="{H}" fill="url(#cream)"/>'
    for i in range(16):
        y = 170 + i*26; shade = ["#9a6237", "#a86d3e", "#8f5a32", "#b07445"][i % 4]
        b += f'<rect x="90" y="{y}" width="820" height="25" fill="{shade}"/>'
        b += f'<path d="M90,{y+8} C300,{y+4} 600,{y+14} 910,{y+7}" stroke="#6e4022" stroke-opacity=".55" stroke-width="1.5" fill="none"/>'
        b += f'<path d="M90,{y+17} C350,{y+21} 650,{y+13} 910,{y+18}" stroke="#d29a63" stroke-opacity=".5" stroke-width="1.2" fill="none"/>'
    b += '<rect x="90" y="170" width="820" height="416" rx="10" fill="none" stroke="url(#chrome)" stroke-width="14"/>'
    b += '<rect x="420" y="620" width="160" height="34" rx="17" fill="url(#chrome)"/>'
    b += '<circle cx="160" cy="100" r="46" fill="url(lamp)"/><circle cx="160" cy="100" r="46" fill="url(#lamp)" stroke="url(#chrome)" stroke-width="8"/>'
    b += '<circle cx="840" cy="100" r="46" fill="url(#lamp)" stroke="url(#chrome)" stroke-width="8"/>'
    b += '<rect x="0" y="690" width="1000" height="60" fill="#d9c7a6"/>'
    for i in range(60):
        x, y = rng.integers(0, 1000), rng.integers(694, 748); b += f'<circle cx="{x}" cy="{y}" r="{rng.uniform(1,2.5):.1f}" fill="#b8a07a"/>'
    render_svg("mb1-2", svg_wrap(W, H, b, defs), W, H)

def a_interior():
    W, H = 1000, 750
    defs = '''<linearGradient id="ocean" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffe2c4"/><stop offset=".5" stop-color="#f6b892"/><stop offset=".52" stop-color="#5f9bb3"/><stop offset="1" stop-color="#2f6f8f"/></linearGradient>
    <linearGradient id="dash" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9fd3c4"/><stop offset="1" stop-color="#6aa696"/></linearGradient>'''
    b = f'<rect width="{W}" height="{H}" fill="#2e2a26"/>'
    b += '<path d="M60,60 L940,60 L900,360 L100,360 Z" fill="url(#ocean)"/>'
    b += '<path d="M0,0 L1000,0 L1000,60 L0,60 Z M0,0 L60,60 L100,360 L0,420 Z M1000,0 L940,60 L900,360 L1000,420 Z" fill="#f2e8d5"/>'
    b += '<path d="M0,360 L1000,360 L1000,520 C800,500 200,500 0,520 Z" fill="url(#dash)"/>'
    b += '<rect x="80" y="395" width="840" height="38" rx="19" fill="#9a6237"/>'
    for i in range(14): b += f'<line x1="{100+i*60}" y1="399" x2="{130+i*60}" y2="429" stroke="#7d4a25" stroke-opacity=".4" stroke-width="2"/>'
    for cx in (330, 420): b += f'<circle cx="{cx}" cy="470" r="34" fill="#f4efe4" stroke="#c9ccd0" stroke-width="6"/><line x1="{cx}" y1="470" x2="{cx+18}" y2="452" stroke="#c8643b" stroke-width="4"/>'
    b += '<circle cx="375" cy="560" r="150" fill="none" stroke="#f4efe4" stroke-width="16"/><circle cx="375" cy="560" r="150" fill="none" stroke="#9a6237" stroke-width="8" stroke-dasharray="40 30"/>'
    b += '<line x1="375" y1="560" x2="245" y2="630" stroke="#f4efe4" stroke-width="12"/><line x1="375" y1="560" x2="505" y2="630" stroke="#f4efe4" stroke-width="12"/><circle cx="375" cy="560" r="34" fill="#c8643b"/>'
    b += '<path d="M0,600 C200,580 800,580 1000,600 L1000,750 L0,750 Z" fill="#c8643b"/>'
    for i in range(0, 1000, 26): b += f'<line x1="{i}" y1="600" x2="{i+10}" y2="750" stroke="#a34f2c" stroke-width="3"/>'
    b += '<rect x="640" y="455" width="200" height="60" rx="10" fill="#f2e8d5"/>'
    for i in range(6): b += f'<rect x="{655+i*30}" y="470" width="18" height="30" rx="4" fill="#2f6f8f" opacity="{0.4+i*0.1:.1f}"/>'
    render_svg("mb1-3", svg_wrap(W, H, b, defs), W, H)

def wood_texture(name, w=1000, h=750):
    y, x = np.mgrid[0:h, 0:w].astype(float)
    n = np.zeros((h, w))
    for f, a in [(0.004, 30), (0.011, 10), (0.03, 3)]:
        ph = rng.uniform(0, 6.28, 2)
        n += a*np.sin(x*f + ph[0])*np.cos(y*f*0.3 + ph[1])
    g = np.sin((y + n)*0.22) * 0.5 + 0.5
    g = g**2.2
    fine = rng.normal(0, 1, (h, w)); fine = np.array(Image.fromarray(((fine*20)+128).clip(0,255).astype(np.uint8)).resize((w, h)).filter(ImageFilter.BoxBlur(1)))/255.0 - 0.5
    fine = np.repeat(np.mean(fine.reshape(h, w//50, 50), axis=2), 50, axis=1)*0.6 + fine*0.4
    dark, light = np.array([110, 62, 32]), np.array([186, 126, 76])
    t = (0.65*g + 0.35*(0.5+fine)).clip(0, 1)[..., None]
    img = (dark*(1-t) + light*t).clip(0, 255).astype(np.uint8)
    save(name, Image.fromarray(img).filter(ImageFilter.GaussianBlur(0.6)))

def rattan_texture(name, w=1000, h=750):
    im = Image.new("RGB", (w, h), "#3b2a1e"); d = ImageDraw.Draw(im)
    step = 50; cane = (222, 196, 150); shade = (176, 142, 96)
    for yy in range(-step, h+step, step):
        for off in (-8, 8): d.line([(0, yy+off), (w, yy+off)], fill=shade, width=9); d.line([(0, yy+off-1), (w, yy+off-1)], fill=cane, width=5)
    for xx in range(-step, w+step, step):
        for off in (-8, 8): d.line([(xx+off, 0), (xx+off, h)], fill=shade, width=9); d.line([(xx+off-1, 0), (xx+off-1, h)], fill=cane, width=5)
    for k in range(-h, w+h, step):
        d.line([(k, 0), (k+h, h)], fill=(196, 164, 116), width=7)
        d.line([(k, h), (k+h, 0)], fill=(206, 176, 128), width=7)
    for yy in range(0, h+step, step):
        for xx in range(0, w+step, step): d.ellipse([xx-26+step/2-25, yy-26+step/2-25, xx+26+step/2-25, yy+26+step/2-25], outline=(150, 118, 78), width=2)
    arr = np.array(im).astype(float); arr += rng.normal(0, 7, arr.shape); im = Image.fromarray(arr.clip(0, 255).astype(np.uint8))
    save(name, im.filter(ImageFilter.GaussianBlur(0.8)))

# ---------------- Theme B: Japanese retro-futurism 1980s ----------------
def b_hero():
    W, H = 1600, 900
    defs = '''<linearGradient id="nsky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0d0a24"/><stop offset=".6" stop-color="#2a1550"/><stop offset="1" stop-color="#5b1f62"/></linearGradient>
    <linearGradient id="sun" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffd166"/><stop offset=".5" stop-color="#ff8a3d"/><stop offset="1" stop-color="#ff2e88"/></linearGradient>
    <linearGradient id="pearl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset=".6" stop-color="#e3e1dc"/><stop offset="1" stop-color="#b9b6b0"/></linearGradient>
    <linearGradient id="tint" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3a3d44"/><stop offset=".5" stop-color="#19d3f0" stop-opacity=".35"/><stop offset="1" stop-color="#14121f"/></linearGradient>
    <filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    <clipPath id="sunclip"><rect x="0" y="0" width="1600" height="560"/></clipPath>'''
    b = f'<rect width="{W}" height="{H}" fill="url(#nsky)"/>'
    for i in range(70):
        b += f'<circle cx="{rng.integers(0,1600)}" cy="{rng.integers(0,380)}" r="{rng.uniform(.6,1.8):.1f}" fill="#fff" opacity="{rng.uniform(.3,.9):.2f}"/>'
    sun = '<circle cx="800" cy="520" r="230" fill="url(#sun)"/>'
    for i in range(7): sun += f'<rect x="560" y="{430+i*20}" width="480" height="{3+i*1.6:.1f}" fill="#2a1550"/>'
    b += f'<g clip-path="url(#sunclip)">{sun}</g>'
    # skyline
    x = 0
    while x < 1600:
        bw = int(rng.integers(40, 110)); bh = int(rng.integers(60, 230))
        b += f'<rect x="{x}" y="{560-bh}" width="{bw}" height="{bh}" fill="#120d2b"/>'
        for wy in range(560-bh+10, 550, 16):
            for wx in range(x+6, x+bw-8, 14):
                if rng.random() < 0.28: b += f'<rect x="{wx}" y="{wy}" width="6" height="7" fill="{["#ffd166","#19d3f0","#ff2e88"][rng.integers(0,3)]}" opacity=".8"/>'
        x += bw + int(rng.integers(0, 10))
    b += f'<rect y="560" width="{W}" height="340" fill="#0d0a24"/>'
    for i in range(1, 14):
        y = 560 + (i**1.8)*2.3; b += f'<line x1="0" y1="{y:.1f}" x2="1600" y2="{y:.1f}" stroke="#ff2e88" stroke-opacity=".55" stroke-width="2"/>'
    for i in range(-20, 21):
        b += f'<line x1="{800+i*40}" y1="560" x2="{800+i*260}" y2="900" stroke="#ff2e88" stroke-opacity=".45" stroke-width="2"/>'
    b += '<rect y="640" width="1600" height="10" fill="#19d3f0" filter="url(#glow)" opacity=".8"/>'
    # wedge car
    body = 'M270,705 L276,668 L300,640 C460,616 640,592 760,566 L880,512 C930,506 1020,505 1062,510 L1300,574 C1314,578 1322,590 1322,604 L1322,690 C1322,700 1314,706 1300,706 Z'
    b += '<ellipse cx="800" cy="742" rx="560" ry="18" fill="#000" opacity=".5"/>'
    b += f'<path d="{body}" fill="url(#pearl)"/>'
    b += '<path d="M776,566 L888,518 C930,513 1015,512 1054,517 L1240,566 Z" fill="url(#tint)"/>'
    b += '<line x1="1010" y1="514" x2="1030" y2="566" stroke="#e3e1dc" stroke-width="10"/>'
    b += '<path d="M290,646 L1320,612" stroke="#ff2e88" stroke-width="6" filter="url(#glow)"/><path d="M296,660 L1320,626" stroke="#19d3f0" stroke-width="4" filter="url(#glow)"/>'
    b += '<path d="M282,662 L300,644 L380,634 L376,650 Z" fill="#fff6d0" filter="url(#glow)"/>'
    b += '<rect x="1300" y="586" width="22" height="28" fill="#ff2e2e" filter="url(#glow)"/>'
    b += '<circle cx="470" cy="700" r="72" fill="#0f0d18"/><circle cx="1120" cy="700" r="72" fill="#0f0d18"/>'
    b += '<path d="M270,700 L1322,700 L1322,712 L270,712 Z" fill="#3a3d44"/>'
    b += wheel(470, 708, 60, "#d4a93a", mesh=True) + wheel(1120, 708, 60, "#d4a93a", mesh=True)
    render_svg("mb2-1", svg_wrap(W, H, b, defs), W, H)

def b_taillight():
    W, H = 1000, 750
    defs = '''<linearGradient id="smoke" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2b2d33"/><stop offset="1" stop-color="#0c0c10"/></linearGradient>
    <filter id="g" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="7" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    <linearGradient id="refl" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".22"/><stop offset=".3" stop-color="#fff" stop-opacity="0"/></linearGradient>'''
    b = f'<rect width="{W}" height="{H}" fill="#e3e1dc"/><rect y="0" width="{W}" height="200" fill="#d2cfc8"/>'
    b += '<rect x="40" y="250" width="920" height="210" rx="14" fill="url(#smoke)"/>'
    for r in range(4):
        for c in range(28):
            on = (r in (1, 2)) or (c < 4 or c > 23)
            col = "#ff2a3c" if on else "#3a1218"
            if r == 1 and 12 <= c <= 15: col = "#ffb347"
            b += f'<rect x="{62+c*31.5:.1f}" y="{272+r*44}" width="26" height="36" rx="3" fill="{col}" {"filter=\"url(#g)\"" if on else ""}/>'
    b += '<rect x="40" y="250" width="920" height="210" rx="14" fill="url(#refl)"/>'
    b += '<rect x="40" y="250" width="920" height="210" rx="14" fill="none" stroke="#9a9ca3" stroke-width="3"/>'
    b += '<rect x="0" y="520" width="1000" height="230" fill="#14121f"/>'
    for i in range(28):
        b += f'<rect x="{62+i*31.5:.1f}" y="{540+(i%3)*4}" width="22" height="{rng.integers(60,180)}" fill="#ff2a3c" opacity=".18"/>'
    b += '<path d="M0,520 L1000,520" stroke="#ff2e88" stroke-width="5" filter="url(#g)"/><path d="M0,534 L1000,534" stroke="#19d3f0" stroke-width="3" filter="url(#g)"/>'
    render_svg("mb2-2", svg_wrap(W, H, b, defs), W, H)

def b_cluster():
    W, H = 1000, 750
    defs = '''<filter id="g" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    <linearGradient id="hood" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4a4d55"/><stop offset="1" stop-color="#2a2c32"/></linearGradient>'''
    b = f'<rect width="{W}" height="{H}" fill="#1b1440"/>'
    b += '<path d="M60,140 L940,140 L960,520 L40,520 Z" fill="url(#hood)"/>'
    b += '<rect x="170" y="190" width="660" height="280" rx="10" fill="#07090a"/>'
    for i in range(40):
        h = 20 + i*4.2; on = i < 27
        b += f'<rect x="{195+i*15.5:.1f}" y="{360-h:.1f}" width="10" height="{h:.1f}" fill="{"#39ff88" if on else "#0e2a19"}" {"filter=\"url(#g)\"" if on else ""}/>'
    b += '<text x="200" y="440" font-family="monospace" font-size="64" fill="#39ff88" filter="url(#g)">088</text><text x="340" y="440" font-family="monospace" font-size="22" fill="#39ff88">km/h</text>'
    for i in range(10): b += f'<rect x="{560+i*24}" y="{410}" width="18" height="30" fill="{"#ffb347" if i<7 else "#3a2a10"}" filter="url(#g)"/>'
    b += '<text x="560" y="395" font-family="monospace" font-size="18" fill="#ffb347">FUEL · E</text>'
    for side, x0 in (("L", 70), ("R", 840)):
        b += f'<rect x="{x0}" y="230" width="90" height="220" rx="12" fill="#3a3d44" stroke="#5b5f68" stroke-width="3"/>'
        for k in range(5):
            col = ["#ff2e88", "#19d3f0", "#e3e1dc", "#ffb347", "#e3e1dc"][k]
            b += f'<rect x="{x0+18}" y="{248+k*40}" width="54" height="26" rx="5" fill="#22242a" stroke="{col}" stroke-width="2"/>'
    b += '<path d="M200,750 C200,600 800,600 800,750" fill="none" stroke="#2a2c32" stroke-width="46"/>'
    b += '<path d="M200,750 C200,600 800,600 800,750" fill="none" stroke="#ff2e88" stroke-width="4" stroke-dasharray="6 14" opacity=".8"/>'
    render_svg("mb2-3", svg_wrap(W, H, b, defs), W, H)

def velour_texture(name, w=1000, h=750):
    n = rng.normal(0, 1, (h, w))
    im = Image.fromarray(((n*30)+128).clip(0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))
    a = np.array(im).astype(float)/255.0
    streak = Image.fromarray(((rng.normal(0, 1, (h//6, w))*40)+128).clip(0, 255).astype(np.uint8)).resize((w, h)).filter(ImageFilter.GaussianBlur(3))
    s = np.array(streak).astype(float)/255.0
    yy, xx = np.mgrid[0:h, 0:w]
    sheen = 0.5 + 0.5*np.sin((xx*0.6 + yy)*0.006)
    t = (0.45*a + 0.35*s + 0.2*sheen)[..., None]
    base = np.array([72, 74, 82]); hi = np.array([150, 152, 160])
    img = (base*(1-t) + hi*t).clip(0, 255).astype(np.uint8)
    im = Image.fromarray(img); d = ImageDraw.Draw(im)
    for off, col in ((0, (255, 46, 136)), (34, (25, 211, 240)), (58, (255, 138, 61))):
        d.polygon([(0, 470+off), (w, 250+off), (w, 268+off), (0, 488+off)], fill=col)
    save(name, im.filter(ImageFilter.GaussianBlur(0.4)))

def mesh_texture(name, w=1000, h=750):
    im = Image.new("RGB", (w, h), (18, 16, 26)); d = ImageDraw.Draw(im)
    r = 26; dx = r*math.sqrt(3); dy = r*1.5
    row = 0; y = 0
    while y < h + r:
        x = (dx/2 if row % 2 else 0)
        while x < w + r:
            pts = [(x + r*0.82*math.cos(math.radians(60*k+30)), y + r*0.82*math.sin(math.radians(60*k+30))) for k in range(6)]
            g = 0.55 + 0.45*math.sin((x+y)*0.004)
            d.polygon(pts, outline=(int(212*g), int(169*g), int(58*g)), width=7)
            x += dx
        y += dy; row += 1
    arr = np.array(im).astype(float)
    yy, xx = np.mgrid[0:h, 0:w]
    arr *= (0.55 + 0.45*np.exp(-((xx-300)**2 + (yy-250)**2)/(2*320**2)))[..., None]
    arr[:, :, :] += (np.clip(1 - np.abs((xx - yy*0.8 - 300)/60.0), 0, 1)*40)[..., None]
    save(name, Image.fromarray(arr.clip(0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.7)))

if __name__ == "__main__":
    a_hero(); a_tailgate(); a_interior(); wood_texture("mb1-4"); rattan_texture("mb1-5")
    b_hero(); b_taillight(); b_cluster(); velour_texture("mb2-4"); mesh_texture("mb2-5")
