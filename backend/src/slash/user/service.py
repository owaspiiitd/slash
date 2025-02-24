import logging
from typing import Annotated, Any

import httpx
import jwt
from fastapi import Depends, Header, HTTPException, status
from pydantic import BaseModel

from core.config import CONFIG

from .models import User

logger = logging.getLogger("COMMON_USER_SERVICE")


class AuthToken(BaseModel):
    __algorithm = "HS256"

    data: dict[str, Any]

    def to_jwt(self) -> str:
        return jwt.encode(self.data, key=CONFIG.FIREBASE.JWT_KEY, algorithm=self.__algorithm)

    @classmethod
    def from_jwt(cls, access_token: str):
        data = jwt.decode(access_token, CONFIG.FIREBASE.JWT_KEY, algorithms=[cls.__algorithm, "RS256"])
        return cls(data=data)

    @classmethod
    def __from_jwt_unsafe(cls, access_token: str):
        return cls(data=jwt.decode(access_token, "", algorithms=["RS256"], options={"verify_signature": False}))

    @classmethod
    async def validate_firebase_token(cls, token: str):
        try:
            async with httpx.AsyncClient() as client:
                res = await client.post(
                    f"https://identitytoolkit.googleapis.com/v1/accounts:lookup?key={CONFIG.FIREBASE.API_KEY}",
                    json={"idToken": token},
                )
            if res.status_code != 200:
                logger.error(f"Firebase token lookup failed: {res.status_code} - {res.text}")
                return None, None
            # Decode token without verifying for extracting fields (do not use unverified decode in production)
            data = cls.__from_jwt_unsafe(token)
            # Wrap token data into a simple object for attribute-style access
            return str(res.json()["users"][0]["email"]).lower(), data
        except Exception as e:
            logger.exception("Error validating firebase token")
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
