import httpx

from config.settings import settings
from services.auth import get_access_token

ODATA_HEADERS = {
    "OData-MaxVersion": "4.0",
    "OData-Version": "4.0",
    "Accept": "application/json",
    "Content-Type": "application/json",
}


async def _token() -> str:
    return await get_access_token(
        settings.crm_client_id,
        settings.crm_client_secret,
        settings.crm_tenant_id,
        f"{settings.crm_base_url}/.default",
    )


async def get_lead(lead_id: str) -> dict:
    token = await _token()
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{settings.crm_base_url}/api/data/v9.2/leads({lead_id})",
            headers={"Authorization": f"Bearer {token}", **ODATA_HEADERS},
        )
        response.raise_for_status()
        return response.json()


async def update_lead(lead_id: str, data: dict) -> None:
    token = await _token()
    async with httpx.AsyncClient() as client:
        response = await client.patch(
            f"{settings.crm_base_url}/api/data/v9.2/leads({lead_id})",
            headers={"Authorization": f"Bearer {token}", **ODATA_HEADERS},
            json=data,
        )
        response.raise_for_status()


async def log_activity(lead_id: str, subject: str, description: str) -> None:
    token = await _token()
    payload = {
        "subject": subject,
        "description": description,
        "regardingobjectid_lead@odata.bind": f"/leads({lead_id})",
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.crm_base_url}/api/data/v9.2/tasks",
            headers={"Authorization": f"Bearer {token}", **ODATA_HEADERS},
            json=payload,
        )
        response.raise_for_status()
