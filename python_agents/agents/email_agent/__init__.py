"""
Email Agent - Handles email writing with human-in-the-loop functionality.
"""

from langgraph.graph import StateGraph, START, END
from .types import EmailAgentAnnotation, HumanResponse, EmailAgentState
from .nodes.write_email import write_email
from .nodes.interrupt import interrupt_node
from .nodes.send_email import send_email
from .nodes.rewrite_email import rewrite_email


def route_after_interrupt(state: EmailAgentState) -> str:
    """Route after interrupt based on human response."""
    response_type = state.get("human_response", {}).get("type")
    if not response_type or response_type == "ignore":
        return END
    if response_type == "response":
        return "rewrite_email"
    return "send_email"


def route_after_writing_email(state: EmailAgentState) -> str:
    """Route after writing email."""
    if not state.get("email"):
        return END
    return "interrupt"


# Create the graph
graph = StateGraph(EmailAgentAnnotation)
graph.add_node("writeEmail", write_email)
graph.add_node("interrupt", interrupt_node)
graph.add_node("sendEmail", send_email)
graph.add_node("rewriteEmail", rewrite_email)

# Add edges
graph.add_edge(START, "writeEmail")
graph.add_conditional_edges("writeEmail", route_after_writing_email, [END, "interrupt"])
graph.add_conditional_edges("interrupt", route_after_interrupt, ["sendEmail", "rewriteEmail", END])
graph.add_edge("rewriteEmail", "interrupt")
graph.add_edge("sendEmail", END)

# Compile the graph
email_agent = graph.compile()
email_agent.name = "Email Assistant Agent"
