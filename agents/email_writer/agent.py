from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import AzureChatOpenAI

from config.settings import settings
from orchestrator.state import EmailProcessingState

_llm = AzureChatOpenAI(
    azure_endpoint=settings.azure_openai_endpoint,
    api_key=settings.azure_openai_api_key,
    azure_deployment=settings.azure_openai_deployment_name,
    api_version=settings.azure_openai_api_version,
    temperature=0.3,
)

_SYSTEM = """You are a B2B sales email writer.
Write a concise, professional reply.
- Under 150 words
- Warm but not pushy
- Use the actual lead name — no placeholders like [Name]
- Output only the email body, no subject line"""


async def write_email_node(state: EmailProcessingState) -> EmailProcessingState:
    email = state["email"]
    lead = state.get("lead", {})

    sender_name = email.get("from", {}).get("emailAddress", {}).get("name", "there")
    product_interest = lead.get("description", "our solution")

    context = f"""Lead name: {sender_name}
Product interest: {product_interest}
Their intent: {state["intent"]}
Suggested action: {state["next_action"]}
Original subject: {email.get("subject", "")}
Original body:
{email.get("body", {}).get("content", "")[:1000]}"""

    messages = [
        SystemMessage(content=_SYSTEM),
        HumanMessage(content=context),
    ]

    response = await _llm.ainvoke(messages)
    return {**state, "draft_reply": response.content.strip()}
