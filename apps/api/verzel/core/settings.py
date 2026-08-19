from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )

    POSTGRES_USER: str = ''
    POSTGRES_PASSWORD: str = ''
    POSTGRES_DB: str = ''
    POSTGRES_PORT: int = 6000
    POSTGRES_HOST: str = ''

    JWT_SECRET_KEY: str = ''
    JWT_ALGORITHM: str = ''
    JWT_TOKEN_EXP_MINUTES: int = 40

    @property
    def database_url(self) -> str:
        return f'postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}'


settings = Settings()
