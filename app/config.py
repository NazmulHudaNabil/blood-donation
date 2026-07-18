import logging

from pydantic import field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger("app.config")


class Settings(BaseSettings):
    DATABASE_URL: str

    @field_validator("DATABASE_URL")
    def assemble_db_connection(cls, v: str) -> str:
        if v.startswith("postgres://"):
            return v.replace("postgres://", "postgresql+psycopg://", 1)
        elif v.startswith("postgresql://"):
            return v.replace("postgresql://", "postgresql+psycopg://", 1)
        return v

    SECRET_KEY: str

    ALGORITHM: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int

    ENVIRONMENT: str = "development"

    # Verbose SQL logging — leave off by default, it's noisy and can leak
    # bound parameter values (e.g. password hashes) into stdout/log storage.
    DB_ECHO: bool = False

    # Comma-separated list of allowed browser origins for CORS.
    CORS_ORIGINS: str = "http://localhost:3000,http://127.0.0.1:3000"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

    @model_validator(mode="after")
    def _check_secret_key_strength(self):
        if len(self.SECRET_KEY) < 32:
            message = (
                f"SECRET_KEY is only {len(self.SECRET_KEY)} characters — use at least 32 "
                "random characters (e.g. `openssl rand -hex 32`) for a real deployment."
            )
            if self.ENVIRONMENT == "production":
                raise ValueError(message)
            logger.warning(message)
        return self


settings = Settings()
