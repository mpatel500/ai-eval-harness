from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    anthropic_api_key: str
    model: str = "claude-haiku-4-5"
    max_tokens: int = 1024
    input_price_per_mtok: float = 1.0
    output_price_per_mtok: float = 5.0

settings = Settings() # pyright: ignore[reportCallIssue]
