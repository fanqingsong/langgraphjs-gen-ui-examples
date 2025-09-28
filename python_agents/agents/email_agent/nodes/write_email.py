"""
Write email node for email agent.
"""

from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from pydantic import BaseModel, Field

from ..types import EmailAgentState, EmailAgentUpdate


class EmailSchema(BaseModel):
    """Schema for email content."""
    to: str = Field(description="Recipient email address")
    subject: str = Field(description="Email subject")
    body: str = Field(description="Email body content")


async def write_email(state: EmailAgentState) -> EmailAgentUpdate:
    """Write an email based on user input."""
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
        content="""You are an AI assistant that helps users write emails. 
        Extract the recipient email address, subject, and body content from the user's request.
        If any information is missing, ask the user to provide it."""
    )
    messages.insert(0, system_message)
    
    # Use structured output to extract email details
    structured_model = model.with_structured_output(EmailSchema)
    response = await structured_model.ainvoke(messages)
    
    # Create email object
    email = {
        "to": response.to,
        "subject": response.subject,
        "body": response.body,
        "from": "user@example.com"
    }
    
    return {
        "email": email,
        "messages": [AIMessage(content=f"I've drafted an email to {response.to} with subject '{response.subject}'.")]
    }
