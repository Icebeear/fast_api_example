import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

BASE_DIR = Path(__file__).parent.parent


# class AuthJWT(BaseModel):
#     private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
#     public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
#     algorithm: str = "RS256"
#     access_token_expire_minutes: int = 15
    

class AppSettings(BaseSettings):
    api_v1_prefix: str = "/api/v1"
    debug: bool = False 
    db_url: str = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    # auth_jwt: AuthJWT = AuthJWT()


settings = AppSettings()
