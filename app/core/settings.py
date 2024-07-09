from pydantic_settings import BaseSettings, SettingsConfigDict

class PostgresSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )

    DB_HOSTNAME: str
    DB_PORT: int
    DB_PASSWORD: str
    DB_NAME: str
    DB_USERNAME: str

    def __str__(self):
        return f"postgresql://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOSTNAME}:{self.DB_PORT}/{self.DB_NAME}"

class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )

    REDIS_HOSTNAME: str
    REDIS_PORT: int

    def __str__(self):
        return f'redis://{self.REDIS_HOSTNAME}:{self.REDIS_PORT}/0'

postgres_settings = PostgresSettings()
redis_settings = RedisSettings()