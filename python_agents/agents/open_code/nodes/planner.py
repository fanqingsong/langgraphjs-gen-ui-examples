"""
Planner node for open code agent.
"""

from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage

from ..types import OpenCodeState, OpenCodeUpdate


async def planner(state: OpenCodeState) -> OpenCodeUpdate:
    """Plan the code generation steps."""
    model = ChatOpenAI(model="gpt-4o", temperature=0)
    
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
        content="""You are a code generation assistant. Create a detailed plan for building a React TODO app.
        Break down the task into specific, actionable steps that can be implemented one by one.
        Each step should be clear and focused on a single aspect of the application."""
    )
    messages.insert(0, system_message)
    
    response = await model.ainvoke(messages)
    
    # Create a static plan for demonstration
    plan = [
        {
            "id": 1,
            "title": "Set up React project structure",
            "description": "Initialize a new React project with necessary dependencies",
            "code": "npx create-react-app todo-app\ncd todo-app\nnpm install"
        },
        {
            "id": 2,
            "title": "Create Todo component",
            "description": "Build the main Todo component with state management",
            "code": """import React, { useState } from 'react';\n\nconst Todo = () => {\n  const [todos, setTodos] = useState([]);\n  const [inputValue, setInputValue] = useState('');\n\n  return (\n    <div className=\"todo-app\">\n      <h1>Todo App</h1>\n      {/* Todo implementation */}\n    </div>\n  );\n};\n\nexport default Todo;"""
        },
        {
            "id": 3,
            "title": "Add todo functionality",
            "description": "Implement add, delete, and toggle todo functionality",
            "code": """const addTodo = () => {\n  if (inputValue.trim()) {\n    setTodos([...todos, {\n      id: Date.now(),\n      text: inputValue,\n      completed: false\n    }]);\n    setInputValue('');\n  }\n};\n\nconst deleteTodo = (id) => {\n  setTodos(todos.filter(todo => todo.id !== id));\n};\n\nconst toggleTodo = (id) => {\n  setTodos(todos.map(todo => \n    todo.id === id ? { ...todo, completed: !todo.completed } : todo\n  ));\n};"""
        },
        {
            "id": 4,
            "title": "Add styling",
            "description": "Style the todo app with CSS",
            "code": """.todo-app {\n  max-width: 600px;\n  margin: 0 auto;\n  padding: 20px;\n}\n\n.todo-item {\n  display: flex;\n  align-items: center;\n  padding: 10px;\n  border-bottom: 1px solid #eee;\n}\n\n.completed {\n  text-decoration: line-through;\n  color: #999;\n}"""
        }
    ]
    
    return {
        "plan": plan,
        "current_step": 0,
        "completed_steps": [],
        "messages": [response]
    }
