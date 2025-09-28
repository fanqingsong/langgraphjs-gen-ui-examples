"""
Writer Agent - Handles text document writing with generative UI.
"""

from typing import Dict, Any, List
from langgraph.graph import StateGraph, START
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from pydantic import BaseModel, Field
import uuid

from .types import GenerativeUIAnnotation, Annotation, typed_ui


class CreateTextDocumentTool(BaseModel):
    """Schema for creating a text document."""
    title: str = Field(description="Title of the document")
    description: str = Field(description="Description of the document")


# Create annotation for writer agent
WriterAnnotation = GenerativeUIAnnotation.Root({
    "messages": GenerativeUIAnnotation.spec["messages"],
    "ui": GenerativeUIAnnotation.spec["ui"],
    "context": Annotation[Dict[str, Any]]
})

# Type aliases
WriterState = WriterAnnotation.State
WriterUpdate = WriterAnnotation.Update


async def prepare(state: WriterState, config: Dict[str, Any]) -> WriterUpdate:
    """Prepare the document by creating initial draft."""
    ui = typed_ui(config)
    model = ChatAnthropic(model="claude-3-5-sonnet-latest")
    
    # Create tool for document creation
    def draft_text_document(title: str, description: str) -> Dict[str, Any]:
        """Prepare a text document for the user with a short title and short description for browsing purposes."""
        return {
            "title": title,
            "description": description,
            "is_generating": True
        }
    
    # Format messages
    messages = []
    if state.get("context", {}).get("writer", {}).get("selected"):
        messages.append(HumanMessage(
            content=f"Selected text in question: {state['context']['writer']['selected']}"
        ))
    
    for msg in state.get("messages", []):
        if isinstance(msg, dict):
            if msg.get("role") == "human":
                messages.append(HumanMessage(content=msg.get("content", "")))
            elif msg.get("role") == "assistant":
                messages.append(AIMessage(content=msg.get("content", "")))
        else:
            messages.append(msg)
    
    # Create streaming response
    response = await model.astream(messages)
    
    document_id = str(uuid.uuid4())
    message = None
    
    async for chunk in response:
        if message is None:
            message = chunk
        else:
            message = message + chunk
        
        # Check for tool calls
        if hasattr(message, 'tool_calls') and message.tool_calls:
            for tool_call in message.tool_calls:
                if tool_call.get("name") == "draft_text_document":
                    tool_args = tool_call.get("args", {})
                    ui.push(
                        {
                            "id": document_id,
                            "name": "writer",
                            "props": {
                                **tool_args,
                                "is_generating": True
                            }
                        },
                        {"message": message}
                    )
    
    return {
        "messages": [message] if message else [],
        "ui": ui.items
    }


async def writer(state: WriterState, config: Dict[str, Any]) -> WriterUpdate:
    """Write the actual content of the document."""
    ui = typed_ui(config)
    last_message = state.get("messages", [])[-1] if state.get("messages") else None
    last_ui = None
    
    # Find the last UI component
    for ui_item in reversed(state.get("ui", [])):
        if (isinstance(ui_item, dict) and 
            ui_item.get("name") == "writer" and 
            ui_item.get("metadata", {}).get("message_id") == getattr(last_message, "id", None)):
            last_ui = ui_item
            break
    
    if not last_ui or not last_message:
        return {}
    
    document_id = last_ui["id"]
    
    # Create model for content generation
    model = ChatAnthropic(model="claude-3-5-sonnet-latest")
    
    # Format messages for content generation
    messages = []
    system_content = (
        "Write a text document based on the user's request. "
        "Only output the content, do not ask any additional questions."
    )
    
    if state.get("context", {}).get("writer", {}).get("selected"):
        system_content += f"\n\nSelected text in question: {state['context']['writer']['selected']}"
    
    messages.append(HumanMessage(content=system_content))
    
    # Add previous messages (excluding the last one)
    for msg in state.get("messages", [])[:-1]:
        if isinstance(msg, dict):
            if msg.get("role") == "human":
                messages.append(HumanMessage(content=msg.get("content", "")))
            elif msg.get("role") == "assistant":
                messages.append(AIMessage(content=msg.get("content", "")))
        else:
            messages.append(msg)
    
    # Generate content
    content_message = None
    
    async for chunk in model.astream(messages):
        if content_message is None:
            content_message = chunk
        else:
            content_message = content_message + chunk
        
        content = getattr(content_message, 'content', '') if content_message else ""
        
        ui.push(
            {
                "id": document_id,
                "name": "writer",
                "props": {
                    "content": content,
                    "is_generating": True
                }
            },
            {"message": last_message}
        )
    
    # Add final UI component
    ui.push(
        {
            "id": document_id,
            "name": "writer",
            "props": {
                "is_generating": False
            }
        },
        {"message": last_message}
    )
    
    return {
        "messages": [],
        "ui": ui.items
    }


async def suggestions(state: WriterState) -> WriterUpdate:
    """Generate suggestions for the document."""
    messages = state.get("messages", []).copy()
    last_message = messages[-1] if messages else None
    
    if not last_message or not hasattr(last_message, 'tool_calls'):
        return {}
    
    # Add tool responses
    for tool_call in getattr(last_message, 'tool_calls', []):
        if tool_call.get("id"):
            messages.append({
                "type": "tool",
                "content": "Finished",
                "tool_call_id": tool_call["id"]
            })
    
    model = ChatAnthropic(model="claude-3-5-sonnet-latest")
    finish = await model.ainvoke(messages)
    messages.append(finish)
    
    return {
        "messages": messages
    }


# Create the graph
graph = StateGraph(WriterAnnotation)
graph.add_node("prepare", prepare)
graph.add_node("writer", writer)
graph.add_node("suggestions", suggestions)
graph.add_edge(START, "prepare")
graph.add_edge("prepare", "writer")
graph.add_edge("writer", "suggestions")

# Compile the graph
writer_agent_graph = graph.compile()
writer_agent_graph.name = "Writer Agent"
