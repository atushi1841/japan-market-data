#!/usr/bin/env python3
"""
Example: Query Japan Market MCP Server (locally)
=================================================
This demonstrates calling the japan-market-mcp server via stdio transport.
Install: npm install -g io.github.atushi1841.japan-market-data
"""

import subprocess
import json
import sys

MCP_SERVER = "japan-market-mcp"

# Example: Search Mercari Japan listings
def search_mercari(query: str, limit: int = 10):
    """Call the MCP server's mercari_search tool."""
    tool_call = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "mercari_search",
            "arguments": {"query": query, "limit": limit},
        },
    }
    proc = subprocess.run(
        ["npx", "-y", "@atushi1841/japan-market-mcp"],
        input=json.dumps(tool_call) + "\n",
        capture_output=True,
        text=True,
        timeout=60,
    )
    return json.loads(proc.stdout.strip()) if proc.stdout.strip() else None


if __name__ == "__main__":
    result = search_mercari("PlayStation 5", limit=5)
    if result:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("MCP server not running. Install: npm install -g @atushi1841/japan-market-mcp")
