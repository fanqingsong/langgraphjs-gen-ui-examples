"""
Trip Planner Agent - Handles trip planning and booking.
"""

from langgraph.graph import StateGraph, START, END
from .types import TripPlannerAnnotation, TripPlannerState
from .nodes.classify import classify
from .nodes.extraction import extraction
from .nodes.tools import call_tools


def route_start(state: TripPlannerState) -> str:
    """Route from start based on trip details."""
    if not state.get("trip_details"):
        return "extraction"
    return "classify"


def route_after_classifying(state: TripPlannerState) -> str:
    """Route after classification."""
    if not state.get("trip_details"):
        return "extraction"
    return "call_tools"


def route_after_extraction(state: TripPlannerState) -> str:
    """Route after extraction."""
    if not state.get("trip_details"):
        return END
    return "call_tools"


# Create the graph
graph = StateGraph(TripPlannerAnnotation)
graph.add_node("classify", classify)
graph.add_node("extraction", extraction)
graph.add_node("call_tools", call_tools)

# Add conditional edges
graph.add_conditional_edges(
    START, 
    route_start, 
    ["classify", "extraction"]
)
graph.add_conditional_edges(
    "classify", 
    route_after_classifying, 
    ["call_tools", "extraction"]
)
graph.add_conditional_edges(
    "extraction", 
    route_after_extraction, 
    ["call_tools", END]
)

# Add regular edges
graph.add_edge("call_tools", END)

# Compile the graph
trip_planner_graph = graph.compile()
trip_planner_graph.name = "Trip Planner"
