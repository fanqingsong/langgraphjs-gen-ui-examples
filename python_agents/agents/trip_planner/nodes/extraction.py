"""
Extraction node for trip planner.
"""

from typing import Dict, Any
from datetime import datetime, timedelta
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage
from pydantic import BaseModel, Field
import uuid

from ..types import TripPlannerState, TripPlannerUpdate, TripDetails


class ExtractionSchema(BaseModel):
    """Schema for trip details extraction."""
    location: str = Field(description="The location to plan the trip for. Can be a city, state, or country.")
    start_date: str = Field(None, description="The start date of the trip. Should be in YYYY-MM-DD format")
    end_date: str = Field(None, description="The end date of the trip. Should be in YYYY-MM-DD format")
    number_of_guests: int = Field(2, description="The number of guests for the trip. Should default to 2 if not specified")


@tool
def extract_trip_details(
    location: str,
    start_date: str = None,
    end_date: str = None,
    number_of_guests: int = 2
) -> Dict[str, Any]:
    """Extract trip details from user input."""
    return {
        "location": location,
        "start_date": start_date,
        "end_date": end_date,
        "number_of_guests": number_of_guests
    }


def calculate_dates(start_date: str = None, end_date: str = None) -> tuple[datetime, datetime]:
    """Calculate start and end dates with defaults."""
    now = datetime.now()
    
    if not start_date and not end_date:
        # Both undefined: 4 and 5 weeks in future
        start = now + timedelta(weeks=4)
        end = now + timedelta(weeks=5)
        return start, end
    
    if start_date and not end_date:
        # Only start defined: end is 1 week after
        start = datetime.fromisoformat(start_date)
        end = start + timedelta(weeks=1)
        return start, end
    
    if not start_date and end_date:
        # Only end defined: start is 1 week before
        end = datetime.fromisoformat(end_date)
        start = end - timedelta(weeks=1)
        return start, end
    
    # Both defined: use as is
    return datetime.fromisoformat(start_date), datetime.fromisoformat(end_date)


async def extraction(state: TripPlannerState) -> TripPlannerUpdate:
    """Extract trip details from user input."""
    model = ChatOpenAI(model="gpt-4o", temperature=0)
    model_with_tools = model.bind_tools([extract_trip_details])
    
    prompt = """You're an AI assistant for planning trips. The user has requested information about a trip they want to go on.
Before you can help them, you need to extract the following information from their request:
- location - The location to plan the trip for. Can be a city, state, or country.
- start_date - The start date of the trip. Should be in YYYY-MM-DD format. Optional
- end_date - The end date of the trip. Should be in YYYY-MM-DD format. Optional
- number_of_guests - The number of guests for the trip. Optional

You are provided with the ENTIRE conversation history between you, and the user. Use these messages to extract the necessary information.

Do NOT guess, or make up any information. If the user did NOT specify a location, please respond with a request for them to specify the location.
You should ONLY send a clarification message if the user did not provide the location. You do NOT need any of the other fields, so if they're missing, proceed without them.
It should be a single sentence, along the lines of "Please specify the location for the trip you want to go on".

Extract only what is specified by the user. It is okay to leave fields blank if the user did not specify them.
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
    
    # Check if we got a tool call
    if not response.tool_calls:
        return {
            "messages": [response]
        }
    
    # Extract the details
    tool_call = response.tool_calls[0]
    extracted_details = tool_call["args"]
    
    # Calculate dates
    start_date, end_date = calculate_dates(
        extracted_details.get("start_date"),
        extracted_details.get("end_date")
    )
    
    # Create trip details
    trip_details = TripDetails(
        location=extracted_details["location"],
        start_date=start_date,
        end_date=end_date,
        number_of_guests=extracted_details.get("number_of_guests", 2)
    )
    
    # Create tool response
    tool_response = {
        "type": "tool",
        "id": f"extract-{uuid.uuid4()}",
        "tool_call_id": tool_call["id"],
        "content": "Successfully extracted trip details"
    }
    
    return {
        "trip_details": trip_details.dict(),
        "messages": [response, tool_response]
    }


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
