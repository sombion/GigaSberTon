from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BOT_TOKEN: str

    RABBIT_HOST: str
    RABBIT_PORT: int


    model_config = SettingsConfigDict(env_file='.env')

settings = Settings()