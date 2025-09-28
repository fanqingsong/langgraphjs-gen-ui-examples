"""
Stockbroker Agent - Handles stock trading and portfolio management.
"""

from langgraph.graph import StateGraph, START
from .types import StockbrokerAnnotation
from .tools import call_tools

# Create the graph
graph = StateGraph(StockbrokerAnnotation)
graph.add_node("agent", call_tools)
graph.add_edge(START, "agent")

# Compile the graph
stockbroker_graph = graph.compile()
stockbroker_graph.name = "Stockbroker"
