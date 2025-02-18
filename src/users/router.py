from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response

from src.database import db_helper
from src.exceptions import UserAlreadyExists, IncorrectEmailOrPassword
from src.users.auth import authenticate_user, create_access_token
from src.users.crud import UsersCRUD
from src.users.dependencies import get_current_user, get_current_superuser
from src.users.models import User
from src.users.schemas import UserCreate, UserLogin, UserGet, \
    UserCreateSuperUser

router = APIRouter(prefix="/users", tags=["Работа с пользователями"])


@router.post(
    "/register/",
    summary="Зарегистрировать пользователя"
)
async def register_user(
        user_data: UserCreate,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
) -> dict:
    if user_data.email:
        user_by_email = await UsersCRUD.get_all(email=user_data.email, session=session)
        user_by_phone = await UsersCRUD.get_all(phone=user_data.phone, session=session)
        if user_by_email or user_by_phone:
            raise UserAlreadyExists
    await UsersCRUD.add(data=user_data, session=session)
    return {'message': 'Вы успешно зарегистрированы!'}


@router.post(
    "/login/",
    summary="Войти в систему"
)
async def login_user(
        response: Response,
        user_data: UserLogin,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
) -> dict:
    user = await authenticate_user(email=user_data.email,
                                   phone=user_data.phone,
                                   password=user_data.password,
                                   session=session)
    if user is None:
        raise IncorrectEmailOrPassword
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie(key="Authorization", value=access_token, httponly=True)
    return {"access_token": access_token}


@router.post(
    "/logout/",
    summary="Выйти из системы"
)
async def logout_user(
        response: Response
):
    response.delete_cookie(key="Authorization")
    return {"message": "Выход прошел успешно"}


@router.get(
    "/all_users/",
    summary="Получить всех пользователей",
    dependencies=[Depends(get_current_superuser)]
)
async def get_all_users(
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await UsersCRUD.get_all(session=session)


@router.get(
    "/me/",
    summary="Получить информацию о текущем пользователе",
    response_model=UserGet
)
async def get_me(
        user_data: User = Depends(get_current_user)
):
    return user_data


@router.post(
    '/register_superuser/',
    include_in_schema=False
)
async def register_superuser(
        user_data: UserCreateSuperUser,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    if user_data.email:
        user_by_email = await UsersCRUD.get_all(email=user_data.email, session=session)
        user_by_phone = await UsersCRUD.get_all(phone=user_data.phone, session=session)
        if user_by_email or user_by_phone:
            raise UserAlreadyExists
    await UsersCRUD.add(data=user_data, session=session)
    return {'message': 'Вы успешно зарегистрированы!'}
