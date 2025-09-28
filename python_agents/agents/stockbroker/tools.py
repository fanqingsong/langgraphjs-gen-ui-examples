"""
Tools for the Stockbroker agent.
"""

from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from pydantic import BaseModel, Field
import random
import time
from datetime import datetime

from .types import StockbrokerState, StockbrokerUpdate
from ..types import typed_ui


class PriceQuery(BaseModel):
    """Query for stock price."""
    ticker: str = Field(description="Stock ticker symbol")


class BuyOrder(BaseModel):
    """Buy order for stocks."""
    ticker: str = Field(description="Stock ticker symbol")
    quantity: int = Field(description="Number of shares to buy")


class PortfolioQuery(BaseModel):
    """Query for portfolio information."""
    pass


@tool
def get_stock_price(ticker: str) -> Dict[str, Any]:
    """Get current stock price for a given ticker."""
    # Simulate API call delay
    time.sleep(0.5)
    
    # Mock price data
    base_price = random.uniform(50, 500)
    change = random.uniform(-0.05, 0.05)
    current_price = base_price * (1 + change)
    
    return {
        "ticker": ticker.upper(),
        "price": round(current_price, 2),
        "change": round(change * 100, 2),
        "change_percent": round(change * 100, 2),
        "volume": random.randint(1000000, 10000000),
        "market_cap": random.randint(1000000000, 100000000000),
        "timestamp": datetime.now().isoformat()
    }


@tool
def buy_stock(ticker: str, quantity: int) -> Dict[str, Any]:
    """Buy shares of a stock."""
    # Simulate API call delay
    time.sleep(1)
    
    price_data = get_stock_price(ticker)
    total_cost = price_data["price"] * quantity
    
    return {
        "ticker": ticker.upper(),
        "quantity": quantity,
        "price_per_share": price_data["price"],
        "total_cost": round(total_cost, 2),
        "status": "success",
        "timestamp": datetime.now().isoformat()
    }


@tool
def get_portfolio() -> Dict[str, Any]:
    """Get user's portfolio information."""
    # Simulate API call delay
    time.sleep(0.5)
    
    # Mock portfolio data
    holdings = [
        {
            "ticker": "AAPL",
            "shares": 100,
            "current_price": 175.50,
            "total_value": 17550.00,
            "day_change": 2.30,
            "day_change_percent": 1.33
        },
        {
            "ticker": "GOOGL",
            "shares": 50,
            "current_price": 142.80,
            "total_value": 7140.00,
            "day_change": -1.20,
            "day_change_percent": -0.83
        },
        {
            "ticker": "MSFT",
            "shares": 75,
            "current_price": 378.90,
            "total_value": 28417.50,
            "day_change": 5.60,
            "day_change_percent": 1.50
        }
    ]
    
    total_value = sum(holding["total_value"] for holding in holdings)
    total_change = sum(holding["day_change"] * holding["shares"] for holding in holdings)
    
    return {
        "holdings": holdings,
        "total_value": round(total_value, 2),
        "total_day_change": round(total_change, 2),
        "total_day_change_percent": round((total_change / total_value) * 100, 2),
        "timestamp": datetime.now().isoformat()
    }


async def call_tools(state: StockbrokerState, config: Dict[str, Any]) -> StockbrokerUpdate:
    """Call the appropriate tools based on the conversation."""
    ui = typed_ui(config)
    model = ChatOpenAI(model="gpt-4o", temperature=0)
    
    # Bind tools to the model
    model_with_tools = model.bind_tools([get_stock_price, buy_stock, get_portfolio])
    
    # Convert messages to proper format
    messages = []
    for msg in state.get("messages", []):
        if isinstance(msg, dict):
            if msg.get("role") == "human":
                messages.append(HumanMessage(content=msg.get("content", "")))
            elif msg.get("role") == "assistant":
                messages.append(AIMessage(content=msg.get("content", "")))
        else:
            messages.append(msg)
    
    # Add system message
    system_message = HumanMessage(
        content="You are a helpful stockbroker assistant. Use the available tools to help users with stock prices, buying stocks, and viewing their portfolio."
    )
    messages.insert(0, system_message)
    
    response = await model_with_tools.ainvoke(messages)
    
    # Execute tool calls if any
    if response.tool_calls:
        tool_messages = []
        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            
            if tool_name == "get_stock_price":
                result = get_stock_price(**tool_args)
            elif tool_name == "buy_stock":
                result = buy_stock(**tool_args)
            elif tool_name == "get_portfolio":
                result = get_portfolio()
            else:
                result = {"error": f"Unknown tool: {tool_name}"}
            
            # Push UI component for each tool call
            ui.push(
                {
                    "name": "stockbroker",
                    "props": {
                        "toolName": tool_name,
                        "result": result,
                        "timestamp": time.time()
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
    
    return {
        "messages": [response]
    }
