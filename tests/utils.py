import json

from sqlalchemy.ext.asyncio import AsyncSession

from src.product_service.models import Cart, CartItem, Product
from src.users.models import User


async def load_prepared_data(data_path, session: AsyncSession):
    with open(data_path, 'r', encoding='utf-8') as file:
        json_data = json.load(file)

    for item in json_data:
        if item['model'] == 'User':
            user = User(
                id=item.get('id'),
                full_name=item['fields'].get('full_name'),
                email=item['fields'].get('email'),
                phone=item['fields'].get('phone'),
                hashed_password=item['fields'].get('hashed_password'),
                is_active=item['fields'].get('is_active'),
                is_superuser=item['fields'].get('is_superuser')
            )
            session.add(user)

    for item in json_data:
        if item['model'] == 'Cart':
            cart = Cart(
                id=item.get('id'),
                user_id=item['fields'].get('user_id')
            )
            session.add(cart)

    for item in json_data:
        if item['model'] == 'CartItem':
            cartitem = CartItem(
                id=item.get('id'),
                cart_id=item['fields'].get('cart_id'),
                product_id=item['fields'].get('product_id'),
                quantity=item['fields'].get('quantity')
            )
            session.add(cartitem)

    for item in json_data:
        if item['model'] == 'Product':
            product = Product(
                id=item.get('id'),
                name=item['fields'].get('name'),
                description=item['fields'].get('description'),
                price=item['fields'].get('price'),
                is_active=item['fields'].get('is_active')
            )
            session.add(product)

    await session.commit()
