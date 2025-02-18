from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import jwt
from passlib.context import CryptContext
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.users.crud import UsersCRUD


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode.update({"exp": expire})
    auth_data = settings.auth_data
    encode_jwt = jwt.encode(to_encode, auth_data['secret_key'],
                            algorithm=auth_data['algorithm'])
    return encode_jwt


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(
        email: EmailStr,
        password: str,
        phone: str,
        session: AsyncSession
):
    if email and email is not Optional[str]:
        user = await UsersCRUD.get_user_by_email(email=email, session=session)
    else:
        user = await UsersCRUD.get_user_by_phone(phone=phone, session=session)
    if not user or verify_password(plain_password=password, hashed_password=user.hashed_password) is False:
        return None
    return user
