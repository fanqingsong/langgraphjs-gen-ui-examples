"""
Type definitions for the LangGraph agents.
This module contains the core type definitions and annotations used across all agents.
"""

from typing import Dict, Any, Optional, List, Union, Literal
from datetime import datetime
from pydantic import BaseModel
from langgraph.graph import Annotation
import uuid


class UIMessage(BaseModel):
    """UI message for generative UI components."""
    id: str
    name: str
    props: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = None


class RemoveUIMessage(BaseModel):
    """Message to remove a UI component."""
    id: str


# Create the main annotation for generative UI
GenerativeUIAnnotation = Annotation.Root({
    "messages": Annotation[List[Dict[str, Any]]],
    "ui": Annotation[List[Union[UIMessage, RemoveUIMessage]]],
    "context": Annotation[Optional[Dict[str, Any]]],
    "timestamp": Annotation[Optional[float]],
    "next": Annotation[Optional[Literal[
        "stockbroker", "tripPlanner", "openCode", 
        "orderPizza", "writerAgent", "generalInput"
    ]]]
})

# Type aliases
GenerativeUIState = GenerativeUIAnnotation.State
GenerativeUIUpdate = GenerativeUIAnnotation.Update


class Accommodation(BaseModel):
    """Accommodation information for trip planning."""
    id: str
    name: str
    price: float
    rating: float
    city: str
    image: str


class Price(BaseModel):
    """Stock price information."""
    ticker: str
    open: float
    close: float
    high: float
    low: float
    volume: int
    time: str


class Snapshot(BaseModel):
    """Market snapshot information."""
    price: float
    ticker: str
    day_change: float
    day_change_percent: float
    market_cap: float
    time: str


class TripDetails(BaseModel):
    """Trip planning details."""
    location: str
    start_date: datetime
    end_date: datetime
    number_of_guests: int


class ToolCall(BaseModel):
    """Tool call information."""
    name: str
    args: Dict[str, Any]
    id: Optional[str] = None
    type: str = "tool_call"


def find_tool_call(name: str):
    """Find a specific tool call by name."""
    def predicate(tool_call: ToolCall) -> bool:
        return tool_call.name == name
    return predicate


class UIMessageManager:
    """Manager for UI messages in Python LangGraph agents."""
    
    def __init__(self):
        self.items = []
    
    def push(self, ui_component: Dict[str, Any], message_metadata: Optional[Dict[str, Any]] = None):
        """Push a UI component to the UI state."""
        ui_message = {
            "id": ui_component.get("id", str(uuid.uuid4())),
            "name": ui_component["name"],
            "props": ui_component["props"],
            "metadata": message_metadata or {}
        }
        self.items.append(ui_message)
        return ui_message


def typed_ui(config: Dict[str, Any]) -> UIMessageManager:
    """Create a typed UI manager for the given config."""
    return UIMessageManager()
