#!/usr/bin/env python3
"""Mood boards for 2026-10-09: Alpine wellness lounge / Memphis Group pop hatchback.
Original, fictional, logo-free procedural art. Usage: python3 tools/moodart_20261009.py issues/2026-10-09/img"""
import sys, os, subprocess, math, numpy as np
from PIL import Image
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
TMP = "/tmp/moodart"; os.makedirs(TMP, exist_ok=True)
rng = np.random.default_rng(20261009)

def render_svg(name, svg, w, h):
    p = f"{TMP}/{name}.svg"; open(p, "w").write(svg); png = f"{TMP}/{name}.png"
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                    f"--window-size={w},{h}", f"--screenshot={png}", "file://" + p], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=60)
    save(name, Image.open(png).convert("RGB").crop((0, 0, w, h)))
def save(name, im):
    im.thumbnail((1400, 1400)); dst = f"{OUT}/{name}.webp"; im.save(dst, "WEBP", quality=80, method=6)
    print("ok", dst, im.size, os.path.getsize(dst))
def wrap(w, h, body, defs=""):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><defs>{defs}</defs>{body}</svg>'
def wheel(cx, cy, r, tyre, rim, accent=None):
    s = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{tyre}"/><circle cx="{cx}" cy="{cy}" r="{r*.62}" fill="{rim}"/>'
    if accent:
        for i in range(5):
            a = math.radians(i*72-90); s += f'<circle cx="{cx+r*.36*math.cos(a):.1f}" cy="{cy+r*.36*math.sin(a):.1f}" r="{r*.1:.1f}" fill="{accent}"/>'
    return s + f'<circle cx="{cx}" cy="{cy}" r="{r*.12}" fill="{tyre}"/>'

# ---------- A: Alpine wellness lounge ----------
def a_hero():
    W, H = 1600, 900
    d = '''<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#cfdde3"/><stop offset="1" stop-color="#f1ece4"/></linearGradient>
    <linearGradient id="body" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e9e4dc"/><stop offset="1" stop-color="#b9b2a7"/></linearGradient>
    <linearGradient id="gl" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f4d9b8"/><stop offset=".6" stop-color="#8aa3ab"/><stop offset="1" stop-color="#4b5d63"/></linearGradient>
    <filter id="b"><feGaussianBlur stdDeviation="8"/></filter>'''
    b = f'<rect width="{W}" height="{H}" fill="url(#sky)"/>'
    b += '<path d="M0,520 L230,300 L360,410 L560,190 L760,420 L900,330 L1120,140 L1340,380 L1480,290 L1600,380 L1600,620 L0,620 Z" fill="#9fb3ba"/>'
    b += '<path d="M490,260 L560,190 L630,270 L600,262 L560,240 L520,268 Z M1050,210 L1120,140 L1195,225 L1160,215 L1120,190 L1085,222 Z" fill="#ffffff"/>'
    b += '<path d="M0,600 C300,560 700,580 1000,560 C1250,545 1450,570 1600,560 L1600,900 L0,900 Z" fill="#f6f3ee"/>'
    for x in range(40, 1600, 90):
        hgt = 120 + (x*37 % 90); b += f'<path d="M{x},{600-hgt} L{x-28},{600} L{x+28},{600} Z" fill="#3f5a52" opacity=".85"/>'
    b += '<ellipse cx="820" cy="760" rx="560" ry="26" fill="#000" opacity=".16" filter="url(#b)"/>'
    body = 'M330,750 C320,700 335,650 380,628 C470,600 560,590 640,585 C700,520 780,480 880,470 L1150,470 C1230,474 1280,520 1300,590 C1330,600 1345,640 1340,700 L1330,750 Z'
    b += f'<path d="{body}" fill="url(#body)"/>'
    b += '<path d="M660,585 C715,525 790,492 880,488 L1140,488 C1205,492 1250,530 1270,586 Z" fill="url(#gl)"/>'
    b += '<rect x="560" y="470" width="660" height="16" rx="8" fill="#8a6a4a"/>'
    for i in range(6): b += f'<rect x="{590+i*100}" y="452" width="60" height="18" rx="5" fill="#c9a77c"/>'
    b += '<path d="M380,650 C600,630 1000,626 1335,640" stroke="#c9a77c" stroke-width="5" fill="none"/>'
    b += '<rect x="330" y="640" width="70" height="10" rx="5" fill="#fff6e5"/><rect x="1300" y="636" width="40" height="12" rx="6" fill="#e3a67a"/>'
    b += wheel(520, 750, 72, "#2d3331", "#d8d2c8", "#8a6a4a") + wheel(1160, 750, 72, "#2d3331", "#d8d2c8", "#8a6a4a")
    b += '<circle cx="1420" cy="170" r="70" fill="#fff8ec" opacity=".8"/>'
    render_svg("mb1-1", wrap(W, H, b, d), W, H)

def a_interior():
    W, H = 1000, 750
    d = '''<linearGradient id="win" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#dfe8ea"/><stop offset="1" stop-color="#f6f1ea"/></linearGradient>
    <linearGradient id="wool" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ece6dc"/><stop offset="1" stop-color="#cfc6b8"/></linearGradient>'''
    b = f'<rect width="{W}" height="{H}" fill="#7a5c43"/>'
    for i in range(0, W, 24): b += f'<rect x="{i}" y="0" width="22" height="{H}" fill="#{"8a6a4a" if (i//24)%2 else "94735a"}"/>'
    b += '<path d="M90,60 L910,60 L880,330 L120,330 Z" fill="url(#win)"/>'
    b += '<path d="M120,330 L300,170 L420,260 L560,120 L720,280 L800,220 L880,330 Z" fill="#a9bcc2"/><path d="M520,160 L560,120 L600,165 Z" fill="#fff"/>'
    b += '<path d="M0,330 L1000,330 L1000,450 C700,430 300,430 0,450 Z" fill="#e9e3d9"/>'
    b += '<rect x="80" y="360" width="840" height="26" rx="13" fill="#c9a77c"/>'
    for cx in (260, 740):
        b += f'<path d="M{cx-150},750 L{cx-130},500 C{cx-120},460 {cx+120},460 {cx+130},500 L{cx+150},750 Z" fill="url(#wool)"/>'
        for k in range(5): b += f'<line x1="{cx-120}" y1="{520+k*45}" x2="{cx+120}" y2="{520+k*45}" stroke="#b8ae9f" stroke-width="3"/>'
    b += '<rect x="420" y="520" width="160" height="230" rx="18" fill="#5f4633"/><circle cx="500" cy="580" r="26" fill="#e3a67a" opacity=".85"/>'
    b += '<rect x="450" y="650" width="100" height="8" rx="4" fill="#e9e3d9"/>'
    render_svg("mb1-2", wrap(W, H, b, d), W, H)

def a_sauna_detail():
    W, H = 1000, 750
    b = f'<rect width="{W}" height="{H}" fill="#3a2a1f"/>'
    for i in range(14):
        y = 40 + i*50; b += f'<rect x="60" y="{y}" width="880" height="44" rx="6" fill="#{["b5895f","a97e56","bf9367"][i%3]}"/>'
        b += f'<path d="M60,{y+20} C300,{y+14} 640,{y+28} 940,{y+18}" stroke="#7d5737" stroke-opacity=".5" stroke-width="2" fill="none"/>'
    b += '<rect x="360" y="230" width="280" height="280" rx="140" fill="#f2c79a" opacity=".22"/>'
    b += '<rect x="420" y="290" width="160" height="160" rx="80" fill="#ffd9a8" opacity=".55"/>'
    b += '<rect x="120" y="610" width="760" height="18" rx="9" fill="#e9e3d9"/>'
    render_svg("mb1-3", wrap(W, H, b), W, H)

def felt_texture(name, w=1000, h=750):
    from PIL import ImageFilter
    def blur(r):
        n = rng.normal(128, 40, (h, w)).clip(0, 255).astype(np.uint8)
        return np.asarray(Image.fromarray(n).filter(ImageFilter.GaussianBlur(r)), dtype=float)
    a = blur(1.2)*0.4 + blur(6)*3
    a = (a - a.min())/(a.max()-a.min())
    base = np.array([214, 206, 194]); dark = np.array([170, 160, 146])
    img = (dark[None, None]*(1-a[..., None]) + base[None, None]*a[..., None]).astype(np.uint8)
    save(name, Image.fromarray(img))

# ---------- B: Memphis Group pop hatchback ----------
def b_hero():
    W, H = 1600, 900
    b = f'<rect width="{W}" height="{H}" fill="#f7e9d7"/>'
    for i in range(0, W, 40): b += f'<path d="M{i},120 l20,-20 l20,20" stroke="#1d1d1f" stroke-width="5" fill="none"/>'
    b += '<circle cx="1330" cy="250" r="120" fill="#ffcc33"/><rect x="140" y="170" width="220" height="220" fill="#2bb3c0" transform="rotate(14 250 280)"/>'
    for x in range(0, W, 26):
        for y in range(420, 560, 26): b += f'<circle cx="{x+13}" cy="{y}" r="4" fill="#1d1d1f" opacity=".7"/>'
    b += '<path d="M1450,380 l60,100 l-120,0 Z" fill="#ff5a7a"/>'
    b += '<rect y="660" width="1600" height="240" fill="#1d1d1f"/>'
    for x in range(0, W, 80): b += f'<rect x="{x}" y="660" width="40" height="240" fill="#2a2a2c"/>'
    body = 'M400,700 L400,560 C400,520 430,500 470,495 L660,480 L760,380 C780,362 800,355 830,355 L1120,355 C1150,355 1170,370 1180,400 L1210,500 C1230,505 1240,525 1240,560 L1240,700 Z'
    b += f'<path d="{body}" fill="#ff5a7a" stroke="#1d1d1f" stroke-width="10" stroke-linejoin="round"/>'
    b += '<path d="M690,478 L780,388 C792,378 805,374 830,374 L1110,374 C1135,374 1150,385 1158,405 L1185,480 Z" fill="#2bb3c0" stroke="#1d1d1f" stroke-width="8"/>'
    b += '<line x1="960" y1="374" x2="960" y2="480" stroke="#1d1d1f" stroke-width="10"/>'
    b += '<rect x="400" y="560" width="840" height="46" fill="#ffcc33" stroke="#1d1d1f" stroke-width="8"/>'
    for x in range(420, 1230, 36): b += f'<path d="M{x},572 l12,22 l12,-22" stroke="#1d1d1f" stroke-width="4" fill="none"/>'
    b += '<rect x="410" y="510" width="60" height="34" fill="#fff" stroke="#1d1d1f" stroke-width="6"/><circle cx="1215" cy="525" r="18" fill="#2bb3c0" stroke="#1d1d1f" stroke-width="6"/>'
    b += wheel(560, 700, 78, "#1d1d1f", "#ffcc33", "#1d1d1f") + wheel(1080, 700, 78, "#1d1d1f", "#ffcc33", "#1d1d1f")
    render_svg("mb2-1", wrap(W, H, b), W, H)

def b_dash():
    W, H = 1000, 750
    b = f'<rect width="{W}" height="{H}" fill="#2bb3c0"/>'
    for x in range(0, W, 30):
        for y in range(0, 300, 30): b += f'<rect x="{x+10}" y="{y+10}" width="6" height="6" fill="#1d1d1f" opacity=".35"/>'
    b += '<rect x="60" y="300" width="880" height="200" rx="0" fill="#f7e9d7" stroke="#1d1d1f" stroke-width="10"/>'
    b += '<circle cx="260" cy="400" r="80" fill="#ffcc33" stroke="#1d1d1f" stroke-width="8"/><line x1="260" y1="400" x2="310" y2="350" stroke="#1d1d1f" stroke-width="8"/>'
    b += '<rect x="420" y="340" width="200" height="120" fill="#ff5a7a" stroke="#1d1d1f" stroke-width="8"/>'
    for i in range(4): b += f'<circle cx="{690+i*60}" cy="400" r="22" fill="{["#ffcc33","#2bb3c0","#ff5a7a","#7c4dff"][i]}" stroke="#1d1d1f" stroke-width="6"/>'
    b += '<path d="M0,560 L1000,560 L1000,750 L0,750 Z" fill="#ff5a7a"/>'
    for x in range(-50, 1000, 70): b += f'<path d="M{x},600 q35,-30 70,0 t70,0" stroke="#1d1d1f" stroke-width="7" fill="none"/>'
    b += '<path d="M380,750 L420,520 L580,520 L620,750 Z" fill="#7c4dff" stroke="#1d1d1f" stroke-width="8"/>'
    render_svg("mb2-2", wrap(W, H, b), W, H)

def b_objects():
    W, H = 1000, 750
    b = f'<rect width="{W}" height="{H}" fill="#fff"/>'
    for i in range(0, W, 50): b += f'<line x1="{i}" y1="0" x2="{i+300}" y2="{H}" stroke="#eee" stroke-width="2"/>'
    b += '<circle cx="250" cy="260" r="150" fill="#ffcc33" stroke="#1d1d1f" stroke-width="10"/>'
    b += '<rect x="520" y="120" width="300" height="200" fill="#2bb3c0" stroke="#1d1d1f" stroke-width="10" transform="rotate(-8 670 220)"/>'
    b += '<path d="M600,620 L760,380 L920,620 Z" fill="#ff5a7a" stroke="#1d1d1f" stroke-width="10"/>'
    b += '<path d="M90,560 q60,-70 120,0 t120,0 t120,0" stroke="#7c4dff" stroke-width="22" fill="none" stroke-linecap="round"/>'
    for x in range(120, 480, 40): b += f'<circle cx="{x}" cy="660" r="9" fill="#1d1d1f"/>'
    render_svg("mb2-3", wrap(W, H, b), W, H)

def terrazzo_texture(name, w=1000, h=750):
    im = Image.new("RGB", (w, h), (246, 240, 230)); from PIL import ImageDraw
    dr = ImageDraw.Draw(im); cols = [(255, 90, 122), (43, 179, 192), (255, 204, 51), (29, 29, 31), (124, 77, 255)]
    for _ in range(900):
        x, y = rng.integers(0, w), rng.integers(0, h); r = rng.integers(3, 16); c = cols[rng.integers(0, 5)]
        pts = [(x + r*math.cos(a)*rng.uniform(.6, 1.2), y + r*math.sin(a)*rng.uniform(.6, 1.2)) for a in np.linspace(0, 2*math.pi, 6)[:-1]]
        dr.polygon(pts, fill=c)
    save(name, im)

if __name__ == "__main__":
    a_hero(); a_interior(); a_sauna_detail(); felt_texture("mb1-4")
    b_hero(); b_dash(); b_objects(); terrazzo_texture("mb2-4")
