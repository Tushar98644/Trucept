from pydantic import BaseSettings, Field, SecretStr, AnyUrl

class Settings(BaseSettings):
    google_api_key: SecretStr = Field(..., env="GOOGLE_API_KEY")

    gemini_model: str = Field("gemini-2.5-flash", env="GEMINI_MODEL")
    temperature: float = Field(0.1, env="GEMINI_TEMPERATURE")
    max_output_tokens: int = Field(2000, env="GEMINI_MAX_OUTPUT_TOKENS")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()