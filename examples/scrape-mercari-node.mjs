#!/usr/bin/env node
/**
 * Example: Get Mercari Japan price data via Apify
 * ================================================
 * Prerequisites: APIFY_API_TOKEN env var
 * npm install apify-client
 */

const { ApifyClient } = require("apify-client");

async function main() {
  const client = new ApifyClient({ token: process.env.APIFY_API_TOKEN });

  const run = await client
    .actor("atushi1841/mercari-japan-search-scraper")
    .call({
      searchQuery: "fujifilm x-series",
      maxResults: 30,
    });

  // Stream results
  const dataset = await client.dataset(run.defaultDatasetId).listItems();
  console.log(`Got ${dataset.items.length} results`);
  console.log(JSON.stringify(dataset.items[0], null, 2));
}

main().catch(console.error);
