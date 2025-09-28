"""
Pizza Orderer Agent - Handles pizza ordering.
"""

import asyncio
from typing import Dict, Any
from langgraph.graph import StateGraph, START, END
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, AIMessage
from pydantic import BaseModel, Field
import uuid

from .types import GenerativeUIAnnotation


class FindShopSchema(BaseModel):
    """Schema for finding a pizza shop."""
    location: str = Field(description="The location the user is in. E.g. 'San Francisco' or 'New York'")
    pizza_company: str = Field(None, description="The name of the pizza company. E.g. 'Dominos' or 'Papa John's'. Optional")


class PlaceOrderSchema(BaseModel):
    """Schema for placing a pizza order."""
    address: str = Field(description="The address of the store to order the pizza from")
    phone_number: str = Field(description="The phone number of the store to order the pizza from")
    order: str = Field(description="The full pizza order for the user")


# Create annotation for pizza orderer
PizzaOrdererAnnotation = GenerativeUIAnnotation.Root({
    "messages": GenerativeUIAnnotation.spec["messages"]
})


async def sleep(ms: int = 5000) -> None:
    """Sleep for specified milliseconds."""
    await asyncio.sleep(ms / 1000)


async def find_store(state: Dict[str, Any]) -> Dict[str, Any]:
    """Find a pizza store for the user."""
    model = ChatAnthropic(
        model="claude-3-5-sonnet-latest",
        temperature=0
    ).with_structured_output(FindShopSchema)
    
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
        content="You are a helpful AI assistant, tasked with extracting information from the conversation between you, and the user, in order to find a pizza shop for them."
    )
    messages.insert(0, system_message)
    
    response = await model.ainvoke(messages)
    
    await sleep()
    
    # Create tool response
    tool_response = {
        "type": "tool",
        "id": str(uuid.uuid4()),
        "content": "I've found a pizza shop at 1119 19th St, San Francisco, CA 94107. The phone number for the shop is 415-555-1234.",
        "tool_call_id": str(uuid.uuid4())
    }
    
    return {
        "messages": [response.dict(), tool_response]
    }


async def order_pizza(state: Dict[str, Any]) -> Dict[str, Any]:
    """Order pizza for the user."""
    await sleep(1500)
    
    model = ChatAnthropic(
        model="claude-3-5-sonnet-latest",
        temperature=0
    ).with_structured_output(PlaceOrderSchema)
    
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
        content="You are a helpful AI assistant, tasked with placing an order for a pizza for the user."
    )
    messages.insert(0, system_message)
    
    response = await model.ainvoke(messages)
    
    # Create tool response
    tool_response = {
        "type": "tool",
        "id": str(uuid.uuid4()),
        "content": "Pizza order successfully placed.",
        "tool_call_id": str(uuid.uuid4())
    }
    
    return {
        "messages": [response.dict(), tool_response]
    }


# Create the graph
graph = StateGraph(PizzaOrdererAnnotation)
graph.add_node("findStore", find_store)
graph.add_node("orderPizza", order_pizza)
graph.add_edge(START, "findStore")
graph.add_edge("findStore", "orderPizza")
graph.add_edge("orderPizza", END)

# Compile the graph
pizza_orderer_graph = graph.compile()
pizza_orderer_graph.name = "Order Pizza Graph"
