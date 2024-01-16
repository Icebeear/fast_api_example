import os
from pathlib import Path
from dotenv import load_dotenv

from pydantic import Field
from pydantic_settings import BaseSettings

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

BASE_DIR = Path(__file__).parent.parent


origins = [
    "http://127.0.0.1:8000/",
    "http://localhost:8080",
    "http://localhost",
]

methods = [
    "GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"
]

headers = [
    "Content-Type",
    "Set-Cookie",
    "Access-Control-Allow-Headers",
    "Access-Control-Allow-Origin",
    "Authorization",
]


class AppSettings(BaseSettings):
    api_v1_prefix: str = "/api/v1"
    debug: bool = False 
    db_url: str = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    cors_allow_origins: list[str] = Field(default=origins, exclude=True)
    cors_allow_credentials: bool = Field(default=True, exclude=True)
    cors_allow_methods: list[str] = Field(default=methods, exclude=True)
    cors_allow_headers: list[str] = Field(default=headers, exclude=True)

    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    

settings = AppSettings()

'''
миграции не работают если в url есть +asyncpg 
но если после миграций не добавить +asyncpg то приложение даже не запуститься, 
потому что круды написано асинхронно
'''
