from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import db_helper
from src.product_service.crud.cart import CartCRUD
from src.product_service.crud.cartitem import CartItemCRUD
from src.product_service.schemas.cartitem import CartItemUpdate, CartItemCreate, CartItemGet
from src.product_service.utils import get_cart_price
from src.users.dependencies import get_current_user
from src.users.schemas import UserGet

router = APIRouter(prefix='/cart_item', tags=["CartItem"])


@router.get(
    '/'
)
async def get_cartitems(
        user: Annotated[UserGet, Depends(get_current_user)],
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    cart = await CartCRUD.get_one_or_none_by_id(data_id=user.id,
                                                session=session)
    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cart not found")
    cartitems = await CartItemCRUD.get_all(cart_id=cart.id, session=session)
    total_price = get_cart_price(cartitems)
    return {"cart_items": [{"product_id": item.product_id,
                            "quantity": item.quantity} for item in cartitems],
            "total_price": total_price}


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=CartItemGet,
)
async def add_cartitems(
        cartitem_in: CartItemCreate,
        user: Annotated[UserGet, Depends(get_current_user)],
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    cart = await CartCRUD.get_one_or_none_by_id(data_id=user.id, session=session)
    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cart not found")
    cartitem_from_cart = await CartItemCRUD.get_by_product_id(
        product_id=cartitem_in.product_id,
        session=session
    )
    if cartitem_from_cart:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Product already in cart")
    else:
        cartitem_in.cart_id = cart.id
        cartitem_add = await CartItemCRUD.add(data=cartitem_in, session=session)
        return cartitem_add


@router.patch(
    '/{product_id}',
    response_model=CartItemGet,
)
async def update_cartitem(
        product_id: int,
        cart_item_in: CartItemUpdate,
        user: Annotated[UserGet, Depends(get_current_user)],
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    cart = await CartCRUD.get_one_or_none_by_id(data_id=user.id, session=session)
    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found")

    cart_item = await CartItemCRUD.get_by_product_id(product_id=product_id, session=session)
    if not cart_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found in cart")

    cart_item.quantity = cart_item_in.quantity
    await session.commit()
    return cart_item


@router.delete(
    '/{product_id}',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_cartitem(
        product_id: int,
        user: Annotated[UserGet, Depends(get_current_user)],
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    cart = await CartCRUD.get_one_or_none_by_id(data_id=user.id, session=session)
    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found")

    cart_item = await CartItemCRUD.get_by_product_id(product_id=product_id, session=session)
    if cart_item:
        await session.delete(cart_item)
        await session.commit()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")
