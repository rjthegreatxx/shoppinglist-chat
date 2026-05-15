from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    do_inference_api_key: str
    do_inference_base_url: str = "https://inference.do-ai.run/v1"
    do_model: str = "llama3.3-70b-instruct"
    qdrant_url: str = ""
    qdrant_api_key: str = ""
    cors_origins: list[str] = ["*"]
    env: str = "dev"

    # Vector search constants shared between app and ingestion script
    qdrant_collection: str = "products"
    embedding_model: str = "all-mini-lm-l6-v2"
    embedding_dimensions: int = 384
    rag_top_k: int = 5
    rag_score_threshold: float = 0.3

    stripe_secret_key: str = ""
    stripe_webhook_secret: str = ""
    stripe_success_url: str = "http://localhost:3000/checkout/success"
    stripe_cancel_url: str = "http://localhost:3000/checkout/cancel"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def qdrant_configured(self) -> bool:
        return bool(self.qdrant_url and self.qdrant_api_key)


settings = Settings()
