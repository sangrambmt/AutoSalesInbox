from orchestrator.state import EmailProcessingState

# leadqualitycode values in Dynamics 365: 1=Hot, 2=Warm, 3=Cold
_HOT = 1


def _decide(intent: str, lead: dict) -> str:
    if intent in ("no_reply", "negative"):
        return "no_action"

    quality = lead.get("leadqualitycode", 3)

    if intent == "positive":
        return "schedule" if quality == _HOT else "reply"

    # neutral — keep nurturing
    return "reply"


async def make_decision_node(state: EmailProcessingState) -> EmailProcessingState:
    next_action = _decide(state["intent"], state.get("lead", {}))
    return {**state, "next_action": next_action}
