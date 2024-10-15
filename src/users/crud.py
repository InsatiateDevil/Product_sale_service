from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud import BaseCRUD
from src.product_service.models import Cart
from src.users.models import User


class UsersCRUD(BaseCRUD):
    model = User

    @staticmethod
    async def get_user_by_email(email: EmailStr, session: AsyncSession):
        query = select(User).filter(User.email == email)
        user = await session.execute(query)
        return user.scalars().first()

    @staticmethod
    async def get_user_by_phone(phone: str, session: AsyncSession):
        query = select(User).filter(User.phone == phone)
        user = await session.execute(query)
        return user.scalars().first()

    @classmethod
    async def add(cls, data, session: AsyncSession):
        from src.users.auth import get_password_hash
        user_dict = data.model_dump()
        user_dict['hashed_password'] = get_password_hash(data.password)
        del user_dict['password']
        new_user = cls.model(**user_dict)
        cart = Cart(user=new_user)
        session.add(new_user)
        session.add(cart)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return new_user
