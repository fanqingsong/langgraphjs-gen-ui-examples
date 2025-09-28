"""
General input node for supervisor agent.
"""

from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage

from ..types import SupervisorState, SupervisorUpdate


async def general_input(state: SupervisorState) -> SupervisorUpdate:
    """Handle general input that doesn't require specialized agents."""
    model = ChatOpenAI(model="gpt-4o", temperature=0)
    
    # Format messages
    messages = []
    for msg in state.get("messages", []):
        if isinstance(msg, dict):
            if msg.get("role") == "human":
                messages.append(HumanMessage(content=msg.get("content", "")))
            elif msg.get("role") == "assistant":
                messages.append(AIMessage(content=msg.get("content", "")))
        else:
            messages.append(msg)
    
    system_message = HumanMessage(
        content="You are a helpful AI assistant. Provide a helpful response to the user's query."
    )
    messages.insert(0, system_message)
    
    response = await model.ainvoke(messages)
    
    return {
        "messages": [response]
    }
