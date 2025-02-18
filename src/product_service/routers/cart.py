from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import db_helper
from src.product_service.crud.cart import CartCRUD
from src.product_service.crud.cartitem import CartItemCRUD
from src.product_service.utils import get_cart_price
from src.users.dependencies import get_current_user
from src.users.models import User
from src.users.schemas import UserGet

router = APIRouter(prefix='/cart', tags=["Cart"])


@router.get(
    "/",
    response_model=None,
)
async def get_cart(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    user: User = Depends(get_current_user)
):
    """
    контроллер для просмотра корзины
    """
    cart = await CartCRUD.get_one_or_none_by_id(data_id=user.id, session=session)
    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found")
    cartitems = await CartItemCRUD.get_all(cart_id=cart.id, session=session)
    total_price = get_cart_price(cartitems)
    return {
        "cart_items": [
            {"product_id": item.product_id,
             "quantity": item.quantity} for item in cartitems],
        "total_price": total_price
    }


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_cart(
        session: Annotated[AsyncSession, Depends(db_helper.scoped_session_dependency)],
        user: UserGet = Depends(get_current_user)
) -> None:
    cart = await CartCRUD.get_one_or_none_by_id(data_id=user.id, session=session)
    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cart not found")
    cartitems = await CartItemCRUD.get_all(cart_id=cart.id, session=session)
    for cartitem in cartitems:
        await session.delete(cartitem)
        await session.commit()
