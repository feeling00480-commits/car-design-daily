#!/usr/bin/env python3
"""Mood boards for 2026-10-11: Italian 1970s wedge supercar / Martian terraformer rover."""
import sys, os, subprocess, math, numpy as np
from PIL import Image, ImageFilter, ImageDraw
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
TMP = "/tmp/moodart1011"; os.makedirs(TMP, exist_ok=True)
rng = np.random.default_rng(20261011)

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
            a = math.radians(i*72-90)
            s += f'<line x1="{cx}" y1="{cy}" x2="{cx+r*.5*math.cos(a):.1f}" y2="{cy+r*.5*math.sin(a):.1f}" stroke="{accent}" stroke-width="3"/>'
    return s + f'<circle cx="{cx}" cy="{cy}" r="{r*.12}" fill="{tyre}"/>'

# ---------- A: Italian 1970s wedge ----------
def a_hero():
    W, H = 1600, 900
    d = '''<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1a2744"/><stop offset=".55" stop-color="#4a3a50"/><stop offset="1" stop-color="#c47b5a"/></linearGradient>
    <linearGradient id="body" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff7a2e"/><stop offset="1" stop-color="#b33a00"/></linearGradient>
    <linearGradient id="road" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4a4a4a"/><stop offset="1" stop-color="#2b2b2b"/></linearGradient>
    <filter id="b"><feGaussianBlur stdDeviation="8"/></filter>'''
    b = f'<rect width="{W}" height="{H}" fill="url(#sky)"/>'
    # concrete blocks
    for x,hgt in [(80,180),(200,240),(1400,200),(1500,260)]:
        b += f'<rect x="{x}" y="{520-hgt}" width="60" height="{hgt}" fill="#3a3a42" opacity=".7"/>'
    b += f'<rect y="620" width="{W}" height="280" fill="url(#road)"/>'
    b += '<ellipse cx="820" cy="700" rx="520" ry="20" fill="#000" opacity=".25" filter="url(#b)"/>'
    # wedge: ultra low nose, flat belt, chopped tail
    body='M180,700 L220,560 L520,500 L1100,495 L1280,530 L1320,700 Z'
    b += f'<path d="{body}" fill="url(#body)"/>'
    b += '<path d="M220,560 L520,500 L900,498 L880,560 Z" fill="#1a1a1a" opacity=".85"/>'  # canopy
    b += '<path d="M240,555 L500,510 L860,508 L840,548 Z" fill="#3a5068" opacity=".55"/>'
    # pop-up seam
    b += '<rect x="260" y="545" width="70" height="10" rx="2" fill="#2b2b2b"/>'
    b += '<rect x="360" y="542" width="70" height="10" rx="2" fill="#2b2b2b"/>'
    # belt line
    b += '<path d="M230,580 L1280,560" stroke="#1a1a1a" stroke-width="5" fill="none"/>'
    # NACA / side intake
    b += '<path d="M980,560 L1080,555 L1100,620 L1000,625 Z" fill="#1a1a1a"/>'
    b += '<rect x="200" y="680" width="1100" height="22" fill="#1a1a1a"/>'  # black sill
    b += wheel(420, 700, 62, "#1d252b", "#c5c8cc", "#e85d04") + wheel(1120, 700, 66, "#1d252b", "#c5c8cc", "#e85d04")
    b += '<rect x="1260" y="600" width="40" height="14" rx="2" fill="#f4a261"/>'
    render_svg("mb1-1", wrap(W, H, b, d), W, H)

def a_cockpit():
    W, H = 1000, 750
    d = '''<linearGradient id="dash" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2b2b2b"/><stop offset="1" stop-color="#1a1a1a"/></linearGradient>'''
    b = f'<rect width="{W}" height="{H}" fill="#1a2744"/>'
    b += '<path d="M0,80 L1000,80 L1000,280 L0,320 Z" fill="#3a4558"/>'
    b += '<path d="M0,280 L1000,250 L1000,420 L0,450 Z" fill="url(#dash)"/>'
    # single binnacle
    b += '<circle cx="500" cy="340" r="90" fill="#0d0d10" stroke="#c5c8cc" stroke-width="8"/>'
    b += '<circle cx="500" cy="340" r="70" fill="#e8e4dc"/>'
    for i in range(12):
        a=math.radians(-120+i*20)
        b += f'<line x1="{500+50*math.cos(a):.1f}" y1="{340+50*math.sin(a):.1f}" x2="{500+62*math.cos(a):.1f}" y2="{340+62*math.sin(a):.1f}" stroke="#1a1a1a" stroke-width="2"/>'
    b += '<line x1="500" y1="340" x2="530" y2="290" stroke="#e85d04" stroke-width="3"/>'
    # suede wheel
    b += '<circle cx="500" cy="560" r="120" fill="none" stroke="#a67c52" stroke-width="18"/>'
    b += '<circle cx="500" cy="560" r="120" fill="none" stroke="#2b2b2b" stroke-width="4"/>'
    b += '<rect x="455" y="520" width="90" height="50" rx="6" fill="#c5c8cc"/>'
    # exposed gate
    b += '<rect x="720" y="480" width="160" height="200" rx="8" fill="#2b2b2b"/>'
    for y in (520,560,600,640):
        b += f'<line x1="750" y1="{y}" x2="850" y2="{y}" stroke="#c5c8cc" stroke-width="3"/>'
    b += '<circle cx="800" cy="560" r="10" fill="#e85d04"/>'
    render_svg("mb1-2", wrap(W, H, b, d), W, H)

def a_detail():
    W, H = 1000, 750
    b = f'<rect width="{W}" height="{H}" fill="#2b2b2b"/>'
    # wedge section lines
    b += '<path d="M100,600 L200,200 L800,180 L900,600 Z" fill="none" stroke="#e85d04" stroke-width="3"/>'
    b += '<path d="M200,200 L400,350 L800,180" fill="none" stroke="#c5c8cc" stroke-width="2" stroke-dasharray="6 4"/>'
    # harness buckle
    b += '<rect x="420" y="400" width="160" height="100" rx="10" fill="#c5c8cc"/>'
    b += '<rect x="450" y="430" width="100" height="40" rx="4" fill="#1a1a1a"/>'
    b += '<path d="M480,450 L520,450 M500,430 L500,470" stroke="#e85d04" stroke-width="4"/>'
    # mesh intake
    for i in range(8):
        for j in range(5):
            b += f'<circle cx="{120+i*40}" cy="{500+j*35}" r="8" fill="none" stroke="#a67c52" stroke-width="2"/>'
    render_svg("mb1-3", wrap(W, H, b), W, H)

def orange_lacquer(name, w=1000, h=750):
    y, x = np.mgrid[0:h, 0:w].astype(float)
    base = np.zeros((h, w, 3))
    base[..., 0] = 220 + 20*np.sin(x*0.008)
    base[..., 1] = 80 + 15*np.sin(y*0.01)
    base[..., 2] = 10 + 8*np.cos(x*0.006)
    # orange peel micro noise
    noise = rng.normal(0, 6, (h, w, 3))
    base = np.clip(base + noise, 0, 255)
    band = np.exp(-((y - h*0.4)/100)**2) * 35
    base[..., 0] = np.clip(base[..., 0] + band, 0, 255)
    base[..., 1] = np.clip(base[..., 1] + band*0.5, 0, 255)
    im = Image.fromarray(base.astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8))
    save(name, im)

# ---------- B: Martian terraformer rover ----------
def b_hero():
    W, H = 1600, 900
    d = '''<linearGradient id="mars" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a1810"/><stop offset=".45" stop-color="#8b3a2a"/><stop offset="1" stop-color="#c47b5a"/></linearGradient>
    <linearGradient id="hull" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e8e4dc"/><stop offset="1" stop-color="#6e7f8a"/></linearGradient>
    <filter id="b"><feGaussianBlur stdDeviation="10"/></filter>'''
    b = f'<rect width="{W}" height="{H}" fill="url(#mars)"/>'
    b += '<circle cx="300" cy="160" r="40" fill="#e9c46a" opacity=".9"/>'
    # dunes
    b += '<path d="M0,520 Q400,460 800,530 T1600,500 L1600,900 L0,900 Z" fill="#8b3a2a"/>'
    b += '<path d="M0,600 Q500,560 1000,620 T1600,580 L1600,900 L0,900 Z" fill="#6a2e22" opacity=".85"/>'
    b += '<ellipse cx="850" cy="680" rx="480" ry="28" fill="#000" opacity=".3" filter="url(#b)"/>'
    # rover body
    b += '<rect x="480" y="420" width="520" height="200" rx="30" fill="url(#hull)"/>'
    b += '<rect x="560" y="360" width="360" height="100" rx="40" fill="#e8e4dc" stroke="#6e7f8a" stroke-width="4"/>'  # pressure cabin
    b += '<circle cx="640" cy="410" r="28" fill="#3a6b8a" opacity=".7"/><circle cx="760" cy="410" r="28" fill="#3a6b8a" opacity=".7"/>'
    # solar wings
    b += '<rect x="200" y="480" width="280" height="50" rx="6" fill="#3a6b8a" opacity=".85"/>'
    b += '<rect x="1000" y="470" width="300" height="50" rx="6" fill="#3a6b8a" opacity=".85"/>'
    for i in range(6):
        b += f'<line x1="{220+i*40}" y1="485" x2="{220+i*40}" y2="525" stroke="#e9c46a" stroke-width="2" opacity=".5"/>'
        b += f'<line x1="{1020+i*40}" y1="475" x2="{1020+i*40}" y2="515" stroke="#e9c46a" stroke-width="2" opacity=".5"/>'
    # tool arm
    b += '<path d="M980,450 L1120,380 L1180,420" fill="none" stroke="#6e7f8a" stroke-width="10" stroke-linecap="round"/>'
    b += '<rect x="1160" y="410" width="40" height="24" rx="4" fill="#e9c46a"/>'
    # six wheels
    for cx in (520, 740, 960):
        b += wheel(cx, 650, 48, "#2b2b2b", "#6e7f8a", "#e9c46a")
        b += f'<line x1="{cx}" y1="620" x2="{cx}" y2="520" stroke="#6e7f8a" stroke-width="8"/>'
    render_svg("mb2-1", wrap(W, H, b, d), W, H)

def b_cabin():
    W, H = 1000, 750
    d = '''<radialGradient id="g" cx=".5" cy=".4" r=".7"><stop offset="0" stop-color="#4a5560"/><stop offset="1" stop-color="#1a2028"/></radialGradient>'''
    b = f'<rect width="{W}" height="{H}" fill="url(#g)"/>'
    b += '<circle cx="500" cy="280" r="140" fill="#1a2744" stroke="#e8e4dc" stroke-width="12"/>'
    b += '<circle cx="500" cy="280" r="110" fill="#c47b5a" opacity=".4"/>'
    # gauges
    for cx in (220, 500, 780):
        b += f'<circle cx="{cx}" cy="520" r="55" fill="#e8e4dc" stroke="#6e7f8a" stroke-width="6"/>'
        b += f'<line x1="{cx}" y1="520" x2="{cx+25}" y2="490" stroke="#8b3a2a" stroke-width="3"/>'
    b += '<rect x="150" y="620" width="700" height="80" rx="12" fill="#6e7f8a"/>'
    b += '<rect x="180" y="640" width="200" height="40" rx="6" fill="#e9c46a"/>'
    b += '<rect x="420" y="640" width="200" height="40" rx="6" fill="#3a6b8a"/>'
    render_svg("mb2-2", wrap(W, H, b, d), W, H)

def b_joint():
    W, H = 1000, 750
    b = f'<rect width="{W}" height="{H}" fill="#3a2a22"/>'
    # sealed joint
    b += '<circle cx="500" cy="380" r="160" fill="none" stroke="#6e7f8a" stroke-width="28"/>'
    b += '<circle cx="500" cy="380" r="160" fill="none" stroke="#e8e4dc" stroke-width="6"/>'
    for i in range(16):
        a=math.radians(i*22.5)
        b += f'<circle cx="{500+160*math.cos(a):.1f}" cy="{380+160*math.sin(a):.1f}" r="8" fill="#e9c46a"/>'
    # bellows
    for i in range(7):
        y=560+i*18
        b += f'<ellipse cx="500" cy="{y}" rx="{120-i*8}" ry="10" fill="none" stroke="#c47b5a" stroke-width="4"/>'
    # tool latch
    b += '<rect x="700" y="200" width="180" height="120" rx="10" fill="#6e7f8a"/>'
    b += '<rect x="730" y="230" width="120" height="60" rx="6" fill="#1a2028"/>'
    b += '<circle cx="790" cy="260" r="16" fill="#e9c46a"/>'
    render_svg("mb2-3", wrap(W, H, b), W, H)

def dust_texture(name, w=1000, h=750):
    y, x = np.mgrid[0:h, 0:w].astype(float)
    base = np.zeros((h, w, 3))
    base[..., 0] = 140 + 30*np.sin(x*0.02) + 20*np.cos(y*0.015)
    base[..., 1] = 70 + 15*np.sin(y*0.02)
    base[..., 2] = 45 + 10*np.cos(x*0.01)
    # dust grains
    grains = rng.random((h, w)) > 0.992
    base[grains] = [232, 228, 220]
    # titanium sheen band
    band = np.exp(-((y - h*0.3)/90)**2) * 40
    base[..., 0] = np.clip(base[..., 0] + band*0.4, 0, 255)
    base[..., 1] = np.clip(base[..., 1] + band*0.6, 0, 255)
    base[..., 2] = np.clip(base[..., 2] + band*0.7, 0, 255)
    im = Image.fromarray(base.astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.0))
    save(name, im)

if __name__ == "__main__":
    a_hero(); a_cockpit(); a_detail(); orange_lacquer("mb1-4")
    b_hero(); b_cabin(); b_joint(); dust_texture("mb2-4")
    print("done")
