from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    do_inference_api_key: str
    do_inference_base_url: str = "https://inference.do-ai.run/v1"
    do_model: str = "llama3.3-70b-instruct"
    cors_origins: list[str] = ["*"]
    env: str = "dev"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
