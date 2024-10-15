from typing import Optional

from pydantic import BaseModel, ConfigDict


# CartItem schemas
class CartItemBase(BaseModel):
    product_id: int
    quantity: int | None = 1


class CartItemUpdate(BaseModel):
    quantity: int | None = None


class CartItem(CartItemBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    card_id: Optional[int]


class CartItemCreate(CartItemBase):
    id: int | None = None
    cart_id: int | None = None


class CartItemGet(CartItemBase):
    pass
