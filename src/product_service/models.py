from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.models import Base

if TYPE_CHECKING:
    from src.users.models import User


class Product(Base):
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=False)
    cart_items: Mapped[list["CartItem"]] = relationship("CartItem", back_populates="product", lazy='selectin')


class Cart(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    user: Mapped["User"] = relationship("User", back_populates="cart", single_parent=True, lazy='selectin')
    cart_items: Mapped[list["CartItem"]] = relationship("CartItem", back_populates="cart", lazy='selectin')


class CartItem(Base):
    cart_id: Mapped[int] = mapped_column(ForeignKey("carts.id", ondelete="CASCADE"))
    cart: Mapped["Cart"] = relationship("Cart", back_populates="cart_items")
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"))
    product: Mapped["Product"] = relationship("Product", back_populates="cart_items", lazy='selectin')
    quantity: Mapped[int] = mapped_column(nullable=False)
