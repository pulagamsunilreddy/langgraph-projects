"""LangGraph backend for EasyTrip-Agent."""

from __future__ import annotations

import os
from typing import Annotated, Sequence, TypedDict

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

from tools import search_flights, search_web

load_dotenv()

SYSTEM_PROMPT = """You are EasyTrip, a helpful travel planning assistant.
You help users find flights, research destinations, and plan trips.
Use the available tools when you need live flight options or web research.
Be concise, practical, and friendly. When showing flights, highlight price,
timing, and airline clearly. Ask clarifying questions if origin, destination,
or dates are missing.
"""

TOOLS = [search_flights, search_web]


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


def _get_llm():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is not set. Add it to your .env file.")
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    return ChatOpenAI(model=model, temperature=0.2).bind_tools(TOOLS)


def call_model(state: AgentState) -> dict:
    llm = _get_llm()
    messages = [SystemMessage(content=SYSTEM_PROMPT), *state["messages"]]
    response = llm.invoke(messages)
    return {"messages": [response]}


def should_continue(state: AgentState) -> str:
    last = state["messages"][-1]
    if isinstance(last, AIMessage) and last.tool_calls:
        return "tools"
    return END


def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("agent", call_model)
    graph.add_node("tools", ToolNode(TOOLS))
    graph.set_entry_point("agent")
    graph.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
    graph.add_edge("tools", "agent")
    return graph.compile()


_agent = None


def get_agent():
    global _agent
    if _agent is None:
        _agent = build_graph()
    return _agent


def run_agent(user_message: str, history: list[dict] | None = None) -> str:
    """Run the EasyTrip agent and return the final assistant reply."""
    agent = get_agent()
    messages: list[BaseMessage] = []

    if history:
        for item in history:
            role = item.get("role")
            content = item.get("content", "")
            if role == "user":
                messages.append(HumanMessage(content=content))
            elif role == "assistant":
                messages.append(AIMessage(content=content))

    messages.append(HumanMessage(content=user_message))
    result = agent.invoke({"messages": messages})
    final = result["messages"][-1]
    return getattr(final, "content", str(final))
