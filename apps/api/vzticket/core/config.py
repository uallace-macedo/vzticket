from datetime import timedelta

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

    web_url: str = 'http://localhost:5173'

    # Database
    database_host: str = 'localhost'
    database_port: int = 5432
    database_user: str = 'postgres'
    database_password: str = 'postgres'
    database_name: str = 'vzticket'

    # Security & Tokens
    secret_key: str = 'change-me-in-production'
    algorithm: str = 'HS256'
    access_token_expire_minutes: int = 15
    refresh_token_expire_minutes: int = 720

    qr_code_hmac_secret: str = 'change-me-in-production'

    # --- COMPUTED FIELDS ---

    @computed_field
    def database_url(self) -> str:
        """Asynchronous PostgreSQL connection URL for SQLAlchemy."""
        return f'postgresql+asyncpg://{self.database_user}:{self.database_password}@{self.database_host}:{self.database_port}/{self.database_name}'

    @computed_field
    def is_production(self) -> bool:
        """Returns True if running under HTTPS and with debug disabled."""
        return self.web_url.startswith('https://') and not self.debug

    @computed_field
    def cors_origins(self) -> list[str]:
        """Generates allowed CORS origins list from the web URL."""
        return [self.web_url]

    @computed_field
    def cookie_secure(self) -> bool:
        """Ensures the cookie secure flag is active only in production (HTTPS)."""
        return self.is_production

    @computed_field
    def cookie_samesite(self) -> str:
        """Defines the SameSite policy ('none' for cross-site prod, 'lax' for local dev)."""
        return 'none' if self.is_production else 'lax'

    @computed_field
    def access_token_expire_seconds(self) -> int:
        """Access token expiration duration in seconds (for cookie max_age)."""
        return self.access_token_expire_minutes * 60

    @computed_field
    def refresh_token_expire_seconds(self) -> int:
        """Refresh token expiration duration in seconds (for cookie max_age)."""
        return self.refresh_token_expire_minutes * 60

    @computed_field
    def access_token_timedelta(self) -> timedelta:
        """Timedelta instance ready for JWT access token encoding."""
        return timedelta(minutes=self.access_token_expire_minutes)

    @computed_field
    def refresh_token_timedelta(self) -> timedelta:
        """Timedelta instance ready for JWT refresh token encoding."""
        return timedelta(minutes=self.refresh_token_expire_minutes)


settings = Settings()
