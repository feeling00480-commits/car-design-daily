#!/usr/bin/env python3
"""Mood boards for 2026-10-10: Coastal regatta yacht-inspired roadster / Art Deco streamliner.
Original, fictional, logo-free. Usage: python3 tools/moodart_20261010.py issues/2026-10-10/img"""
import sys, os, subprocess, math, numpy as np
from PIL import Image, ImageFilter, ImageDraw
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
TMP = "/tmp/moodart1010"; os.makedirs(TMP, exist_ok=True)
rng = np.random.default_rng(20261010)

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
        for i in range(6):
            a = math.radians(i*60-90)
            s += f'<line x1="{cx}" y1="{cy}" x2="{cx+r*.5*math.cos(a):.1f}" y2="{cy+r*.5*math.sin(a):.1f}" stroke="{accent}" stroke-width="3"/>'
    return s + f'<circle cx="{cx}" cy="{cy}" r="{r*.12}" fill="{tyre}"/>'

# ---------- A: Coastal regatta yacht-inspired roadster ----------
def a_hero():
    W, H = 1600, 900
    d = '''<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#a8d4e8"/><stop offset=".55" stop-color="#e8f2f6"/><stop offset="1" stop-color="#f7f4ee"/></linearGradient>
    <linearGradient id="sea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a7ca5"/><stop offset="1" stop-color="#1f4e6b"/></linearGradient>
    <linearGradient id="hull" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f4f7f8"/><stop offset="1" stop-color="#c5d0d6"/></linearGradient>
    <linearGradient id="gl" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#e8f6ff"/><stop offset=".6" stop-color="#5a8aa8"/><stop offset="1" stop-color="#1a3a4e"/></linearGradient>
    <filter id="b"><feGaussianBlur stdDeviation="8"/></filter>'''
    b = f'<rect width="{W}" height="{H}" fill="url(#sky)"/>'
    b += '<circle cx="1280" cy="160" r="55" fill="#fff8e0" opacity=".95"/>'
    # distant sails
    for x,hgt,col in [(180,160,"#ffffff"),(320,120,"#f0f4f6"),(1480,140,"#ffffff")]:
        b += f'<path d="M{x},{520-hgt} L{x},{520} L{x+48},{520-hgt*0.55} Z" fill="{col}" opacity=".9"/>'
        b += f'<line x1="{x}" y1="{520-hgt-10}" x2="{x}" y2="520" stroke="#2a4555" stroke-width="2"/>'
    b += f'<rect y="520" width="{W}" height="100" fill="url(#sea)"/>'
    for i in range(8):
        y=530+i*10; b += f'<path d="M0,{y} Q400,{y-5} 800,{y} T1600,{y}" stroke="#9fd0e8" stroke-opacity="{0.4-i*0.04:.2f}" stroke-width="2" fill="none"/>'
    b += f'<rect y="620" width="{W}" height="280" fill="#d9c9a8"/><rect y="620" width="{W}" height="12" fill="#c4b08a"/>'
    b += '<ellipse cx="820" cy="720" rx="520" ry="22" fill="#000" opacity=".15" filter="url(#b)"/>'
    # roadster: long hood, cut-down windscreen, teak deck accents
    body='M280,700 C270,650 290,600 340,575 C420,545 560,530 700,520 L980,515 C1080,518 1180,540 1240,590 C1280,620 1295,660 1290,700 Z'
    b += f'<path d="{body}" fill="url(#hull)"/>'
    b += '<path d="M700,520 L960,516 C1040,520 1120,545 1160,580 L720,585 C710,555 705,535 700,520 Z" fill="url(#gl)"/>'
    b += '<path d="M340,575 C500,555 900,545 1240,575" stroke="#1e5a8a" stroke-width="6" fill="none"/>'  # navy boot stripe
    b += '<rect x="560" y="500" width="420" height="14" rx="3" fill="#8b5a2b"/>'  # teak rail
    for i in range(8): b += f'<line x1="{570+i*50}" y1="500" x2="{570+i*50}" y2="514" stroke="#c49a6c" stroke-width="2"/>'
    b += '<path d="M640,515 L700,470 L760,515" fill="none" stroke="#2a4555" stroke-width="4"/>'  # low screen
    b += '<ellipse cx="310" cy="620" rx="18" ry="14" fill="#e8f6ff" stroke="#c5d0d6" stroke-width="3"/>'
    b += '<rect x="1260" y="600" width="28" height="10" rx="3" fill="#c45c26"/>'
    b += wheel(480, 700, 68, "#1d252b", "#e8eef0", "#1e5a8a") + wheel(1100, 700, 68, "#1d252b", "#e8eef0", "#1e5a8a")
    # rope coil
    b += '<circle cx="200" cy="780" r="36" fill="none" stroke="#c49a6c" stroke-width="10"/><circle cx="200" cy="780" r="18" fill="none" stroke="#8b5a2b" stroke-width="6"/>'
    render_svg("mb1-1", wrap(W, H, b, d), W, H)

def a_deck():
    W, H = 1000, 750
    d = '''<linearGradient id="teak" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#c49a6c"/><stop offset="1" stop-color="#8b5a2b"/></linearGradient>
    <linearGradient id="sky2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#b8d8e8"/><stop offset="1" stop-color="#eef4f6"/></linearGradient>'''
    b = f'<rect width="{W}" height="{H}" fill="#1f4e6b"/>'
    b += '<path d="M60,40 L940,40 L900,280 L100,280 Z" fill="url(#sky2)"/>'
    b += '<path d="M200,280 L280,120 L320,200 L400,90 L480,210 L560,100 L640,220 L720,110 L800,230 L900,280 Z" fill="#3a7ca5" opacity=".5"/>'
    # teak dashboard
    b += '<path d="M0,280 L1000,280 L1000,420 C700,400 300,400 0,420 Z" fill="url(#teak)"/>'
    for i in range(20):
        b += f'<line x1="{40+i*48}" y1="290" x2="{40+i*48}" y2="410" stroke="#d4b896" stroke-opacity=".45" stroke-width="3"/>'
    b += '<rect x="80" y="320" width="840" height="18" rx="9" fill="#1e5a8a"/>'
    # brass gauges
    for cx in (280, 420, 560):
        b += f'<circle cx="{cx}" cy="500" r="48" fill="#e8eef0" stroke="#b8976a" stroke-width="8"/>'
        b += f'<circle cx="{cx}" cy="500" r="36" fill="#f7f4ee"/><line x1="{cx}" y1="500" x2="{cx+20}" y2="475" stroke="#c45c26" stroke-width="3"/>'
    b += '<circle cx="720" cy="520" r="90" fill="none" stroke="#e8eef0" stroke-width="14"/><circle cx="720" cy="520" r="90" fill="none" stroke="#1e5a8a" stroke-width="6" stroke-dasharray="30 20"/>'
    b += '<path d="M0,560 C250,540 750,540 1000,560 L1000,750 L0,750 Z" fill="#f4f7f8"/>'
    b += '<path d="M0,560 C250,540 750,540 1000,560" stroke="#1e5a8a" stroke-width="5" fill="none"/>'
    render_svg("mb1-2", wrap(W, H, b, d), W, H)

def a_detail():
    W, H = 1000, 750
    b = f'<rect width="{W}" height="{H}" fill="#e8eef0"/>'
    # rope / cleat detail
    b += '<rect x="100" y="120" width="800" height="500" rx="12" fill="#c5d0d6"/>'
    b += '<rect x="140" y="160" width="720" height="40" rx="4" fill="#8b5a2b"/>'
    for i in range(12): b += f'<line x1="{160+i*58}" y1="160" x2="{160+i*58}" y2="200" stroke="#c49a6c" stroke-width="3"/>'
    # navy stripe
    b += '<rect x="140" y="280" width="720" height="28" fill="#1e5a8a"/>'
    b += '<rect x="140" y="320" width="720" height="8" fill="#f4f7f8"/>'
    # brass cleat
    b += '<ellipse cx="500" cy="480" rx="120" ry="28" fill="#b8976a"/><rect x="460" y="430" width="80" height="50" rx="10" fill="#d4b896"/>'
    b += '<path d="M380,500 C420,420 580,420 620,500" fill="none" stroke="#c49a6c" stroke-width="16"/><path d="M400,510 C440,450 560,450 600,510" fill="none" stroke="#8b5a2b" stroke-width="8"/>'
    b += '<circle cx="200" cy="600" r="8" fill="#1e5a8a"/><circle cx="800" cy="600" r="8" fill="#1e5a8a"/>'
    render_svg("mb1-3", wrap(W, H, b), W, H)

def sailcloth_texture(name, w=1000, h=750):
    im = Image.new("RGB", (w, h), "#e8eef0"); d = ImageDraw.Draw(im)
    for y in range(0, h, 3):
        shade = 220 + int(8*math.sin(y*0.05)) + int(rng.integers(-4, 5))
        d.line([(0, y), (w, y)], fill=(shade, shade+2, shade+4), width=2)
    for _ in range(40):
        x0, y0 = rng.integers(0, w), rng.integers(0, h)
        d.line([(x0, y0), (x0+rng.integers(20, 80), y0+rng.integers(-3, 4))], fill=(200, 205, 210), width=1)
    # navy stitch
    for y in range(80, h, 120):
        d.line([(40, y), (w-40, y)], fill=(30, 90, 138), width=3)
    save(name, im.filter(ImageFilter.GaussianBlur(0.4)))

# ---------- B: Art Deco streamliner ----------
def b_hero():
    W, H = 1600, 900
    d = '''<linearGradient id="dusk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1a1a2e"/><stop offset=".5" stop-color="#2d1f3d"/><stop offset="1" stop-color="#4a2c1a"/></linearGradient>
    <linearGradient id="gold" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f0d080"/><stop offset=".5" stop-color="#c9a227"/><stop offset="1" stop-color="#8a6a12"/></linearGradient>
    <linearGradient id="body" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2a2a32"/><stop offset=".4" stop-color="#4a4850"/><stop offset="1" stop-color="#1a1a20"/></linearGradient>
    <linearGradient id="chrome" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset=".5" stop-color="#a8aeb4"/><stop offset="1" stop-color="#6a7078"/></linearGradient>
    <filter id="b"><feGaussianBlur stdDeviation="10"/></filter>'''
    b = f'<rect width="{W}" height="{H}" fill="url(#dusk)"/>'
    b += '<circle cx="1200" cy="200" r="80" fill="#f0d080" opacity=".25"/>'
    # city silhouettes art deco
    for x,hgt in [(40,280),(120,360),(220,240),(340,400),(1480,320),(1380,380)]:
        b += f'<rect x="{x}" y="{520-hgt}" width="70" height="{hgt}" fill="#12121a"/>'
        b += f'<polygon points="{x},{520-hgt} {x+35},{520-hgt-40} {x+70},{520-hgt}" fill="#1a1a28"/>'
    b += '<ellipse cx="800" cy="700" rx="580" ry="24" fill="#000" opacity=".35" filter="url(#b)"/>'
    # streamliner: long teardrop, covered rear, chrome spears
    body='M200,680 C190,620 220,560 300,530 C420,480 700,450 900,445 L1200,450 C1320,460 1400,520 1420,580 L1430,680 Z'
    b += f'<path d="{body}" fill="url(#body)"/>'
    # chrome side spear
    b += '<path d="M320,580 C600,555 1000,550 1380,575" stroke="url(#chrome)" stroke-width="8" fill="none"/>'
    b += '<path d="M320,600 C600,575 1000,570 1380,595" stroke="#c9a227" stroke-width="2" fill="none"/>'
    # cabin
    b += '<path d="M520,530 C600,480 780,460 920,462 L980,520 L540,545 Z" fill="#1a2030" opacity=".9"/>'
    b += '<path d="M540,535 C620,495 780,478 910,480 L950,520 L560,542 Z" fill="#3a5068" opacity=".7"/>'
    # vertical grill art deco
    for i in range(12):
        x=240+i*10; b += f'<line x1="{x}" y1="560" x2="{x}" y2="640" stroke="url(#chrome)" stroke-width="2.5"/>'
    b += '<ellipse cx="250" cy="600" rx="22" ry="18" fill="#f0d080" opacity=".8"/>'
    # covered rear wheel spat
    b += '<path d="M1180,680 C1180,600 1280,580 1360,600 C1400,620 1410,660 1410,680 Z" fill="#2a2a32" stroke="url(#chrome)" stroke-width="3"/>'
    b += wheel(480, 680, 70, "#0d0d10", "#c9a227", "#f0d080")
    b += '<circle cx="1220" cy="680" r="55" fill="#0d0d10" opacity=".5"/>'
    # gold pinstripe on roof
    b += '<path d="M520,470 C700,445 1000,448 1200,470" stroke="#c9a227" stroke-width="3" fill="none"/>'
    render_svg("mb2-1", wrap(W, H, b, d), W, H)

def b_grill():
    W, H = 1000, 750
    d = '''<linearGradient id="ch" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#6a7078"/><stop offset=".5" stop-color="#ffffff"/><stop offset="1" stop-color="#6a7078"/></linearGradient>
    <radialGradient id="amb" cx=".5" cy=".4" r=".7"><stop offset="0" stop-color="#4a2c1a"/><stop offset="1" stop-color="#1a1a2e"/></radialGradient>'''
    b = f'<rect width="{W}" height="{H}" fill="url(#amb)"/>'
    # vertical art deco grille
    b += '<rect x="200" y="80" width="600" height="520" rx="20" fill="#2a2a32" stroke="url(#ch)" stroke-width="10"/>'
    for i in range(18):
        x = 230 + i*30
        b += f'<line x1="{x}" y1="110" x2="{x}" y2="560" stroke="url(#ch)" stroke-width="4"/>'
        if i % 3 == 0: b += f'<line x1="{x}" y1="110" x2="{x}" y2="560" stroke="#c9a227" stroke-width="1.5" stroke-opacity=".6"/>'
    # sunburst badge
    b += '<circle cx="500" cy="300" r="70" fill="#1a1a20" stroke="#c9a227" stroke-width="4"/>'
    for i in range(16):
        a = math.radians(i*22.5); b += f'<line x1="{500+25*math.cos(a):.1f}" y1="{300+25*math.sin(a):.1f}" x2="{500+60*math.cos(a):.1f}" y2="{300+60*math.sin(a):.1f}" stroke="#f0d080" stroke-width="2"/>'
    b += '<circle cx="500" cy="300" r="18" fill="#c9a227"/>'
    b += '<rect x="350" y="620" width="300" height="40" rx="4" fill="#c9a227" opacity=".85"/>'
    render_svg("mb2-2", wrap(W, H, b, d), W, H)

def b_interior():
    W, H = 1000, 750
    d = '''<linearGradient id="fan" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a3040"/><stop offset="1" stop-color="#1a1a28"/></linearGradient>
    <linearGradient id="wood" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6b4423"/><stop offset="1" stop-color="#3d2410"/></linearGradient>'''
    b = f'<rect width="{W}" height="{H}" fill="url(#fan)"/>'
    # fan-shaped dash
    b += '<path d="M100,400 Q500,80 900,400 L900,480 L100,480 Z" fill="#2a2430" stroke="#c9a227" stroke-width="3"/>'
    for i in range(9):
        x = 180 + i*80
        b += f'<line x1="500" y1="200" x2="{x}" y2="400" stroke="#c9a227" stroke-opacity=".35" stroke-width="2"/>'
    b += '<rect x="120" y="420" width="760" height="50" rx="6" fill="url(#wood)"/>'
    for i in range(15): b += f'<line x1="{140+i*50}" y1="425" x2="{140+i*50}" y2="465" stroke="#8a6238" stroke-opacity=".5" stroke-width="2"/>'
    # ivory gauges
    for cx in (300, 500, 700):
        b += f'<circle cx="{cx}" cy="340" r="42" fill="#f5f0e6" stroke="#c9a227" stroke-width="5"/>'
        b += f'<line x1="{cx}" y1="340" x2="{cx+15}" y2="315" stroke="#8a1a1a" stroke-width="3"/>'
    b += '<circle cx="500" cy="580" r="110" fill="none" stroke="#c9a227" stroke-width="10"/>'
    b += '<circle cx="500" cy="580" r="110" fill="none" stroke="#f0d080" stroke-width="3" stroke-dasharray="20 15"/>'
    b += '<rect x="200" y="640" width="600" height="80" rx="8" fill="#3d2410"/>'
    render_svg("mb2-3", wrap(W, H, b, d), W, H)

def lacquer_texture(name, w=1000, h=750):
    y, x = np.mgrid[0:h, 0:w].astype(float)
    base = np.zeros((h, w, 3))
    # deep black-burgundy lacquer
    base[..., 0] = 28 + 8*np.sin(x*0.01)
    base[..., 1] = 18 + 5*np.sin(y*0.008)
    base[..., 2] = 32 + 10*np.cos(x*0.006)
    # gold dust flecks
    flecks = rng.random((h, w)) > 0.997
    base[flecks] = [240, 208, 128]
    # soft reflection band
    band = np.exp(-((y - h*0.35)/80)**2) * 40
    base[..., 0] = np.clip(base[..., 0] + band, 0, 255)
    base[..., 1] = np.clip(base[..., 1] + band*0.8, 0, 255)
    base[..., 2] = np.clip(base[..., 2] + band*0.5, 0, 255)
    im = Image.fromarray(base.astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))
    save(name, im)

if __name__ == "__main__":
    a_hero(); a_deck(); a_detail(); sailcloth_texture("mb1-4")
    b_hero(); b_grill(); b_interior(); lacquer_texture("mb2-4")
    print("done")
