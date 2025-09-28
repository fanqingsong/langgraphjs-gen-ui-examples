"""
Executor node for open code agent.
"""

from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
import uuid
import time

from ..types import OpenCodeState, OpenCodeUpdate, SUCCESSFULLY_COMPLETED_STEPS_CONTENT
from ...types import typed_ui


async def executor(state: OpenCodeState, config: Dict[str, Any]) -> OpenCodeUpdate:
    """Execute the current step in the plan."""
    ui = typed_ui(config)
    
    # Find the last plan tool call
    last_plan_tool_call = None
    for msg in reversed(state.get("messages", [])):
        if (isinstance(msg, dict) and 
            msg.get("type") == "ai" and 
            msg.get("tool_calls") and
            any(tc.get("name") == "plan" for tc in msg.get("tool_calls", []))):
            last_plan_tool_call = msg
            break
    
    plan_tool_call_args = last_plan_tool_call.get("tool_calls", [{}])[0].get("args", {}) if last_plan_tool_call else {}
    next_plan_item = plan_tool_call_args.get("remainingPlans", [None])[0] if plan_tool_call_args.get("remainingPlans") else None
    
    num_seen_plans = len(
        (plan_tool_call_args.get("executedPlans", []) or []) +
        (plan_tool_call_args.get("rejectedPlans", []) or [])
    )
    
    if not next_plan_item:
        # All plans have been executed
        successfully_finished_msg = {
            "type": "ai",
            "id": str(uuid.uuid4()),
            "content": SUCCESSFULLY_COMPLETED_STEPS_CONTENT,
        }
        return {"messages": [successfully_finished_msg]}
    
    # Mock file contents for different steps
    update_file_contents = ""
    step_files = {
        0: "src/agent/open-code/nodes/plan-code/step-1.txt",
        1: "src/agent/open-code/nodes/plan-code/step-2.txt", 
        2: "src/agent/open-code/nodes/plan-code/step-3.txt",
        3: "src/agent/open-code/nodes/plan-code/step-4.txt",
        4: "src/agent/open-code/nodes/plan-code/step-5.txt",
        5: "src/agent/open-code/nodes/plan-code/step-6.txt",
    }
    
    if num_seen_plans in step_files:
        # Mock file content - in real implementation, you would read from file
        update_file_contents = f"// Step {num_seen_plans + 1} code content\n// {next_plan_item}\n\n// Mock generated code for this step"
    else:
        update_file_contents = ""
    
    if not update_file_contents:
        raise ValueError("No file updates found!")
    
    tool_call_id = str(uuid.uuid4())
    ai_message = {
        "type": "ai",
        "id": str(uuid.uuid4()),
        "content": "",
        "tool_calls": [
            {
                "name": "update_file",
                "args": {
                    "new_file_content": update_file_contents,
                    "executed_plan_item": next_plan_item,
                },
                "id": tool_call_id,
                "type": "tool_call",
            },
        ],
    }
    
    full_write_access = bool(config.get("configurable", {}).get("permissions", {}).get("full_write_access", False))
    
    # Push UI component - this is the key functionality that was missing!
    ui.push(
        {
            "name": "proposed-change",
            "props": {
                "toolCallId": tool_call_id,
                "change": update_file_contents,
                "planItem": next_plan_item,
                "fullWriteAccess": full_write_access,
            },
        },
        {"message": ai_message},
    )
    
    return {
        "messages": [ai_message],
        "ui": ui.items,
        "timestamp": time.time(),
    }
