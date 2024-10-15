from datetime import datetime, timezone

from fastapi import Request, HTTPException, status, Depends
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.database import db_helper
from src.exceptions import TokenExpired, NoJwtException, NoUserIdException, \
    ForbiddenException, TokenNoFound
from src.users.crud import UsersCRUD
from src.users.models import User
from src.users.schemas import UserGet


def get_token(request: Request):
    token = request.cookies.get('Authorization')
    if not token:
        raise TokenNoFound
    return token


async def get_current_user(
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
        token: str = Depends(get_token),
) -> UserGet:
    try:
        auth_data = settings.auth_data
        payload = jwt.decode(token, auth_data['secret_key'],
                             algorithms=auth_data['algorithm'])
    except JWTError:
        raise NoJwtException

    expire: str = payload.get('exp')
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise TokenExpired

    user_id: str = payload.get('sub')
    if not user_id:
        raise NoUserIdException

    user = await UsersCRUD.get_one_or_none_by_id(data_id=int(user_id), session=session)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Пользователь не найден')
    return user


def get_current_superuser(current_user: User = Depends(get_current_user)):
    if current_user.is_superuser:
        return current_user
    raise ForbiddenException
