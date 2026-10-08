#!/usr/bin/env python3
"""Pick N random mood-board themes, avoiding ones used in the last 10 issues. Usage: pick_themes.py [N]"""
import json, glob, os, random, sys
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pool = json.load(open(f"{R}/tools/themes.json"))
used = []
for p in sorted(glob.glob(f"{R}/issues/*/data.json"))[-10:]:
    used += [b["theme"] for b in json.load(open(p))["moodboards"]]
cand = [t for t in pool if t not in used] or pool
print(json.dumps(random.sample(cand, int(sys.argv[1]) if len(sys.argv) > 1 else 2), ensure_ascii=False))
