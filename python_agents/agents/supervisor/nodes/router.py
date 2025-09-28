"""
Router node for supervisor agent.
"""

from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage

from ..types import SupervisorState, SupervisorUpdate, ALL_TOOL_DESCRIPTIONS


@tool
def route_to_agent(agent: str) -> Dict[str, Any]:
    """Route to a specific agent based on the conversation context."""
    return {"agent": agent}


async def router(state: SupervisorState) -> SupervisorUpdate:
    """Route the conversation to the appropriate agent."""
    model = ChatOpenAI(model="gpt-4o", temperature=0)
    model_with_tools = model.bind_tools([route_to_agent])
    
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
        content=f"""You are a supervisor agent that routes conversations to specialized agents.
        
        Available agents:
        {ALL_TOOL_DESCRIPTIONS}
        
        Based on the conversation, determine which agent should handle the user's request.
        If no specific agent is needed, route to 'generalInput' for general conversation."""
    )
    messages.insert(0, system_message)
    
    response = await model_with_tools.ainvoke(messages)
    
    # Extract the routing decision
    next_agent = "generalInput"  # Default
    if response.tool_calls:
        for tool_call in response.tool_calls:
            if tool_call.get("name") == "route_to_agent":
                next_agent = tool_call.get("args", {}).get("agent", "generalInput")
                break
    
    return {
        "next": next_agent,
        "messages": [response]
    }
