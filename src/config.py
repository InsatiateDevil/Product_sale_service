import os
from pathlib import Path

from pydantic_settings import BaseSettings
from dotenv import load_dotenv


BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    load_dotenv()
    db_name: str = os.getenv('POSTGRES_DB')
    db_user: str = os.getenv('POSTGRES_USER')
    db_pass: str = os.getenv('POSTGRES_PASSWORD')
    db_host: str = os.getenv('POSTGRES_HOST')
    db_port: int = os.getenv('POSTGRES_PORT')
    db_url: str = f'postgresql+asyncpg://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'
    db_echo: bool = os.getenv('DB_ECHO', False) == 'True'
    SECRET_KEY: str = os.getenv('SECRET_KEY')
    ALGORITHM: str = os.getenv('ALGORITHM')
    REFRESH_TOKEN_EXPIRES_MINUTES: int = int(os.getenv('REFRESH_TOKEN_EXPIRES_MINUTES'))
    ACCESS_TOKEN_EXPIRES_MINUTES: int = int(os.getenv('ACCESS_TOKEN_EXPIRES_MINUTES'))
    auth_data: dict = {"secret_key": SECRET_KEY, "algorithm": ALGORITHM}


settings = Settings()
