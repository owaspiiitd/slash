from typing import Annotated

import motor.motor_asyncio
from beanie import init_beanie
from fastapi import Depends

from core.config import CONFIG
from slash.user.models import User


def get_mongodb_url() -> str:
    return f"mongodb://{CONFIG.DB.USER}:{CONFIG.DB.PASSWORD}@{CONFIG.DB.HOST}:{CONFIG.DB.PORT}/{CONFIG.DB.NAME}"


# Initialize the MongoDB client
client = None
db = None


async def init_db():
    global client, db

    mongodb_url = get_mongodb_url()
    client = motor.motor_asyncio.AsyncIOMotorClient(
        mongodb_url,
        maxPoolSize=max(1, CONFIG.DB.POOL_SIZE // CONFIG.UVICORN.WORKERS),
        serverSelectionTimeoutMS=180000,
    )
    db = client[CONFIG.DB.NAME]

    await init_beanie(database=db, document_models=[User])


async def get_db():
    global db
    if db is None:
        await init_db()
    return db


DBSession = Annotated[motor.motor_asyncio.AsyncIOMotorDatabase, Depends(get_db)]
