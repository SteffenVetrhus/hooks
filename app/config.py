"""
Application configuration module.

Loads settings from environment variables (or a .env file) using pydantic-settings.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Attributes:
        pocketbase_url: The base URL of the PocketBase instance.
                        Defaults to "http://127.0.0.1:8090".
        pocketbase_admin_email: Optional admin email for authenticating with PocketBase.
                                Required for operations that need admin privileges.
        pocketbase_admin_password: Optional admin password for authenticating with PocketBase.
                                   Required for operations that need admin privileges.
    """

    pocketbase_url: str = "http://127.0.0.1:8090"
    pocketbase_admin_email: str = ""
    pocketbase_admin_password: str = ""

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


# Singleton settings instance used throughout the application
settings = Settings()
