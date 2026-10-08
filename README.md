# Car Design Daily · 汽車設計日報

每日一期的靜態網頁：全球汽車設計新聞＋汽車新知＋隨機情緒板（zh-TW）。

- 線上（永久）：https://feeling00480-commits.github.io/car-design-daily/ （GitHub Pages，repo `feeling00480-commits/car-design-daily`，branch `main`、root）
- 每期固定網址：`/issues/YYYY-MM-DD/`；首頁 `/` = 最新一期；`/archive/` = 往期列表

## 結構
```
index.html                  ← build.py 產生（最新一期）
archive/index.html          ← build.py 產生
assets/style.css            ← 共用樣式（深淺色、RWD、CJK 字體）
issues/YYYY-MM-DD/
  data.json                 ← 唯一需要手寫的內容檔
  img/*.webp                ← 情緒板圖像（≤1400px WebP）
  index.html                ← build.py 產生
tools/
  build.py                  ← data.json → HTML
  publish.sh                ← build + git commit + push main（GitHub Pages 自動重新部署）
  publish-flypod.sh         ← 已棄用的 flypod 備案
  pick_themes.py, themes.json ← 隨機主題（避開近 10 期）
  moodart.py                ← 程式生成情緒板插畫／材質（無 AI 生圖工具時的備案）
  genimg.py                 ← AI 生圖腳本（Pollinations；目前匿名呼叫回 402 需付費，已停用）
```

## 產生下一期（每日流程）
1. **蒐集設計新聞（5–8 則，近 24–72 小時）**：用 WebSearch/WebFetch 實際讀過原文才收錄；不得杜撰日期、引言。
   每則：品牌、標籤、日期、中文標題、原文標題、2–3 句摘要、3–5 點設計解析（比例／燈號／面處理／CMF／室內 UX／品牌方向）、來源連結。
   - **每則設計新聞都必須有 1 張代表圖（必要步驟）**：
     1. 優先用車廠官方新聞室／press kit 圖片（BMW PressClub、JLR Media、VW Newsroom、Renault/Alpine Media、Hyundai Newsroom、Porsche Newsroom…）；找不到才用來源報導的 `og:image`。
        取得方式：`curl -sL -A "<瀏覽器 UA>" <URL> | grep -o -i -E '<meta[^>]*og:image[^>]*>'`，必要時在頁面 HTML 中找較大尺寸的圖。
     2. 必須確認圖片就是該車款（開圖檢查）；**不可用不相符的圖，也不可用 AI 生成圖代表真實車款**。若找不到合適圖片，該則不放圖，並在回報中註明。
     3. 裁成 16:9、縮成 1600×900 WebP（q≈82，<300KB），存成 `issues/<date>/img/news-<id>.webp`。
     4. 在 data.json 該則加入 `"image": {"file": "news-<id>.webp", "alt": "<中文描述>", "credit": "<來源名稱，如 BMW Group PressClub>", "credit_url": "<來源頁面>"}`。
        build.py 會把圖片放在卡片最上方（object-fit: cover、lazy loading、alt），並顯示「圖片來源：…」連結；首則卡片的圖也會用作 og:image。
2. **汽車新知（3–5 則）**：EV、電池、自駕、法規、製造、市場；摘要＋連結。另寫一則「今日設計名詞」（盡量和當期新聞呼應）。
3. **情緒板（1–2 組）**：`python3 tools/pick_themes.py 2` 抽主題 → 每組 4–6 張原創虛構圖（不可出現真實車款或 logo）＋6 色 hex 色票、關鍵字、材質筆記。
   - 有 GenerateImage 等生圖工具時優先使用，輸出後轉 WebP（≤1400px、q≈80）放 `issues/<date>/img/`，命名 `mb1-1…`、`mb2-1…`，每組第一張為 hero（16:9），其餘 4:3。
   - 沒有時用 `tools/moodart.py` 的做法（SVG 插畫＋numpy 材質）為新主題寫對應函式。
4. 複製前一期 `data.json` 為模板，填入新內容（`issue_no` +1、`date`、`weekday`、`lede`）。
5. 發佈：在 `/workspace/car-design-daily` 執行 `./tools/publish.sh "Issue 00N · YYYY-MM-DD"`
   （= `python3 tools/build.py --site-url "$(cat .site-url)"` → `git add -A` → `git commit` → `git push origin main`）。
   GitHub Pages 約 1–2 分鐘重新部署（可用 `gh api repos/feeling00480-commits/car-design-daily/pages/builds/latest` 查狀態）。
   之後用 WebFetch／curl 驗證 `https://feeling00480-commits.github.io/car-design-daily/`、`/issues/<date>/`、`/archive/` 以及所有新聞圖與情緒板圖片都回 200。
   - 所有站內連結必須是相對路徑（站點位於子路徑 `/car-design-daily/`）；og:image／canonical 用 `.site-url` 產生絕對網址。
6. 預覽圖：`google-chrome --headless=new --no-sandbox --window-size=1280,2400 --screenshot=preview.png <URL>`

## 新聞來源清單
- 設計專業：Car Design News、Interior Motives、Auto&Design（義）、Dezeen、Designboom、Design Week、Wallpaper*、Yanko Design
- 綜合車媒：Autocar、Top Gear、Motor1、Carscoops、Car and Driver、Road & Track、CAR Magazine、Octane、autoevolution
- 科技／EV：The Verge、Electrek、InsideEVs、electrive、WIRED
- 亞洲：Chosun Biz、Digital Today（韓）、Car Watch／Response（日）、汽车之家／懂车帝（中）、Yahoo 汽車／U-CAR／8891（台）
- 原廠新聞室：JLR、BMW PressClub、Renault、Stellantis、Alpine、Porsche Newsroom、Hyundai Newsroom 等
- 產業：Reuters、Automotive News、just-auto、Insurance Journal

## 主題池
見 `tools/themes.json`（Brutalist off-roader、Japanese retro-futurism 1980s、Scandinavian calm interior、Desert rally pastel、Art Deco streamliner、Kyoto craft & washi interior…），可自由增補。

## 託管
- **正式**：GitHub Pages（`main` / root，含 `.nojekyll`），push 即更新，網址永久。gh CLI 已在本機以 `feeling00480-commits` 登入。
- **已棄用備案**：flypod 匿名部署 https://2b80368e7d1741c6.flypod.page（2026-10-22 到期；`tools/publish-flypod.sh`）。更新權杖在本機 `~/.config/flypod/`，絕不可 commit。
