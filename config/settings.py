from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Azure OpenAI
    azure_openai_endpoint: str = ""
    azure_openai_api_key: str = ""
    azure_openai_deployment_name: str = "gpt-4o-mini"
    azure_openai_api_version: str = "2024-08-01-preview"

    # Microsoft Graph API
    graph_client_id: str = ""
    graph_client_secret: str = ""
    graph_tenant_id: str = ""

    # CRM / Dynamics 365
    crm_base_url: str = ""
    crm_client_id: str = ""
    crm_client_secret: str = ""
    crm_tenant_id: str = ""

    # Azure Service Bus
    service_bus_connection_string: str = ""

    # App
    log_level: str = "INFO"


settings = Settings()
