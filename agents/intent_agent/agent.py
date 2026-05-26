from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import AzureChatOpenAI

from config.settings import settings
from orchestrator.state import EmailProcessingState

_llm = AzureChatOpenAI(
    azure_endpoint=settings.azure_openai_endpoint,
    api_key=settings.azure_openai_api_key,
    azure_deployment=settings.azure_openai_deployment_name,
    api_version=settings.azure_openai_api_version,
    temperature=0,
)

_SYSTEM = """You are an email intent classifier for a B2B sales team.
Classify the email intent as exactly one of: positive, neutral, negative, no_reply.

positive  — lead is interested, wants to proceed, or asks for more info
neutral   — lead acknowledges but has not committed; needs follow-up
negative  — lead is not interested or wants to unsubscribe
no_reply  — automated reply, out-of-office, or empty content

Respond with ONLY one word."""

_VALID = {"positive", "neutral", "negative", "no_reply"}


async def classify_intent_node(state: EmailProcessingState) -> EmailProcessingState:
    email = state["email"]
    subject = email.get("subject", "")
    body = email.get("body", {}).get("content", "")

    messages = [
        SystemMessage(content=_SYSTEM),
        HumanMessage(content=f"Subject: {subject}\n\nBody:\n{body[:2000]}"),
    ]

    response = await _llm.ainvoke(messages)
    intent = response.content.strip().lower()

    if intent not in _VALID:
        intent = "neutral"

    return {**state, "intent": intent}
