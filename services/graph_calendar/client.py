from datetime import datetime

import httpx

from config.settings import settings
from services.auth import get_access_token

GRAPH_BASE = "https://graph.microsoft.com/v1.0"
GRAPH_SCOPE = "https://graph.microsoft.com/.default"


async def _token() -> str:
    return await get_access_token(
        settings.graph_client_id,
        settings.graph_client_secret,
        settings.graph_tenant_id,
        GRAPH_SCOPE,
    )


async def create_event(
    user_id: str,
    subject: str,
    body: str,
    start: datetime,
    end: datetime,
    attendee_email: str,
) -> dict:
    token = await _token()
    payload = {
        "subject": subject,
        "body": {"contentType": "HTML", "content": body},
        "start": {"dateTime": start.isoformat(), "timeZone": "UTC"},
        "end": {"dateTime": end.isoformat(), "timeZone": "UTC"},
        "attendees": [
            {"emailAddress": {"address": attendee_email}, "type": "required"}
        ],
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{GRAPH_BASE}/users/{user_id}/events",
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            json=payload,
        )
        response.raise_for_status()
        return response.json()
