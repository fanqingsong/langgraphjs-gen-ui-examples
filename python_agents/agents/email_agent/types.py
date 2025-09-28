"""
Types for the Email Agent.
"""

from typing import Dict, Any, Optional, List, Union, Literal
from langgraph.graph import Annotation
from pydantic import BaseModel
from ..types import GenerativeUIAnnotation


class HumanResponse(BaseModel):
    """Human response to email interrupt."""
    type: Literal["response", "ignore", "accept", "edit"]
    content: Optional[str] = None


# Create annotation for email agent
EmailAgentAnnotation = GenerativeUIAnnotation.Root({
    "messages": GenerativeUIAnnotation.spec["messages"],
    "email": Annotation[Optional[Dict[str, Any]]],
    "human_response": Annotation[Optional[HumanResponse]]
})

# Type aliases
EmailAgentState = EmailAgentAnnotation.State
EmailAgentUpdate = EmailAgentAnnotation.Update
