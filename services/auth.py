import httpx


async def get_access_token(client_id: str, client_secret: str, tenant_id: str, scope: str) -> str:
    """Client credentials OAuth2 flow — used by all Microsoft services."""
    url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    async with httpx.AsyncClient() as client:
        response = await client.post(url, data={
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
            "scope": scope,
        })
        response.raise_for_status()
        return response.json()["access_token"]
