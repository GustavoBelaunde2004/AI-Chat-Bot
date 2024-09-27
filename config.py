import os
from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from pathlib import Path

SOURCE_DIR = Path(__file__).resolve().parents[0]
ENV_FILE: str = os.path.join(SOURCE_DIR, ".env")


class Settings(BaseSettings):
    # Whatsapp Cloud API
    webhook_verify_token: str = Field(default="")
    graph_api_token: str = Field(default="")
    phone_id: str = Field(default="")

    # Bot Aliado API
    botaliado_api_url: str = Field(default="")
    botaliado_api_key: str = Field(default="")
    botaliado_user_id: str = Field(default="")

    # Azure Services
    speech_api_key: str = Field(default="")
    speech_api_region: str = Field(default="")

    #Sql Database
    sql_username:str = Field(default="")
    sql_password:str = Field(default="")
    sql_server:str = Field(default="")
    sql_database:str = Field(default="")

    #Config
    model_config = SettingsConfigDict(env_file="../.env", env_file_encoding="utf-8")

    def __init__(self, config_file: str = None, *args, **kwargs):
        super().__init__(_env_file=config_file or ENV_FILE, *args, **kwargs)


@lru_cache
def get_settings() -> Settings:
    """
    Returns a Settings object loaded with config properties from a .env file.
    The Settings object is allocated once in the memory and available during
    the application lifetime.
    """
    return Settings()

# # Test
# a = get_settings()
# print(a.model_dump())
