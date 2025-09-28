"""
Interrupt node for email agent - implements human-in-the-loop functionality.
"""

from typing import Dict, Any
from langgraph.graph import interrupt

from ..types import EmailAgentState, EmailAgentUpdate, HumanResponse


@interrupt
async def interrupt_node(state: EmailAgentState) -> EmailAgentUpdate:
    """Interrupt the flow to get human input."""
    if not state.get("email"):
        return {}
    
    # This will cause the graph to pause and wait for human input
    # The human response will be provided through the state
    return {
        "messages": [{
            "type": "human_interrupt",
            "content": "Please review the email and choose an action: Accept, Edit, Respond, or Ignore",
            "email": state["email"]
        }]
    }
