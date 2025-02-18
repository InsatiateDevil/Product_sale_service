from fastapi import FastAPI

from src.product_service.routers.cart import router as cart_router
from src.product_service.routers.cartitem import router as cartitem_router
from src.product_service.routers.product import router as product_router
from src.users.router import router as user_router

app = FastAPI(
    title="My First FastAPI-app",
)
app.include_router(user_router)
app.include_router(product_router)
app.include_router(cart_router)
app.include_router(cartitem_router)
