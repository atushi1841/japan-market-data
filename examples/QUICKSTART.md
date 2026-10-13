# Quick Start — Japan Market Data

Get Japanese market data in seconds. No API key, no sign-up — just pick an actor and run.

## For AI Agents (MCP)

```bash
# Install the MCP bundle
npm install -g @atushi1841/japan-market-mcp

# Add to claude_desktop_config.json or .mcp.json
{
  "mcpServers": {
    "japan-market": {
      "command": "npx",
      "args": ["-y", "@atushi1841/japan-market-mcp"]
    }
  }
}
```

## For Python

```bash
pip install apify-client
```

```python
from apify_client import ApifyClient

client = ApifyClient("YOUR_APIFY_TOKEN")  # free tier: 1M credits/month
run = client.actor("atushi1841/mercari-japan-search-scraper").call({
    "searchQuery": "anime figure",
    "maxResults": 50
})
data = run["data"]["items"]
```

## For Node.js

```bash
npm install apify-client
```

```js
const { ApifyClient } = require("apify-client");
const client = new ApifyClient("YOUR_TOKEN");
const run = await client.actor("atushi1841/mercari-japan-search-scraper").call({
  searchQuery: "sneakers",
  maxResults: 30
});
```

## Top Actors by Use Case

| Use Case | Actor | Input |
|----------|-------|-------|
| Mercari Japan | `mercari-japan-search-scraper` | `searchQuery`, `maxResults` |
| Yahoo Auctions JP | `yahoo-auctions-japan-scraper` | `keyword`, `maxResults` |
| Rakuten Ichiba | `rakuten-market-scraper` | `searchTerm`, `maxResults` |
| DLsite (doujin) | `dlsite-scraper` | `category`, `maxResults` |
| Anime Figures | `japan-anime-figure-price-data` | `title`, `condition` |
| Property Prices (MLIT) | `mlit-japan-property-prices` | `prefecture`, `year` |
| Cameras (Used) | `japan-used-camera-market-scraper` | `brand`, `model` |
| Weather (JMA) | `japan-jma-weather` | `city`, `forecastDays` |

## Data Output Format

All actors return structured JSON:

```json
{
  "title": "【美品】Figma 魔獣探偵ケサラン・サツラン",
  "price": 8500,
  "currency": "JPY",
  "url": "https://jp.mercari.com/item/m12345",
  "seller": "user123",
  "condition": "new",
  "images": ["https://..."],
  "scraped_at": "2026-10-17T00:00:00Z"
}
```

## Full Catalog

See [README.md](../README.md) for the complete list of 55 actors with descriptions, run counts, and Apify Store links.

[MCP Registry](https://registry.modelcontextprotocol.io) · [Apify Store](https://apify.com/fruitful_quintessence)
