"""Tavily web search tool for EasyTrip-Agent."""

from __future__ import annotations

import os

from langchain_core.tools import tool
from tavily import TavilyClient


@tool
def search_web(query: str, max_results: int = 5) -> str:
    """Search the web for travel tips, attractions, weather, or destination info.

    Args:
        query: Search query, e.g. "best things to do in Goa in December".
        max_results: Maximum number of results to return (default 5).

    Returns:
        A formatted string of search results, or an error message.
    """
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return "TAVILY_API_KEY is not set. Add it to your .env file."

    try:
        client = TavilyClient(api_key=api_key)
        response = client.search(query=query, max_results=max_results)
        results = response.get("results", [])
        if not results:
            return f"No results found for: {query}"

        lines = [f"Web results for: {query}", ""]
        for i, item in enumerate(results, start=1):
            title = item.get("title", "Untitled")
            url = item.get("url", "")
            content = item.get("content", "")
            lines.append(f"{i}. {title}")
            lines.append(f"   URL: {url}")
            lines.append(f"   Summary: {content}")
            lines.append("")
        return "\n".join(lines)
    except Exception as exc:  # noqa: BLE001
        return f"Tavily search failed: {exc}"
