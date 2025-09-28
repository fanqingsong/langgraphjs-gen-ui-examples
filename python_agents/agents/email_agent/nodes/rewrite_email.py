"""
Rewrite email node for email agent.
"""

from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage

from ..types import EmailAgentState, EmailAgentUpdate


async def rewrite_email(state: EmailAgentState) -> EmailAgentUpdate:
    """Rewrite the email based on human feedback."""
    model = ChatOpenAI(model="gpt-4o", temperature=0)
    
    email = state.get("email", {})
    human_response = state.get("human_response", {})
    
    # Create messages for rewriting
    messages = [
        HumanMessage(content=f"Please rewrite this email based on the feedback: {human_response.get('content', '')}"),
        HumanMessage(content=f"Original email: To: {email.get('to')}, Subject: {email.get('subject')}, Body: {email.get('body')}")
    ]
    
    response = await model.ainvoke(messages)
    
    # Update email with rewritten content
    updated_email = email.copy()
    updated_email["body"] = response.content
    
    return {
        "email": updated_email,
        "messages": [AIMessage(content="I've rewritten the email based on your feedback.")]
    }
