"""Settings module"""

class Settings:
    gcp_project_id: str = "savvy-equator-491510-k9"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    anthropic_api_key: str = ""
    firestore_database: str = "(default)"


settings = Settings()
