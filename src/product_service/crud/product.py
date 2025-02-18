from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud import BaseCRUD
from src.product_service.models import Product


class ProductCRUD(BaseCRUD):
    model = Product

    @classmethod
    async def get_active_product_by_id(
            cls,
            data_id: int,
            session: AsyncSession,
    ):
        query = select(cls.model).where(cls.model.id == data_id, cls.model.is_active)
        obj = await session.execute(query)
        obj = obj.scalars().first()
        if obj is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Product not found'
            )
        return obj
