import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

path = os.path.abspath(os.environ.get("DOTENV_PATH", ".env"))
if os.path.exists(path):
    load_dotenv(dotenv_path=Path(__file__).parent / path)


class UvicornConfig(BaseSettings):
    PORT: int = 8080
    HOST: str = "0.0.0.0"

    WORKERS: int = 4
    RELOAD_ON_CHANGE: bool = False

    class Config:
        env_prefix = "UVICORN_"

class CONFIG:
    UVICORN = UvicornConfig()
