import logging
from typing import Annotated

import httpx
import jwt
from fastapi import Depends, Header, HTTPException, status

from core.config import CONFIG

from .models import User

logger = logging.getLogger("COMMON_USER_SERVICE")


class AuthToken:
    __algorithm = "HS256"

    def __init__(self, data: dict):
        self.data = data

    def to_jwt(self) -> str:
        return jwt.encode(self.data, key=CONFIG.FIREBASE.JWT_KEY, algorithm=self.__algorithm)

    @classmethod
    def from_jwt(cls, access_token: str):
        data = jwt.decode(access_token, CONFIG.FIREBASE.JWT_KEY, algorithms=[cls.__algorithm, "RS256"])
        return cls(data=data)

    @classmethod
    async def validate_firebase_token(cls, token: str):
        try:
            async with httpx.AsyncClient() as client:
                res = await client.post(
                    f"https://identitytoolkit.googleapis.com/v1/accounts:lookup?key={CONFIG.FIREBASE.API_KEY}",
                    data={"idToken": token},
                )
            if res.status_code != 200:
                return None, None
            # Decode token without verifying for extracting fields (do not use unverified decode in production)
            data = jwt.decode(token, options={"verify_signature": False})
            # Wrap token data into a simple object for attribute-style access
            TokenData = type("TokenData", (), {"data": data})
            return str(res.json()["users"][0]["email"]).lower(), TokenData
        except Exception:
            return None, None


async def get_user(authorization: str = Header(...)):
    if "Bearer " in authorization:
        token = authorization.replace("Bearer", "").strip()
    else:
        token = authorization.strip()
    try:
        auth_token = AuthToken.from_jwt(token)
        email = auth_token.data.get("email")
        user = await User.find_one(User.email == email)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from e


CurrentUser = Annotated[User, Depends(get_user)]
