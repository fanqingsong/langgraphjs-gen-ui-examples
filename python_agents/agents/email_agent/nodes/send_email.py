"""
Send email node for email agent.
"""

from typing import Dict, Any
from langchain_core.messages import AIMessage

from ..types import EmailAgentState, EmailAgentUpdate


async def send_email(state: EmailAgentState) -> EmailAgentUpdate:
    """Send the email."""
    email = state.get("email", {})
    
    # Simulate sending email
    message = AIMessage(
        content=f"Email sent successfully to {email.get('to', 'unknown')} with subject '{email.get('subject', 'No Subject')}'"
    )
    
    return {
        "messages": [message]
    }
