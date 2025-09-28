"""
Types for the Open Code agent.
"""

from typing import Dict, Any, Optional, List
from langgraph.graph import Annotation
from ..types import GenerativeUIAnnotation


# Create annotation for open code agent
OpenCodeAnnotation = GenerativeUIAnnotation.Root({
    "messages": GenerativeUIAnnotation.spec["messages"],
    "plan": Annotation[Optional[List[Dict[str, Any]]]],
    "current_step": Annotation[Optional[int]],
    "completed_steps": Annotation[List[int]]
})

# Type aliases
OpenCodeState = OpenCodeAnnotation.State
OpenCodeUpdate = OpenCodeAnnotation.Update

# Constants
SUCCESSFULLY_COMPLETED_STEPS_CONTENT = "All steps have been successfully completed!"
