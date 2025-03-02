from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, ORJSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from common.exceptions import custom_http_exception_handler, validation_exception_handler
from core.config import CONFIG
from core.db import init_db
from slash.user import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(title="Slash API", version="1.0.0", default_response_class=ORJSONResponse, lifespan=lifespan)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:9000",
    "https://slash.win",
    "https://play.slash.win",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)

app.add_exception_handler(StarletteHTTPException, custom_http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

app.include_router(user_router)


@app.get("/")
async def root():
    return {"message": "Welcome to Slash API"}


if __name__ == "__main__":
    uvicorn.run(
        "api:app",
        host=CONFIG.UVICORN.HOST,
        port=CONFIG.UVICORN.PORT,
        workers=CONFIG.UVICORN.WORKERS,
        reload=CONFIG.UVICORN.RELOAD_ON_CHANGE,
    )
