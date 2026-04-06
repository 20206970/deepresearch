"""Research workflow using LangGraph"""

import json
import re
from typing import Any, Dict, Iterator, Optional

from langgraph.graph import StateGraph, END
from langgraph.constants import START, Send

from src.agents import create_planner_agent, create_summarizer_agent, create_reporter_agent
from src.config import get_config
from src.memory.short_term import get_short_term_memory, get_memory_context
from src.memory.long_term import get_long_term_memory, search_long_term_memory, save_research_memory
from src.state import SearchSource


def _create_llm():
    """Create LLM instance from config"""
    from langchain_openai import ChatOpenAI
    config = get_config()
    return ChatOpenAI(
        model=config.llm.model,
        base_url=config.llm.base_url,
        api_key=config.llm.api_key,
        temperature=config.llm.temperature,
    )


def _parse_tasks(response: str) -> list[dict]:
    """Parse Agent output to extract task list"""
    match = re.search(r'\{[\s\S]*"tasks"[\s\S]*\}', response)
    if not match:
        return []

    try:
        data = json.loads(match.group())
        tasks = data.get("tasks", [])
        return [
            {
                "id": i + 1,
                "title": t.get("title", f"任务{i+1}"),
                "intent": t.get("intent", ""),
                "query": t.get("query", ""),
            }
            for i, t in enumerate(tasks)
        ]
    except json.JSONDecodeError:
        return []


def planner_node(state: dict) -> dict:
    """Planner node: generates task list"""
    llm = _create_llm()
    agent = create_planner_agent(llm)

    topic = state.get("topic", "")

    # Get memory context
    try:
        short_mem = get_short_term_memory(llm)
        long_mem = get_long_term_memory()
        context = get_memory_context(short_mem) if short_mem else ""
        long_context = "\n".join(search_long_term_memory(topic, long_mem) if long_mem else [])
    except Exception:
        context = ""
        long_context = ""

    prompt = f"""当前研究主题：{topic}

历史上下文：
{context}

长期记忆参考：
{long_context}

请为此主题规划研究任务。"""

    response = agent.invoke({"messages": [("user", prompt)]})
    output = response.get("messages", [])[-1].content

    tasks = _parse_tasks(output)

    # Fallback task if no tasks generated
    if not tasks:
        tasks = [{
            "id": 1,
            "title": "基础背景梳理",
            "intent": "收集主题的核心背景与最新动态",
            "query": f"{topic} 最新进展",
        }]

    return {
        "tasks": tasks,
        "loop_count": state.get("loop_count", 0) + 1,
    }


def search_summarize_node(state: dict) -> dict:
    """Search and summarize node"""
    llm = _create_llm()
    agent = create_summarizer_agent(llm)

    task = state.get("task", {})
    topic = state.get("topic", "")

    query = task.get("query", "")

    prompt = f"""任务主题：{topic}
任务名称：{task.get("title", "")}
任务目标：{task.get("intent", "")}
检索查询：{query}

请执行搜索并生成任务总结。

重要：在总结的最后，请以以下 JSON 格式列出你参考的来源：
```json
{{
  "sources": [
    {{"title": "来源标题", "url": "https://..."}},
    ...
  ]
}}
```"""

    response = agent.invoke({"messages": [("user", prompt)]})
    output = response.get("messages", [])[-1].content

    # Extract summary content
    summary = output
    if "<think>" in summary:
        summary = summary.split("</think>")[-1].strip()

    # Extract sources from output
    sources = []
    try:
        # Try to find JSON at the end
        json_match = re.search(r'```json\s*([\s\S]*?)\s*```', output)
        if json_match:
            data = json.loads(json_match.group(1))
            sources = data.get("sources", [])
    except (json.JSONDecodeError, AttributeError):
        pass

    # Build SearchSource objects
    search_sources = [SearchSource(query=query, url=s.get("url") if isinstance(s, dict) else None, title=s.get("title") if isinstance(s, dict) else None) for s in sources]

    return {
        "task_results": [summary],
        "sources": search_sources,
    }


def reporter_node(state: dict) -> dict:
    """Reporter node: generate final report"""
    llm = _create_llm()
    agent = create_reporter_agent(llm)

    topic = state.get("topic", "")
    tasks = state.get("tasks", [])
    results = state.get("task_results", [])
    sources = state.get("sources", [])

    # Build task overview with sources
    tasks_block = []
    for i, (task, result) in enumerate(zip(tasks, results), 1):
        tasks_block.append(f"""### 任务 {i}: {task.get('title', '')}
- 任务目标：{task.get('intent', '')}
- 检索查询：{task.get('query', '')}
- 任务总结：{result}
""")

    # Build sources list
    sources_block = []
    for s in sources:
        url = s.url if hasattr(s, 'url') else s.get("url") if isinstance(s, dict) else None
        title = s.title if hasattr(s, 'title') else s.get("title") if isinstance(s, dict) else url
        if url:
            sources_block.append(f"- [{title}]({url})")

    prompt = f"""研究主题：{topic}

任务概览：
{''.join(tasks_block)}

参考来源：
{chr(10).join(sources_block) if sources_block else "无来源信息"}

请根据以上任务总结和来源链接生成最终研究报告。

要求：
1. 在报告中适当位置添加来源引用，使用 Markdown 链接格式
2. 参考来源格式：[标题](URL)"""

    response = agent.invoke({"messages": [("user", prompt)]})
    report = response.get("messages", [])[-1].content

    # Clean output
    if "<think>" in report:
        report = report.split("</think>")[-1].strip()

    # Save to long-term memory
    try:
        long_mem = get_long_term_memory()
        if long_mem:
            save_research_memory(topic, results, report, long_mem)
    except Exception:
        pass

    return {"report": report}


def _split_tasks(state: dict) -> list[Send]:
    """Split tasks to parallel nodes"""
    tasks = state.get("tasks", [])
    return [Send("search_summarize", {**state, "task": task}) for task in tasks]


def create_research_graph():
    """Create research workflow graph"""
    from src.state import ResearchState

    workflow = StateGraph(ResearchState)

    # Add nodes
    workflow.add_node("planner", planner_node)
    workflow.add_node("search_summarize", search_summarize_node)
    workflow.add_node("reporter", reporter_node)

    # Set entry point
    workflow.add_edge(START, "planner")

    # Conditional edges: from planner to parallel tasks
    workflow.add_conditional_edges(
        "planner",
        _split_tasks,
        ["search_summarize"]
    )

    # Edges: from tasks to reporter
    workflow.add_edge("search_summarize", "reporter")
    workflow.add_edge("reporter", END)

    return workflow.compile()


# Global graph instance
_research_graph = None


def get_research_graph():
    """Get research workflow graph (cached)"""
    global _research_graph
    if _research_graph is None:
        _research_graph = create_research_graph()
    return _research_graph