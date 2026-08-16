# Reddit / Community Outreach Templates

## 原則
- 売り込まない。値(方法論・作り方)を先に提供し、リンクは「補足資料」として自然に添える。
- 自己宣伝はRATIOを守る: 過去コメント/投稿の ~9割が純価値提供、1割が自リンク。
- 各サブレの自己宣伝ルールを必ず読んでから投稿。多くは「ブログ直リンク」より「ガイド本文+コメント/プロフィールリンク」が安全。
- 新規アカウントで一気に複数サブレ投稿しない(スパム判定)。間隔を開ける。

## ターゲット別テンプレ

### A. r/AnimeFigures — Mandarake価格監視
投稿形式: テキスト投稿(ガイド本文を書く)。本文中に自リンク1つ程度。
```
[Question] How do you track Mandarake price drops for hard-to-find figures?

I keep losing out on figures because hot items sell within minutes, and
checking my watchlist (maybe 60 search terms) by hand is impossible.

I ended up pulling Mandarake listing data once or twice a day into a tiny
script that only pings me when a price crosses a threshold or a NEW listing
appears for a term I follow. Historical price rows let me eyeball "is this
a good price?" before committing.

The data side I do with the Apify Mandarake scraper
(https://atushi1841.github.io/japan-market-data/blog/mandarake-price-tracking.html)
because it returns clean JSON instead of fighting the site's JS.

Curious how you all handle watchlists — do you use alerts, 3rd-party
surrogate services, or just brute-force refresh?
```
追記: 純質問として開き、ディスカッションに。決して「買え」とは書かない。

### B. r/doujinshi または DLsite関連コミュニティ — DLsite価格/売上調査
```
Creator-friendly: tracking price/sales trends across DLsite's catalog

Quick share for people thinking about their next work's price point: I put
together a small way to pull DLsite title metadata (RJ number, circle,
genre, price, rating, release date) programmatically instead of clicking
through search results.

Useful for: seeing what genres/price brackets actually move, watching your
own-ish competitors' pricing, or building a personal title database.

More here: https://atushi1841.github.io/japan-market-data/blog/dlsite-price-tracking.html
(This is a guide, not a paywall thing — metadata is free to collect.)
```
注意: 成人コンテンツの規約 — 作品本体の再配布でなくメタデータ収集である旨を表記。

### C. 車輸出コミュニティ(r/importexport, Facebook輸出商サークル) — goo-net在庫データ
```
Importing Japanese used cars? Automating goo-net inventory changed my sourcing.

If you import from Japan, you know the game is speed: the right model at the
right price disappears fast. I run a daily scrape of goo-net nationwide
inventory into a CSV, filter by my target models/mileage/price, and only
look at what's NEW vs yesterday.

Guide + how to set it up: https://atushi1841.github.io/japan-market-data/blog/goo-net-used-car-export-data.html
No dealer/owner PII in the dataset — just vehicle + price + location, which
is all you need for sourcing.
```

### D. AI/開発者コミュニティ( r/selfhosted, r/webdev, HN, X) — MCP/AIエージェント向け
``` 
Japan market data now callable from Claude / Cursor via MCP

Quick dev note: several of these Japan resale-market scrapers are exposed
as MCP servers, so an AI agent can query Mandarake auctions, goo-net used
cars, or camera/watch/collectible prices as a tool call and get JSON back.
Nice for building price-monitoring or market-research agents that speak to
Japanese marketplaces.

Landing with the full list: https://atushi1841.github.io/japan-market-data/
```

## 投稿頻度ガード
- 1日1投稿まで。サブレごとに少なくとも数日開ける。
- アカウントが新規なら、まずは純コメントで評判を積んでから投稿開始。
- 各投稿の最後に「More concrete guide here: <ページ>」形式で自ページ1件のみ。

## 効果判定
- URL短縮(bit.ly/rar 等)を使わず、GitHub Pagesの素のURLをベースに。UTM付けるとスパム判定UP。
- 週1で github.io/japan-market-data/ へのアクセス数の他、Apify各アクターの u30d(totalUsers30Days) が1→複数に動くかで判定。動きが出たサブレ/記事を増やす。
