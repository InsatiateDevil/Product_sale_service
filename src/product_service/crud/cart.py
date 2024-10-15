from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud import BaseCRUD
from src.product_service.models import Cart


class CartCRUD(BaseCRUD):
    model = Cart

    @classmethod
    async def get_one_or_none_by_id(
            cls,
            data_id: int,
            session: AsyncSession
    ):
        query = select(cls.model).filter_by(user_id=data_id)
        result = await session.execute(query)
        return result.scalars().first()
