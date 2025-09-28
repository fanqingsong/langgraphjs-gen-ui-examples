"""
Supervisor Agent - Routes conversations to specialized agents.
"""

from langgraph.graph import StateGraph, START, END
from .types import SupervisorAnnotation, SupervisorState
from .nodes.router import router
from .nodes.general_input import general_input

# Import all sub-agents
from ..stockbroker import stockbroker_graph
from ..trip_planner import trip_planner_graph
from ..open_code import open_code_graph
from ..pizza_orderer import pizza_orderer_graph
from ..writer_agent import writer_agent_graph


def handle_route(state: SupervisorState) -> str:
    """Route to the appropriate agent based on the next field."""
    return state.get("next", "generalInput")


# Create the graph
graph = StateGraph(SupervisorAnnotation)
graph.add_node("router", router)
graph.add_node("stockbroker", stockbroker_graph)
graph.add_node("tripPlanner", trip_planner_graph)
graph.add_node("openCode", open_code_graph)
graph.add_node("orderPizza", pizza_orderer_graph)
graph.add_node("generalInput", general_input)
graph.add_node("writerAgent", writer_agent_graph)

# Add conditional edges
graph.add_conditional_edges("router", handle_route, [
    "stockbroker", "tripPlanner", "openCode", 
    "orderPizza", "generalInput", "writerAgent"
])

# Add regular edges
graph.add_edge(START, "router")
graph.add_edge("stockbroker", END)
graph.add_edge("tripPlanner", END)
graph.add_edge("openCode", END)
graph.add_edge("orderPizza", END)
graph.add_edge("generalInput", END)
graph.add_edge("writerAgent", END)

# Compile the graph
supervisor_graph = graph.compile()
supervisor_graph.name = "Generative UI Agent"
