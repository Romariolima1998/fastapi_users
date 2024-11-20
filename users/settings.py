from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    model_config =SettingsConfigDict(env_file='.env', env_file_encoding="utf-8", extra="ignore")

    DATABASE_URL: str
    DATABASE_URL_ALEMBIC: str
    TOKEN_EXPIRE: int
    SECRET_KEY: str
    ALGORITHM: str
    EMAIL: str
    PASSWORD: str

    #class Config:
    #    env_file = '.env'