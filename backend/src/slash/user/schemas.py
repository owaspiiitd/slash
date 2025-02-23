from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    name: str
    email: EmailStr
    photo_url: str | None = None


class UserCreate(BaseModel):
    # The Google token (from OAuth2 login) that will be validated via Firebase
    google_token: str


class UserSchema(UserBase):
    id: str

    class Config:
        from_attributes = True
