from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud import BaseCRUD
from src.product_service.models import CartItem


class CartItemCRUD(BaseCRUD):
    model = CartItem

    @classmethod
    async def get_all(
            cls,
            session: AsyncSession,
            **filter_by
    ):
        query = select(cls.model).filter_by(**filter_by)
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def get_by_product_id(
            cls,
            product_id: int,
            session: AsyncSession,
    ):
        query = select(cls.model).filter(cls.model.product_id == product_id)
        result = await session.execute(query)
        return result.scalars().first()
