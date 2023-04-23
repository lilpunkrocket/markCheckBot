from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    bot_token: SecretStr
    api: str

    class Config:
        env_file = ".env"


settings = Settings()
