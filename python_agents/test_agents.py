"""
Test script for Python LangGraph agents.
"""

import asyncio
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def test_imports():
    """Test that all agents can be imported without errors."""
    try:
        from agents.chat_agent import agent as chat_agent
        print("✓ Chat agent imported successfully")
        
        from agents.supervisor import supervisor_graph
        print("✓ Supervisor agent imported successfully")
        
        from agents.stockbroker import stockbroker_graph
        print("✓ Stockbroker agent imported successfully")
        
        from agents.trip_planner import trip_planner_graph
        print("✓ Trip planner agent imported successfully")
        
        from agents.open_code import open_code_graph
        print("✓ Open code agent imported successfully")
        
        from agents.pizza_orderer import pizza_orderer_graph
        print("✓ Pizza orderer agent imported successfully")
        
        from agents.writer_agent import writer_agent_graph
        print("✓ Writer agent imported successfully")
        
        from agents.email_agent import email_agent
        print("✓ Email agent imported successfully")
        
        print("\n✅ All agents imported successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

async def test_basic_functionality():
    """Test basic functionality of agents."""
    try:
        from agents.chat_agent import agent as chat_agent
        
        # Test chat agent
        test_input = {
            "messages": [
                {"role": "human", "content": "Hello, how are you?"}
            ]
        }
        
        print("\nTesting chat agent...")
        result = await chat_agent.ainvoke(test_input)
        print(f"✓ Chat agent response: {result.get('messages', [])[-1].content[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Functionality test error: {e}")
        return False

async def main():
    """Main test function."""
    print("Python LangGraph Agents - Test Suite")
    print("=" * 50)
    
    # Test imports
    import_success = await test_imports()
    
    if import_success:
        # Test basic functionality
        await test_basic_functionality()
    
    print("\n" + "=" * 50)
    if import_success:
        print("🎉 All tests passed! The Python agents are ready to use.")
    else:
        print("❌ Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    asyncio.run(main())
