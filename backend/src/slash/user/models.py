from uuid import uuid4

from beanie import Document
from pydantic import EmailStr, Field


class User(Document):
    id: str = Field(default_factory=lambda: uuid4().hex)
    name: str
    email: EmailStr
    photo_url: str | None = None

    class Settings:
        name = "users"
        indexes = [
            "email",
        ]
