from src.crud import BaseCRUD
from src.product_service.models import Product


class ProductCRUD(BaseCRUD):
    model = Product

# from sqlalchemy import select, Result
# from sqlalchemy.ext.asyncio import AsyncSession
#
# from src.product_service.models import Product
# from src.product_service.schemas.product import ProductCreate, ProductUpdate, \
#     ProductPartialUpdate
# from src.users.schemas import UserRead
#
#
# async def get_products(session: AsyncSession, user: UserRead) -> list[Product]:
#     if user.is_superuser :
#         stmt = select(Product).order_by(Product.id)
#     else:
#         stmt = select(Product).order_by(Product.id).where(Product.is_active==True)
#     result: Result = await session.execute(stmt)
#     products = result.scalars().all()
#     return list(products)
#
#
# async def get_inactive_products(session: AsyncSession) -> list[Product]:
#     stmt = select(Product).order_by(Product.id).where(Product.is_active==False)
#     result: Result = await session.execute(stmt)
#     products = result.scalars().all()
#     return list(products)
#
#
# async def get_product(
#         session: AsyncSession,
#         product_id: int
# ) -> Product | None:
#     return await session.get(Product, product_id)
#
#
# async def create_product(
#         session: AsyncSession,
#         product_in: ProductCreate
# ) -> Product:
#     product = Product(**product_in.model_dump())
#     session.add(product)
#     await session.commit()
#     # await session.refresh(product)
#     return product
#
#
# async def update_product(
#         session: AsyncSession,
#         product: Product,
#         product_update: ProductUpdate | ProductPartialUpdate,
#         partial: bool = False,
# ) -> Product:
#     for name, value in product_update.model_dump(exclude_unset=partial).items():
#         setattr(product, name, value)
#     await session.commit()
#     # await session.refresh(product)
#     return product
#
#
# # async def partial_update_product(
# #         session: AsyncSession,
# #         product: Product,
# #         product_partial_update: ProductPartialUpdate
# # ) -> Product:
# #     for name, value in product_partial_update.model_dump(exclude_unset=True).items():
# #         setattr(product, name, value)
# #     await session.commit()
# #     # await session.refresh(product)
# #     return product
#
# async def delete_product(
#         session: AsyncSession,
#         product: Product,
# ) -> None:
#     await session.delete(product)
#     await session.commit()
