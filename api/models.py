from typing import Optional

from pydantic import BaseModel


class ProcessEmailRequest(BaseModel):
    email_id: str
    user_id: str   # Microsoft 365 mailbox user
    lead_id: str   # Dynamics 365 lead GUID


class ProcessEmailResponse(BaseModel):
    email_id: str
    intent: str
    next_action: str
    compliance_approved: bool
    draft_reply: Optional[str] = None
    actions_taken: list[str]
    error: Optional[str] = None
