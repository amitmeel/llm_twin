from loguru import logger
from pydantic_settings import BaseSettings, SettingsConfigDict
from zenml.client import Client
from zenml.exceptions import EntityExistsError

class Settings(BaseSettings):
    """
    The `Settings` class manages configuration values required for the application. 

    This class extends `BaseSettings` from Pydantic, allowing environment variables 
    to be loaded automatically from an `.env` file. It supports retrieving and exporting 
    settings from the ZenML secret store.
    """

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    # Required settings when working locally or remote


    # Required settings when deploying the code

    # MongoDB 
    MONGODB_DATABASE_HOST: str = "mongodb_uri"
    MONGODB_DATABASE_USERNAME: str = "mongodb_username"
    MONGODB_DATABASE_PASSWORD: str = "mongodb_password"
    MONGODB_DATABASE_NAME: str = "llm-twin"

    @classmethod
    def load_settings(cls) -> "Settings":
        """
        This method tries to load the settings from the ZenML secret store.If the secret does not exist,
        it initializes the settings from the .env file and default values.
        
        Returns: 
            Settings: The initialized settings object.
        """

        try:
            logger.info("Loading settings from zenml secret store.")
            setting_secrets = Client().get_secret("settings")
            settings = Settings(**setting_secrets.secret_values)
        except (RuntimeError, KeyError):
            logger.warning(
                "Failed to load settings from the ZenML store. Defaulting to loading default values from .env file. "
            )
            settings = Settings()

        return settings
    
    def export(self) -> None:
        """
        Export the settings to ZenML secret store.
        """

        env_vars = self.model_dump()
        for key, value in env_vars.items():
            env_vars[key] = str(value)

        client = Client()

        try:
            client.create_secret(name='settings', values=env_vars)
        except EntityExistsError:
            logger.warning(
                "Secret 'scope' already exists. Delete it manually by running "
                "'zenml secret delete settings',before trying to recreate it."
            )

settings = Settings().load_settings()    



