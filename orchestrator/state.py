from typing import Optional, TypedDict


class EmailProcessingState(TypedDict):
    # Input
    email_id: str
    user_id: str       # mailbox owner in Microsoft 365
    lead_id: str

    # Fetched data
    email: dict        # raw email from Graph API
    lead: dict         # lead record from CRM

    # Agent outputs
    intent: str               # positive | neutral | negative | no_reply
    next_action: str          # reply | schedule | escalate | no_action
    compliance_approved: bool
    draft_reply: Optional[str]

    # Tracking
    error: Optional[str]
    actions_taken: list[str]
