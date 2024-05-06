from multiprocessing import Queue, Manager

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite+aiosqlite:///base.db"
    # database_url = "sqlite+aiosqlite:///:memory:"
    echo_sql: bool = True
    test: bool = False
    project_name: str = "Certi Checker"
    oauth_token_secret: str = "my_dev_secret"
    log_level: str = "DEBUG"


settings = Settings()  # type: ignore
