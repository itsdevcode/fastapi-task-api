from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "TASK MGMT"
    VERSION: str = "1.1.1"
    ENVIRONMENT: str = "development"
    DATABASE_URL: str
    DEBUG: bool = False
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    model_config = SettingsConfigDict(
        env_file=".env"
    )
settings = Settings()