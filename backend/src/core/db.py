import urllib.parse
from typing import AsyncGenerator

import motor.motor_asyncio
from beanie import init_beanie

from core.config import CONFIG
from slash.user import User


def get_mongodb_url() -> str:
    username = urllib.parse.quote_plus(CONFIG.DB.USER)
    password = urllib.parse.quote_plus(CONFIG.DB.PASSWORD)

    if CONFIG.DB.IS_CLOUD:
        return f"mongodb+srv://{username}:{password}@{CONFIG.DB.HOST}/{CONFIG.DB.NAME}"
    else:
        return f"mongodb://{username}:{password}@{CONFIG.DB.HOST}:{CONFIG.DB.PORT}/{CONFIG.DB.NAME}"


async def init_db():
    mongodb_url = get_mongodb_url()
    client = motor.motor_asyncio.AsyncIOMotorClient(
        mongodb_url,
        maxPoolSize=max(1, CONFIG.DB.POOL_SIZE // CONFIG.UVICORN.WORKERS),
        serverSelectionTimeoutMS=180000,
    )
    db = client.db_name

    await init_beanie(database=db, document_models=[User])
