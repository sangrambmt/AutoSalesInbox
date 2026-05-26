from orchestrator.state import EmailProcessingState
from services.crm import client as crm_client
from services.graph_mail import client as mail_client


async def read_email_node(state: EmailProcessingState) -> EmailProcessingState:
    email = await mail_client.get_email(state["user_id"], state["email_id"])
    lead = await crm_client.get_lead(state["lead_id"])
    return {**state, "email": email, "lead": lead}
