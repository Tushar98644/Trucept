from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    google_api_key: SecretStr = Field(..., env="GOOGLE_API_KEY")

    gemini_model: str = Field("gemini-2.5-flash", env="GEMINI_MODEL")
    gemini_temperature: float = Field(0, env="GEMINI_TEMPERATURE")
    gemini_max_output_tokens: int = Field(20000, env="GEMINI_MAX_OUTPUT_TOKENS")

    max_chunk_size: int = 8000
    enable_workflow_logging: bool = True
    workflow_retry_attempts: int = 3
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

settings = Settings()
