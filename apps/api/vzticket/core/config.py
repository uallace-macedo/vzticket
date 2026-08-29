from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )

    app_name: str = 'VzTicket API'
    debug: bool = False

    database_host: str = 'localhost'
    database_port: int = 5432
    database_user: str = 'postgres'
    database_password: str = 'postgres'
    database_name: str = 'vzticket'

    @computed_field
    def database_url(self) -> str:
        return f'postgresql+asyncpg://{self.database_user}:{self.database_password}@{self.database_host}:{self.database_port}/{self.database_name}'

    secret_key: str = 'change-me-in-production'
    algorithm: str = 'HS256'
    access_token_expire_minutes: int = 15
    refresh_token_expire_minutes: int = 720

    qr_code_hmac_secret: str = 'change-me-in-production'


settings = Settings()
