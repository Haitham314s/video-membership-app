import os
from functools import lru_cache
from pathlib import Path

from pydantic import BaseSettings, Field

os.environ["CQLENG_ALLOW_SCHEMA_MANAGEMENT"] = "1"


class Settings(BaseSettings):
    base_dir: Path = Path(__file__).resolve().parent
    templates_dir: Path = Path(__file__).resolve().parent / "templates"
    keyspace: str = Field(..., env="ASTRADB_KEYSPACE")
    db_client_id: str = Field(..., env="ASTRADB_CLIENT_ID")
    db_client_secret: str = Field(..., env="ASTRADB_CLIENT_SECRET")
    secret_key: str = Field(...)
    jwt_algorithm: str = Field(default="HS256")
    session_duration: int = Field(default=86400)

    algolia_api_key: str = Field(...)
    algolia_app_id: str = Field(...)
    algolia_index_name: str = Field(...)

    class Config:
        env_file = ".env"


@lru_cache
def get_settings():
    return Settings()
