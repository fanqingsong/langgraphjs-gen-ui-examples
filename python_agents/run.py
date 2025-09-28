#!/usr/bin/env python3
"""
Run script for Python LangGraph agents.
"""

import asyncio
import argparse
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_environment():
    """Check if required environment variables are set."""
    required_vars = ["OPENAI_API_KEY"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        print("Please set these variables in your .env file or environment.")
        return False
    
    return True

async def run_agent(agent_name: str, message: str):
    """Run a specific agent with a message."""
    try:
        from main import run_agent
        
        input_data = {
            "messages": [
                {"role": "human", "content": message}
            ]
        }
        
        print(f"Running {agent_name} agent with message: '{message}'")
        print("-" * 50)
        
        result = await run_agent(agent_name, input_data)
        
        print("Response:")
        if "messages" in result and result["messages"]:
            for msg in result["messages"]:
                if hasattr(msg, 'content'):
                    print(f"  {msg.content}")
                elif isinstance(msg, dict) and "content" in msg:
                    print(f"  {msg['content']}")
        
        if "ui" in result and result["ui"]:
            print(f"UI Components: {len(result['ui'])} generated")
        
        return True
        
    except Exception as e:
        print(f"❌ Error running agent: {e}")
        return False

async def interactive_mode():
    """Run in interactive mode."""
    print("Python LangGraph Agents - Interactive Mode")
    print("Type 'help' for available commands, 'quit' to exit")
    print("-" * 50)
    
    while True:
        try:
            user_input = input("\n> ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            
            if user_input.lower() == 'help':
                print("\nAvailable commands:")
                print("  agent <message>     - Run main supervisor agent")
                print("  chat <message>      - Run chat agent")
                print("  stock <message>     - Run stockbroker agent")
                print("  trip <message>      - Run trip planner agent")
                print("  code <message>      - Run open code agent")
                print("  pizza <message>     - Run pizza orderer agent")
                print("  write <message>     - Run writer agent")
                print("  email <message>     - Run email agent")
                print("  help                - Show this help")
                print("  quit                - Exit")
                continue
            
            if not user_input:
                continue
            
            # Parse command
            parts = user_input.split(' ', 1)
            command = parts[0].lower()
            message = parts[1] if len(parts) > 1 else "Hello"
            
            agent_map = {
                'agent': 'agent',
                'chat': 'chat',
                'stock': 'stockbroker',
                'trip': 'trip_planner',
                'code': 'open_code',
                'pizza': 'pizza_orderer',
                'write': 'writer_agent',
                'email': 'email_agent'
            }
            
            if command in agent_map:
                await run_agent(agent_map[command], message)
            else:
                print(f"Unknown command: {command}. Type 'help' for available commands.")
                
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Run Python LangGraph agents")
    parser.add_argument("--agent", "-a", default="agent", 
                       help="Agent to run (default: agent)")
    parser.add_argument("--message", "-m", default="What can you do?",
                       help="Message to send to the agent")
    parser.add_argument("--interactive", "-i", action="store_true",
                       help="Run in interactive mode")
    parser.add_argument("--test", "-t", action="store_true",
                       help="Run tests")
    
    args = parser.parse_args()
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    if args.test:
        # Run tests
        from test_agents import main as test_main
        asyncio.run(test_main())
    elif args.interactive:
        # Interactive mode
        asyncio.run(interactive_mode())
    else:
        # Single run
        asyncio.run(run_agent(args.agent, args.message))

if __name__ == "__main__":
    main()
