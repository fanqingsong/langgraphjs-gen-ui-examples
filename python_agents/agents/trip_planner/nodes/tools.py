"""
Tools node for trip planner.
"""

from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage
import random
import time

from ..types import TripPlannerState, TripPlannerUpdate
from ...types import typed_ui


@tool
def list_accommodations() -> Dict[str, Any]:
    """List accommodations for the user."""
    # Simulate API call delay
    time.sleep(0.5)
    
    # Mock accommodation data
    accommodations = []
    cities = ["New York", "San Francisco", "Los Angeles", "Chicago", "Miami"]
    
    for i in range(5):
        accommodations.append({
            "id": f"acc_{i+1}",
            "name": f"Hotel {chr(65+i)}",
            "price": round(random.uniform(100, 500), 2),
            "rating": round(random.uniform(3.5, 5.0), 1),
            "city": random.choice(cities),
            "image": f"https://example.com/hotel_{i+1}.jpg"
        })
    
    return {
        "accommodations": accommodations,
        "total": len(accommodations)
    }


@tool
def list_restaurants() -> Dict[str, Any]:
    """List restaurants for the user."""
    # Simulate API call delay
    time.sleep(0.5)
    
    # Mock restaurant data
    restaurants = []
    cuisines = ["Italian", "Chinese", "Mexican", "Japanese", "American"]
    
    for i in range(5):
        restaurants.append({
            "id": f"rest_{i+1}",
            "name": f"Restaurant {chr(65+i)}",
            "cuisine": random.choice(cuisines),
            "rating": round(random.uniform(3.5, 5.0), 1),
            "price_range": random.choice(["$", "$$", "$$$", "$$$$"]),
            "address": f"{random.randint(100, 999)} Main St"
        })
    
    return {
        "restaurants": restaurants,
        "total": len(restaurants)
    }


async def call_tools(state: TripPlannerState, config: Dict[str, Any]) -> TripPlannerUpdate:
    """Call the appropriate tools based on the conversation."""
    if not state.get("trip_details"):
        raise ValueError("No trip details found")
    
    trip_details = state["trip_details"]
    ui = typed_ui(config)
    
    model = ChatOpenAI(model="gpt-4o", temperature=0)
    model_with_tools = model.bind_tools([list_accommodations, list_restaurants])
    
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
    
    system_message = HumanMessage(
        content="You are an AI assistant who helps users book trips. Use the user's most recent message(s) to contextually generate a response."
    )
    messages.insert(0, system_message)
    
    response = await model_with_tools.ainvoke(messages)
    
    # Check for tool calls
    if not response.tool_calls:
        raise ValueError("No tool calls found")
    
    # Execute tool calls and push UI components
    tool_messages = []
    
    for tool_call in response.tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        
        if tool_name == "list_accommodations":
            result = list_accommodations()
            ui.push(
                {
                    "name": "accommodations-list",
                    "props": {
                        "toolCallId": tool_call["id"],
                        "accommodations": result["accommodations"],
                        "tripDetails": trip_details
                    }
                },
                {"message": response}
            )
        elif tool_name == "list_restaurants":
            result = list_restaurants()
            ui.push(
                {
                    "name": "restaurants-list", 
                    "props": {
                        "tripDetails": trip_details,
                        "restaurants": result["restaurants"]
                    }
                },
                {"message": response}
            )
        
        tool_messages.append({
            "type": "tool",
            "content": str(result),
            "tool_call_id": tool_call["id"]
        })
    
    return {
        "messages": [response] + tool_messages,
        "ui": ui.items,
        "timestamp": time.time()
    }
