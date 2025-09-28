"""
Open Code Agent - Handles code generation with step-by-step execution.
"""

from typing import Dict, Any
from langgraph.graph import StateGraph, START, END
from .types import OpenCodeAnnotation, SUCCESSFULLY_COMPLETED_STEPS_CONTENT, OpenCodeState
from .nodes.planner import planner
from .nodes.executor import executor


def conditionally_end(state: OpenCodeState, config: Dict[str, Any]) -> str:
    """Conditionally end the graph based on completion or permissions."""
    full_write_access = config.get("configurable", {}).get("permissions", {}).get("full_write_access", False)
    last_ai_message = None
    
    # Find the last AI message
    for msg in reversed(state.get("messages", [])):
        if isinstance(msg, dict) and msg.get("role") == "assistant":
            last_ai_message = msg
            break
    
    # If the user did not grant full write access, or the last AI message is the success message, end
    if (last_ai_message and 
        last_ai_message.get("content") == SUCCESSFULLY_COMPLETED_STEPS_CONTENT) or not full_write_access:
        return END
    
    return "planner"


# Create the graph
graph = StateGraph(OpenCodeAnnotation)
graph.add_node("planner", planner)
graph.add_node("executor", executor)
graph.add_edge(START, "planner")
graph.add_edge("planner", "executor")
graph.add_conditional_edges("executor", conditionally_end, ["planner", END])

# Compile the graph
open_code_graph = graph.compile()
open_code_graph.name = "Open Code Graph"
