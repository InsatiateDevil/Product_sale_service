from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions import ObjectDoesNotExist


class BaseCRUD:
    model = None

    @classmethod
    async def get_all(
            cls,
            session: AsyncSession,
            **filter_by):
        query = select(cls.model).filter_by(**filter_by)
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def get_one_or_none_by_id(
            cls,
            data_id: int,
            session: AsyncSession,
    ):
        obj = await session.get(cls.model, data_id)
        return obj

    @classmethod
    async def add(
            cls,
            data,
            session: AsyncSession,
    ):
        new_object = cls.model(**data.model_dump())
        session.add(new_object)
        try:
            await session.commit()
            await session.refresh(new_object)
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return new_object

    @classmethod
    async def update(
            cls,
            data_id: int,
            data,
            session: AsyncSession,
    ):
        old_object = await session.get(cls.model, data_id)
        if not old_object:
            raise ObjectDoesNotExist
        for key, value in data.model_dump().items():
            if value:
                setattr(old_object, key, value)
        await session.commit()
        await session.refresh(old_object)
        return old_object

    @classmethod
    async def delete(
            cls,
            data_id: int,
            session: AsyncSession,
    ):
        old_object = await session.get(cls.model, data_id)
        if not old_object:
            raise ObjectDoesNotExist
        await session.delete(old_object)
        await session.commit()
