from pydantic_settings import BaseSettings, SettingsConfigDict
from faststream.rabbit.fastapi import RabbitRouter


class Settings(BaseSettings):
    GIGACHAT_CREDENTIALS: str
    MODEL: str
    SCOPE: str

    model_config = SettingsConfigDict(env_file='.env')

router = RabbitRouter()

settings = Settings()