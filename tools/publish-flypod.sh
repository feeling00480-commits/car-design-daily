#!/usr/bin/env bash
# DEPRECATED fallback: anonymous flypod deploy (expires 14 days after creation unless `npx flypod login`).
set -euo pipefail
cd "$(dirname "$0")/.."
python3 tools/build.py --site-url "https://2b80368e7d1741c6.flypod.page"
rm -rf public && mkdir -p public
cp -r index.html assets archive .nojekyll public/
mkdir -p public/issues && for d in issues/*/; do n=$(basename "$d"); mkdir -p "public/issues/$n"; cp -r "$d/index.html" "$d/img" "$d/data.json" "public/issues/$n/"; done
cd public && npx -y flypod update .
cd .. && python3 tools/build.py --site-url "$(cat .site-url)"   # restore GitHub Pages URLs
