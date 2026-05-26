from orchestrator.state import EmailProcessingState

_MAX_EMAILS_PER_WEEK = 3


def _is_compliant(lead: dict) -> bool:
    # Dynamics 365 opt-out flags
    if lead.get("donotbulkemail") or lead.get("donotemail"):
        return False

    # Frequency cap — real implementation queries CRM activity history
    if lead.get("emails_this_week", 0) >= _MAX_EMAILS_PER_WEEK:
        return False

    return True


async def check_compliance_node(state: EmailProcessingState) -> EmailProcessingState:
    approved = _is_compliant(state.get("lead", {}))
    return {**state, "compliance_approved": approved}
