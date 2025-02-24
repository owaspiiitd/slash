from datetime import datetime, timedelta

from fastapi import APIRouter

from common.exceptions import UnauthorizedException
from core.db import DBSession

from .models import User
from .schemas import UserCreate, UserSchema
from .service import AuthToken, CurrentUser

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/me", response_model=UserSchema)
async def get_me(user: CurrentUser):
    return user


@router.post("/register", response_model=UserSchema)
async def register_user(user_data: UserCreate, db_session: DBSession):
    email, token_data = await AuthToken.validate_firebase_token(user_data.google_token)
    if not email:
        raise UnauthorizedException(detail="Invalid Google token")
    existing_user = await User.find_one(User.email == email)
    if existing_user:
        return existing_user
    new_user = User(
        name=token_data.data.get("name", "Anonymous"),
        email=email,
        photo_url=token_data.data.get("picture"),
    )
    await new_user.insert()
    return new_user


@router.post("/login")
async def login_user(user_data: UserCreate, db_session: DBSession):
    email, token_data = await AuthToken.validate_firebase_token(user_data.google_token)
    if not email or not token_data:
        raise UnauthorizedException(detail="Invalid Google token")
    existing_user = await User.find_one(User.email == email)
    if not existing_user:
        existing_user = User(
            name=token_data.data.get("name", "Anonymous"),
            email=email,
            photo_url=token_data.data.get("picture"),
        )
        await existing_user.insert()
    jwt_token = AuthToken(
        data={
            "email": existing_user.email,
            "exp": datetime.utcnow() + timedelta(days=365),
        }
    ).to_jwt()
    return {"access_token": jwt_token, "token_type": "bearer"}
