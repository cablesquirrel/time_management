from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    default_balance_minutes: int | None = 300
    begin_stopped: bool | None = True
    awx_user: str
    awx_password: str
    awx_url: str
    awx_job_template_id: int
    awx_job_var_switch: str
    awx_job_var_interface: str

    class Config:
        """Configuration file location."""

        env_file: str = "../.env"
        # Don't error out if there are extra values in the ENV file
        extra: str = "ignore"


settings = Settings()
