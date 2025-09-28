"""
Main entry point for the Python LangGraph agents.
"""

import os
import asyncio
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END

# Load environment variables
load_dotenv()

# Import all agents
from agents.chat_agent import agent as chat_agent
from agents.supervisor import supervisor_graph
from agents.email_agent import email_agent
from agents.stockbroker import stockbroker_graph
from agents.trip_planner import trip_planner_graph
from agents.open_code import open_code_graph
from agents.pizza_orderer import pizza_orderer_graph
from agents.writer_agent import writer_agent_graph

# Agent registry
AGENTS = {
    "agent": supervisor_graph,  # Main supervisor agent
    "chat": chat_agent,
    "email_agent": email_agent,
    "stockbroker": stockbroker_graph,
    "trip_planner": trip_planner_graph,
    "open_code": open_code_graph,
    "pizza_orderer": pizza_orderer_graph,
    "writer_agent": writer_agent_graph
}


async def run_agent(agent_name: str, input_data: dict) -> dict:
    """Run a specific agent with input data."""
    if agent_name not in AGENTS:
        raise ValueError(f"Unknown agent: {agent_name}")
    
    agent = AGENTS[agent_name]
    result = await agent.ainvoke(input_data)
    return result


async def main():
    """Main function for testing agents."""
    print("Python LangGraph Agents")
    print("Available agents:", list(AGENTS.keys()))
    
    # Example usage
    test_input = {
        "messages": [
            {"role": "human", "content": "What can you do?"}
        ]
    }
    
    try:
        result = await run_agent("agent", test_input)
        print("Result:", result)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
