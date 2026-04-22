#!/usr/bin/env python3
"""BEKO Skill #2: Search - Web search capability"""

import json
import requests
from pathlib import Path
from typing import Dict, Any, List
from urllib.parse import quote


class SearchSkill:
    def __init__(self, base_path: str = "."):
        self.cache_path = Path(base_path) / "memory/search_cache.json"

    def duckduckgo_search(
        self, query: str, max_results: int = 5
    ) -> List[Dict[str, str]]:
        """DuckDuckGo instant answer search (no API key)"""
        try:
            url = f"https://api.duckduckgo.com/?q={quote(query)}&format=json&no_html=1&skip_disambig=1"
            resp = requests.get(url, timeout=10)
            data = resp.json()

            results = []
            if data.get("AbstractText"):
                results.append(
                    {"title": "Summary", "url": "", "snippet": data["AbstractText"]}
                )

            related = data.get("RelatedTopics", [])
            for item in related[:max_results]:
                if "Text" in item and "FirstURL" in item:
                    results.append(
                        {
                            "title": item.get("Name", "N/A"),
                            "url": item["FirstURL"],
                            "snippet": item["Text"][:200],
                        }
                    )
            return results
        except Exception as e:
            return [{"error": str(e)}]

    def save_cache(self, query: str, results: List[Dict]):
        """Cache results"""
        cache = self.load_cache()
        cache[query] = {"results": results, "timestamp": str(Path().stat().st_mtime)}
        self.cache_path.parent.mkdir(exist_ok=True)
        with open(self.cache_path, "w") as f:
            json.dump(cache, f, indent=2)

    def load_cache(self) -> Dict:
        if self.cache_path.exists():
            with open(self.cache_path) as f:
                return json.load(f)
        return {}

    def search(self, query: str, use_cache: bool = True) -> List[Dict[str, str]]:
        cache = self.load_cache()
        if use_cache and query in cache:
            return cache[query]["results"]

        results = self.duckduckgo_search(query)
        self.save_cache(query, results)
        return results

    def run_skill(self, params: Dict[str, Any]) -> Dict[str, Any]:
        action = params.get("action", "search")
        if action == "search":
            query = params.get("query", "BEKO AI")
            results = self.search(query, params.get("cache", True))
            return {"status": "searched", "query": query, "results": results[:5]}
        elif action == "cache":
            return {"status": "cache", "data": self.load_cache()}
        return {"error": "action: search|cache"}


if __name__ == "__main__":
    ss = SearchSkill()
    print(
        json.dumps(
            ss.run_skill({"action": "search", "query": "self-improving AI agents"}),
            indent=2,
        )
    )
