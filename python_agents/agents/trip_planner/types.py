"""
Types for the Trip Planner agent.
"""

from typing import Dict, Any, Optional, List, Union
from datetime import datetime
from langgraph.graph import Annotation
from ..types import GenerativeUIAnnotation, TripDetails


# Create annotation for trip planner
TripPlannerAnnotation = GenerativeUIAnnotation.Root({
    "messages": GenerativeUIAnnotation.spec["messages"],
    "ui": GenerativeUIAnnotation.spec["ui"],
    "timestamp": GenerativeUIAnnotation.spec["timestamp"],
    "trip_details": Annotation[Optional[TripDetails]]
})

# Type aliases
TripPlannerState = TripPlannerAnnotation.State
TripPlannerUpdate = TripPlannerAnnotation.Update
