import json
from typing import List, Union
from pydantic_settings import BaseSettings
from pydantic import ConfigDict, field_validator


class Settings(BaseSettings):
    PROJECT_NAME: str = "ParcelPilot"
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    POSTGRES_USER: str = "user"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "parcelpilot"

    CORS_ORIGINS: Union[str, List[str]] = ["*"]

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, list):
            return [str(i).strip() for i in v if str(i).strip()]

        if isinstance(v, str):
            value = v.strip()
            if not value:
                return ["*"]

            if value.startswith("["):
                try:
                    parsed = json.loads(value)
                except json.JSONDecodeError as exc:
                    raise ValueError("CORS_ORIGINS must be a comma-separated list or JSON array") from exc
                if not isinstance(parsed, list):
                    raise ValueError("CORS_ORIGINS JSON value must be an array")
                return [str(i).strip() for i in parsed if str(i).strip()]

            return [i.strip() for i in value.split(",") if i.strip()]

        raise ValueError("Invalid CORS_ORIGINS value")

    model_config = ConfigDict(env_file=".env", extra="ignore")


settings = Settings()
