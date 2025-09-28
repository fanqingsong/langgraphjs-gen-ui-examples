"""
Chat Agent - A simple chat agent without tools or generative UI components.
"""

from typing import Dict, Any, List
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage

from .types import GenerativeUIAnnotation


# Create annotation for chat agent
ChatAgentAnnotation = GenerativeUIAnnotation.Root({
    "messages": GenerativeUIAnnotation.spec["messages"]
})


async def chat_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Simple chat node that processes messages with an LLM."""
    model = ChatOpenAI(model="gpt-4o-mini")
    
    # Convert state messages to proper format
    messages = []
    for msg in state.get("messages", []):
        if isinstance(msg, dict):
            if msg.get("role") == "human":
                messages.append(HumanMessage(content=msg.get("content", "")))
            elif msg.get("role") == "assistant":
                messages.append(AIMessage(content=msg.get("content", "")))
        else:
            messages.append(msg)
    
    # Add system message
    system_message = HumanMessage(content="You are a helpful assistant.")
    messages.insert(0, system_message)
    
    response = await model.ainvoke(messages)
    
    return {
        "messages": [response]
    }


# Create the graph
graph = StateGraph(ChatAgentAnnotation)
graph.add_node("chat", chat_node)
graph.add_edge(START, "chat")
graph.add_edge("chat", END)

# Compile the graph
agent = graph.compile()
agent.name = "Chat Agent"
