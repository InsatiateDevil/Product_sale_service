import pytest
from httpx import AsyncClient


# Users block
@pytest.mark.asyncio(loop_scope="session")
async def test_register_user(unauthorized_client_fixture: AsyncClient):
    response = await unauthorized_client_fixture.post(
        "/users/register/",
        json={
            "full_name": "User",
            "email": "user1@mail.ru",
            "phone": "+79999999999",
            "password": "Useruser1!"
        }
    )
    assert response.status_code == 200
    assert response.json() == {"message": 'Вы успешно зарегистрированы!'}


@pytest.mark.asyncio(loop_scope="session")
async def test_login_user_by_email(unauthorized_client_fixture: AsyncClient):
    response = await unauthorized_client_fixture.post(
        "/users/login/",
        json={
            "email": "user1@mail.ru",
            "password": "Useruser1!"
        }
    )
    assert response.status_code == 200
    assert bool(response.cookies.get("Authorization")) is True


@pytest.mark.asyncio(loop_scope="session")
async def test_login_user_by_phone(unauthorized_client_fixture: AsyncClient):
    response = await unauthorized_client_fixture.post(
        "/users/login/",
        json={
            "phone": "+79999999999",
            "password": "Useruser1!"
        }
    )
    assert response.status_code == 200
    assert bool(response.cookies.get("Authorization")) is True


@pytest.mark.asyncio(loop_scope="session")
async def test_logout_user(unauthorized_client_fixture: AsyncClient):
    response = await unauthorized_client_fixture.post("/users/logout/")
    assert response.status_code == 200
    assert bool(response.cookies.get("Authorization")) is False


@pytest.mark.asyncio(loop_scope="session")
async def test_get_me(authenticated_client_fixture: AsyncClient):
    response = await authenticated_client_fixture.get("/users/me/")
    assert response.status_code == 200
    assert response.json() == {'id': 101,
                               'full_name': 'User Userov',
                               'email': 'user@mail.ru',
                               'phone': '+71111111111',
                               'is_superuser': False}


# Products block
@pytest.mark.asyncio(loop_scope="session")
async def test_post_product(superuser_fixture):
    response = await superuser_fixture.post("/products/",
                                            json={
                                                "name": "string",
                                                "description": "string",
                                                "price": 0
                                            })
    assert response.status_code == 201
    assert response.json() == {'name': 'string',
                               'description': 'string',
                               'price': 0,
                               'is_active': False,
                               'id': 1}


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_product(superuser_fixture):
    response = await superuser_fixture.delete("/products/1")
    assert response.status_code == 204


@pytest.mark.asyncio(loop_scope="session")
async def test_get_product(superuser_fixture):
    response = await superuser_fixture.get("/products/100")
    assert response.status_code == 200
    assert response.json() == {'description': 'Product 1 description',
                               'id': 100,
                               'is_active': True,
                               'name': 'Product 1',
                               'price': 100}


@pytest.mark.asyncio(loop_scope="session")
async def test_get_products(superuser_fixture):
    response = await superuser_fixture.get("/products/")
    assert response.status_code == 200
    assert response.json() == [{'description': 'Product 1 description',
                                'id': 100,
                                'is_active': True,
                                'name': 'Product 1',
                                'price': 100},
                               {'description': 'Product 2 description',
                                'id': 101,
                                'is_active': False,
                                'name': 'Product 2',
                                'price': 200},
                               {'description': 'Product 3 description',
                                'id': 102,
                                'is_active': True,
                                'name': 'Product 3',
                                'price': 300},
                               {'description': 'Product 4 description',
                                'id': 103,
                                'is_active': False,
                                'name': 'Product 4',
                                'price': 400}]


@pytest.mark.asyncio(loop_scope="session")
async def test_patch_product(superuser_fixture):
    response = await superuser_fixture.patch(
        "/products/101",
        json={"is_active": True}
    )
    assert response.status_code == 200
    assert response.json() == {'name': 'Product 2',
                               'description': 'Product 2 description',
                               'price': 200,
                               'is_active': True,
                               'id': 101}


@pytest.mark.asyncio(loop_scope="session")
async def test_get_active_product(authenticated_client_fixture):
    response = await authenticated_client_fixture.get("/products/100")
    assert response.status_code == 200
    assert response.json() == {'name': 'Product 1',
                               'description': 'Product 1 description',
                               'price': 100,
                               'is_active': True,
                               'id': 100}


# Carts block
@pytest.mark.asyncio(loop_scope="session")
async def test_get_cart(authenticated_client_fixture):
    response = await authenticated_client_fixture.get("/cart/")
    assert response.status_code == 200
    assert response.json() == {
        'cart_items':
            [{'product_id': 100,
              'quantity': 10}],
        'total_price': 1000
    }


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_cart(authenticated_client_fixture):
    response = await authenticated_client_fixture.delete("/cart/")
    assert response.status_code == 204


@pytest.mark.asyncio(loop_scope="session")
async def test_get_cart_after_delete_cart(authenticated_client_fixture):
    response = await authenticated_client_fixture.get("/cart/")
    assert response.status_code == 200
    assert response.json() == {
        'cart_items':
            [],
        'total_price': 0
    }


# Cartitems block
@pytest.mark.asyncio(loop_scope="session")
async def test_add_cartitem(authenticated_client_fixture):
    response = await authenticated_client_fixture.post(
        "/cart_item/",
        json={
            "product_id": 102,
            "quantity": 10
        }
    )
    assert response.status_code == 201
    assert response.json() == {'product_id': 102,
                               'quantity': 10}
    response = await authenticated_client_fixture.get("/cart_item/")
    assert response.status_code == 200
    assert response.json() == {
        'cart_items':
            [{'product_id': 102,
              'quantity': 10}],
        'total_price': 3000
    }
    response = await authenticated_client_fixture.post("/cart_item/",
                                                       json={
                                                           "product_id": 102,
                                                           "quantity": 10
                                                       })
    assert response.status_code == 400


@pytest.mark.asyncio(loop_scope="session")
async def test_update_cartitem(authenticated_client_fixture):
    response = await authenticated_client_fixture.patch(
        "/cart_item/102",
        json={
            "quantity": 101
        })
    assert response.status_code == 200
    assert response.json() == {
        'product_id': 102,
        'quantity': 101
    }
    response = await authenticated_client_fixture.get("/cart_item/")
    assert response.status_code == 200
    assert response.json() == {
        'cart_items': [
            {
                'product_id': 102,
                'quantity': 101
            }
        ],
        'total_price': 30300
    }

@pytest.mark.asyncio(loop_scope="session")
async def test_delete_cartitem(authenticated_client_fixture):
    response = await authenticated_client_fixture.delete("/cart_item/102")
    assert response.status_code == 204
    response = await authenticated_client_fixture.get("/cart_item/")
    assert response.status_code == 200
    assert response.json() == {'cart_items': [],
                               'total_price': 0}
