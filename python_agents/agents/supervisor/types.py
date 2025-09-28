"""
Types for the Supervisor agent.
"""

from typing import Dict, Any, Optional, List, Union, Literal
from langgraph.graph import Annotation
from ..types import GenerativeUIAnnotation


# Create annotation for supervisor
SupervisorAnnotation = GenerativeUIAnnotation.Root({
    "messages": GenerativeUIAnnotation.spec["messages"],
    "next": Annotation[Optional[Literal[
        "stockbroker", "tripPlanner", "openCode", 
        "orderPizza", "generalInput", "writerAgent"
    ]]]
})

# Type aliases
SupervisorState = SupervisorAnnotation.State
SupervisorUpdate = SupervisorAnnotation.Update

# Tool descriptions for routing
ALL_TOOL_DESCRIPTIONS = """- stockbroker: can fetch the price of a ticker, purchase/sell a ticker, or get the user's portfolio
- tripPlanner: helps the user plan their trip. it can suggest restaurants, and places to stay in any given location.
- openCode: can write a React TODO app for the user. Only call this tool if they request a TODO app.
- orderPizza: can order a pizza for the user
- writerAgent: can write a text document for the user. Only call this tool if they request a text document."""
