"""Tavily web search tool for EasyTrip-Agent."""

from __future__ import annotations

import os
from dotenv import load_dotenv
load_dotenv()
from langchain_core.tools import tool
from tavily import TavilyClient
api_key = os.getenv("TAVILY_API_KEY")

client = TavilyClient(api_key=api_key)

def tavily_search(query):     
    if not api_key:
        return "TAVILY_API_KEY is not set. Add it to your .env file."
    try:
        response = client.search(query=query, max_results=5)
        results = []
        for i, r in enumerate(response["results"], 1):
            title = r.get("title", "Untitled")
            url = r.get("url", "")
            snippit = r.get("content", "").strip()
            if len(snippit) > 250:
                snippit = snippit[:250].rsplit(" ", 1)[0] + "..."
            results.append(f"{i}. {title}\n{url}\n{snippit}")
        return "\n".join(results)
    except Exception as e:
        return f"Error: {e}"
