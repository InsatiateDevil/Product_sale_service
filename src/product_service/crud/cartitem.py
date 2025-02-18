from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud import BaseCRUD
from src.product_service.crud.product import ProductCRUD
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

    @classmethod
    async def add(
            cls,
            data,
            session: AsyncSession,
    ):
        await ProductCRUD.get_active_product_by_id(data.product_id, session)
        new_object = cls.model(**data.model_dump())
        session.add(new_object)
        try:
            await session.commit()
            await session.refresh(new_object)
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return new_object
