from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    default_balance_minutes: int | None = 300

    class Config:
        """Configuration file location."""

        env_file: str = "../.env"
        # Don't error out if there are extra values in the ENV file
        extra: str = "ignore"


settings = Settings()
