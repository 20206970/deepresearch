"""Search tool using Tavily"""

import json
from typing import Any, Dict, List, Optional

from langchain_core.tools import tool
from pydantic import BaseModel
from tavily import TavilyClient


class SearchResult(BaseModel):
    """搜索结果结构"""
    title: str
    url: str
    content: str
    answer: Optional[str] = None


@tool
def search_web(query: str, max_results: int = 5) -> str:
    """
    执行网络搜索，返回相关网页内容和摘要。

    Args:
        query: 搜索查询关键词
        max_results: 返回结果数量，默认5条

    Returns:
        JSON 格式的搜索结果，包含标题、URL和内容摘要
    """
    api_key = None
    try:
        from src.config import get_config
        config = get_config()
        api_key = config.search.tavily_api_key
    except Exception:
        pass

    if not api_key:
        return json.dumps({"error": "未配置 TAVILY_API_KEY", "results": []})

    try:
        client = TavilyClient(api_key=api_key)
        results = client.search(
            query=query,
            max_results=max_results,
            include_answer=True,
            include_raw_content=True,
        )

        search_results = []
        for item in results.get("results", []):
            search_results.append({
                "title": item.get("title", "无标题"),
                "url": item.get("url", ""),
                "content": item.get("content", "")[:1000],
            })

        output = {
            "answer": results.get("answer"),
            "results": search_results,
        }

        return json.dumps(output, ensure_ascii=False)

    except Exception as e:
        return json.dumps({"error": str(e), "results": []})