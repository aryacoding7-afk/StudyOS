from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # ======================================================
    # Database
    # ======================================================

    DATABASE_URL: str
    TEST_DATABASE_URL: str
    REDIS_URL: str

    # ======================================================
    # Authentication
    # ======================================================

    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # ======================================================
    # AI
    # ======================================================

    GEMINI_API_KEY: str = ""

    EMBEDDING_MODEL: str = "BAAI/bge-small-en-v1.5"

    LLM_MODEL: str = "gemini-2.5-flash"

    TOP_K: int = 5

    TEMPERATURE: float = 0.2

    MAX_OUTPUT_TOKENS: int = 2048

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()