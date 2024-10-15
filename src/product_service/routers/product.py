from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import db_helper
from src.product_service.crud.product import ProductCRUD
from src.product_service.schemas.product import Product, ProductCreate, \
    ProductPartialUpdate
from src.users.dependencies import get_current_user, get_current_superuser
from src.users.models import User
from src.users.schemas import UserGet


router = APIRouter(prefix='/products', tags=["Products"])


@router.get(
    "/",
    response_model=list[Product]
)
async def get_products(
        user: User = Depends(get_current_user),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> list[Product]:
    """
     контроллер для получения списка ВСЕХ доступных продуктов
     (админ видит все, остальные пользователи видят только активные)
    """
    if user.is_superuser:
        return await ProductCRUD.get_all(session=session)
    else:
        return await ProductCRUD.get_all(session=session, is_active=True)


@router.post(
    "/",
    response_model=Product,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_superuser)],
)
async def create_product(
        product_in: ProductCreate,
        user: UserGet = Depends(get_current_user),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
) -> Product:
    """
    контроллер для создания продукта
    """
    if user.is_superuser:
        return await ProductCRUD.add(data=product_in, session=session)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")


@router.get(
    "/inactive",
    response_model=list[Product],
    dependencies=[Depends(get_current_superuser)],
)
async def get_inactive_products(
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
) -> list[Product]:
    """
     контроллер для получения списка ТОЛЬКО НЕАКТИВНЫх продуктов
     доступ только у админа
    """
    return await ProductCRUD.get_all(is_active=False, session=session)


@router.get(
    "/{product_id}",
)
async def get_product(
        product_id: int,
        user: UserGet = Depends(get_current_user),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
) -> Product | None:
    """
    контроллер для получения информации о продукте по id
    нужно сделать так, чтобы неактивные видел только админ
    """
    if user.is_superuser:
        return await ProductCRUD.get_one_or_none_by_id(data_id=product_id, session=session)
    else:
        product = await ProductCRUD.get_all(id=product_id, is_active=True, session=session)
        product = product[0] if product else None
    if product:
        return product
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Продукт не найден")


@router.patch(
    "/{product_id}",
    response_model=Product,
    dependencies=[Depends(get_current_superuser)],
)
async def update_product(
        product_partial_update: ProductPartialUpdate,
        product_id: int,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
) -> Product:
    """
    контрллер для частичного обновленея продукта
    доступ только у админа
    """
    return await ProductCRUD.update(
        data_id=product_id,
        data=product_partial_update,
        session=session
    )


@router.delete(
    "/{product_id}",
    response_model=None,
    dependencies=[Depends(get_current_superuser)],
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_product(
        product_id: int,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
) -> None:
    """
    контроллер для удаления продукта
    доступ только у админа
    """
    await ProductCRUD.delete(data_id=product_id, session=session)
