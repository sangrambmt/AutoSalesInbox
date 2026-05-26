from langgraph.graph import END, StateGraph

from agents.compliance_agent.agent import check_compliance_node
from agents.decision_agent.agent import make_decision_node
from agents.email_reader.agent import read_email_node
from agents.email_writer.agent import write_email_node
from agents.intent_agent.agent import classify_intent_node
from orchestrator.state import EmailProcessingState
from services.crm import client as crm_client
from services.graph_mail import client as mail_client


async def execute_action_node(state: EmailProcessingState) -> EmailProcessingState:
    actions: list[str] = []

    if state["next_action"] == "reply" and state.get("draft_reply"):
        email = state["email"]
        sender_email = email.get("from", {}).get("emailAddress", {}).get("address", "")
        await mail_client.send_email(
            user_id=state["user_id"],
            to=sender_email,
            subject=f"Re: {email.get('subject', '')}",
            body=state["draft_reply"],
        )
        actions.append("email_sent")

    await crm_client.log_activity(
        lead_id=state["lead_id"],
        subject=f"Auto-reply — intent: {state['intent']}",
        description=state.get("draft_reply") or "No reply generated",
    )
    actions.append("crm_logged")

    return {**state, "actions_taken": actions}


def _route_after_decision(state: EmailProcessingState) -> str:
    return "end" if state["next_action"] == "no_action" else "check_compliance"


def _route_after_compliance(state: EmailProcessingState) -> str:
    return "write_email" if state.get("compliance_approved") else "end"


def build_graph():
    graph = StateGraph(EmailProcessingState)

    graph.add_node("read_email", read_email_node)
    graph.add_node("classify_intent", classify_intent_node)
    graph.add_node("make_decision", make_decision_node)
    graph.add_node("check_compliance", check_compliance_node)
    graph.add_node("write_email", write_email_node)
    graph.add_node("execute_action", execute_action_node)

    graph.set_entry_point("read_email")
    graph.add_edge("read_email", "classify_intent")
    graph.add_edge("classify_intent", "make_decision")
    graph.add_conditional_edges(
        "make_decision",
        _route_after_decision,
        {"end": END, "check_compliance": "check_compliance"},
    )
    graph.add_conditional_edges(
        "check_compliance",
        _route_after_compliance,
        {"write_email": "write_email", "end": END},
    )
    graph.add_edge("write_email", "execute_action")
    graph.add_edge("execute_action", END)

    return graph.compile()


email_graph = build_graph()
