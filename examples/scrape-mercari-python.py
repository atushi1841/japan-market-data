#!/usr/bin/env python3
"""
Example: Scrape Mercari Japan with Apify
========================================
Run this actor via the Apify API (no credentials needed for free actors).
Replace ACTOR_NAME and API_TOKEN as needed.
"""

import json
import os
import urllib.request

# --- Option 1: Run via Apify API (requires API token) ------------------------
# pip install apify-client
# from apify_client import ApifyClient

# client = ApifyClient(os.environ["APIFY_API_TOKEN"])
# run = client.actor("atushi1841/mercari-japan-search-scraper").call(
#     run_input={"searchQuery": "iPhone 15", "maxResults": 50}
# )
# results = run["data"]["items"]
# print(json.dumps(results[:3], ensure_ascii=False, indent=2))


# --- Option 2: Use via HTTP directly (no SDK) --------------------------------
ACTOR_HANDLE = "mercari-japan-search-scraper"
APIFY_API_TOKEN = os.environ.get("APIFY_API_TOKEN", "")

if APIFY_API_TOKEN:
    url = f"https://api.apify.com/v2/acts/{ACTOR_HANDLE}/runs"
    payload = json.dumps({
        "searchQuery": "anime figure",
        "maxResults": 20,
        "waitUntilDone": False,
    }).encode()
    req = urllib.request.Request(url, data=payload, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("Authorization", f"Bearer {APIFY_API_TOKEN}")
    with urllib.request.urlopen(req, timeout=30) as r:
        resp = json.loads(r.read())
        run_id = resp["data"]["id"]
        print(f"Run started: {run_id}")
        # Poll for results...
else:
    print("Set APIFY_API_TOKEN to run. Free actors can also be run at:")
    print(f"https://apify.com/atushi1841/{ACTOR_HANDLE}")
