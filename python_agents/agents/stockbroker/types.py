"""
Types for the Stockbroker agent.
"""

from typing import Dict, Any, Optional, List, Union
from langgraph.graph import Annotation
from ..types import GenerativeUIAnnotation


# Create annotation for stockbroker
StockbrokerAnnotation = GenerativeUIAnnotation.Root({
    "messages": GenerativeUIAnnotation.spec["messages"],
    "ui": GenerativeUIAnnotation.spec["ui"],
    "timestamp": GenerativeUIAnnotation.spec["timestamp"]
})

# Type aliases
StockbrokerState = StockbrokerAnnotation.State
StockbrokerUpdate = StockbrokerAnnotation.Update
