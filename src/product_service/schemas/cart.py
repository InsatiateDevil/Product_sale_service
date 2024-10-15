from pydantic import BaseModel
from src.product_service.schemas.cartitem import CartItem


# Cart schemas
class CartBase(BaseModel):
    user_id: int


class CartCreate(CartBase):
    pass


class Cart(CartBase):
    id: int
    cart_items: list["CartItem"] | None = None
    total_price: int


class CartGet(BaseModel):
    cart_items: list["CartItem"] | None = None
    total_price: int
