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


async def get_email(user_id: str, message_id: str) -> dict:
    token = await _token()
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{GRAPH_BASE}/users/{user_id}/messages/{message_id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        response.raise_for_status()
        return response.json()


async def list_emails(user_id: str, folder: str = "inbox", top: int = 10) -> list[dict]:
    token = await _token()
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{GRAPH_BASE}/users/{user_id}/mailFolders/{folder}/messages",
            headers={"Authorization": f"Bearer {token}"},
            params={"$top": top, "$orderby": "receivedDateTime desc"},
        )
        response.raise_for_status()
        return response.json().get("value", [])


async def send_email(user_id: str, to: str, subject: str, body: str) -> None:
    token = await _token()
    payload = {
        "message": {
            "subject": subject,
            "body": {"contentType": "HTML", "content": body},
            "toRecipients": [{"emailAddress": {"address": to}}],
        }
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{GRAPH_BASE}/users/{user_id}/sendMail",
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            json=payload,
        )
        response.raise_for_status()
