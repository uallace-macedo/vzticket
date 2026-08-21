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

    AUTH_COOKIE_NAME: str = ''
    WALLET_CLAIM_EXP_MINUTES: int = 15

    WEB_URL: str = ''

    TMDB_BASE_URL: str = ''
    TMDB_API_KEY: str = ''
    TMDB_IMAGE_BASE_URL: str = ''

    @property
    def DATABASE_URL(self) -> str:
        return f'postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}'

    @property
    def AUTH_COOKIE_MAX_AGE(self) -> int:
        return self.JWT_TOKEN_EXP_MINUTES * 60

    @property
    def IS_SECURE_COOKIE(self) -> bool:
        return self.WEB_URL.startswith('https://')


settings = Settings()
