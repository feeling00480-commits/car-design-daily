#!/usr/bin/env python3
"""Generate mood board images via Pollinations (no-key public API) and optimize to WebP.
Usage: genimg.py <outdir> <prompts.json>   prompts.json: [{"name":"mb1-1","prompt":"...","seed":1}, ...]"""
import json, sys, os, urllib.parse, urllib.request, io, time
from PIL import Image
out, pj = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
NEG = ", original fictional design, no logos, no badges, no text, no watermark"
for it in json.load(open(pj)):
    dst = os.path.join(out, it["name"] + ".webp")
    if os.path.exists(dst): continue
    w, h = it.get("w", 1024), it.get("h", 768)
    url = "https://image.pollinations.ai/prompt/" + urllib.parse.quote(it["prompt"] + NEG) + f"?width={w}&height={h}&nologo=true&seed={it.get('seed',1)}&model=flux"
    for attempt in range(4):
        try:
            data = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent":"car-design-daily"}), timeout=180).read()
            im = Image.open(io.BytesIO(data)).convert("RGB")
            im.thumbnail((1200, 1200))
            im.save(dst, "WEBP", quality=80, method=6)
            print("ok", dst, im.size, os.path.getsize(dst)); break
        except Exception as e:
            print("retry", it["name"], e); time.sleep(5 + attempt*5)
