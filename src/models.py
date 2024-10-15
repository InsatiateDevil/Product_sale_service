from datetime import datetime

from fastapi import Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr

from src.database import db_helper


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + 's'

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(),
                                                 server_onupdate=func.now(),
                                                 onupdate=datetime.now)

    @classmethod
    async def find_by_id(
            cls, current_id: int,
            db: AsyncSession = Depends(db_helper.scoped_session_dependency)
    ):
        query = select(cls).where(cls.id == current_id)
        result = await db.execute(query)
        return result.scalars().first()