"""
Classification node for trip planner.
"""

from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage
from pydantic import BaseModel, Field

from ..types import TripPlannerState, TripPlannerUpdate


class ClassificationSchema(BaseModel):
    """Schema for trip relevance classification."""
    is_relevant: bool = Field(description="Whether the trip details are still relevant to the user's request")


@tool
def classify_trip_relevance(is_relevant: bool) -> Dict[str, Any]:
    """Classify whether trip details are still relevant."""
    return {"is_relevant": is_relevant}


async def classify(state: TripPlannerState) -> TripPlannerUpdate:
    """Classify whether trip details are still relevant."""
    if not state.get("trip_details"):
        return {}
    
    trip_details = state["trip_details"]
    
    model = ChatOpenAI(model="gpt-4o", temperature=0)
    model_with_tools = model.bind_tools([classify_trip_relevance])
    
    prompt = f"""You're an AI assistant for planning trips. The user has already specified the following details for their trip:
- location - {trip_details['location']}
- start_date - {trip_details['start_date']}
- end_date - {trip_details['end_date']}
- number_of_guests - {trip_details['number_of_guests']}

Your task is to carefully read over the user's conversation, and determine if their trip details are still relevant to their most recent request.
You should set is_relevant to false if they are now asking about a new location, trip duration, or number of guests.
If they do NOT change their request details (or they never specified them), please set is_relevant to true.
"""
    
    # Format messages for the model
    messages = []
    for msg in state.get("messages", []):
        if isinstance(msg, dict):
            if msg.get("role") == "human":
                messages.append(HumanMessage(content=msg.get("content", "")))
            elif msg.get("role") == "assistant":
                messages.append(AIMessage(content=msg.get("content", "")))
        else:
            messages.append(msg)
    
    human_message = f"Here is the entire conversation so far:\n{_format_messages(state.get('messages', []))}"
    
    response = await model_with_tools.ainvoke([
        HumanMessage(content=prompt),
        HumanMessage(content=human_message)
    ])
    
    # Extract classification result
    if response.tool_calls:
        classification_result = response.tool_calls[0]["args"]
        if not classification_result.get("is_relevant", True):
            return {
                "trip_details": None
            }
    
    return {}


def _format_messages(messages: list) -> str:
    """Format messages for display."""
    formatted = []
    for msg in messages:
        if isinstance(msg, dict):
            role = msg.get("role", "unknown")
            content = msg.get("content", "")
            formatted.append(f"{role}: {content}")
        else:
            formatted.append(str(msg))
    return "\n".join(formatted)
