from forklyft_app.db import get_db
from sqlalchemy import text
from flask import session


def test_restaurant_home(client, auth):
    # test redirect to login page if not signed in
    response = client.get("/restaurant")
    assert response.headers["Location"] == "/restaurant/login"

    auth.login_restaurant()
    response = client.get("/restaurant")
    assert response.status_code == 200
    assert b"tester_login_res" in response.data
    assert b"Our Menu" in response.data
    assert b"poor service and terrible food" in response.data


def test_restaurant_menu(client, auth):
    # test redirect to login page if not signed in
    response = client.get("/restaurant/menu")
    assert response.headers["Location"] == "/restaurant/login"

    auth.login_restaurant()
    response = client.get("/restaurant/menu")
    assert response.status_code == 200
    assert b"food1" in response.data


def test_restaurant_order_his(client, auth):
    # test redirect to login page if not signed in
    response = client.get("/restaurant/order_his")
    assert response.headers["Location"] == "/restaurant/login"

    auth.login_restaurant()
    response = client.get("/restaurant/order_his")
    assert response.status_code == 200
    assert b"No orders yet" in response.data


def test_restaurant_add_item(client, auth, app):
    # test redirect to login page if not signed in
    response = client.get("/restaurant/add_item")
    assert response.headers["Location"] == "/restaurant/login"

    auth.login_restaurant()
    response = client.get("/restaurant/add_item")
    assert response.status_code == 200
    assert b"Add item" in response.data
    response = client.post(
        "/restaurant/add_item",
        data={
            "food_name": "food3",
            "price": "200",
            "type": "starter",
            "url": "https://images.unsplash.com/photo-1606755456206-b25206cde27e",
        },
        follow_redirects=True,
    )
    with app.app_context():
        db = get_db()
        with db.connect() as conn:
            menu = conn.execute(
                text("SELECT * FROM menus WHERE restaurant_id = :id ORDER BY menu_id"),
                {"id": 14134141},
            ).all()
            assert len(menu) == 3
            assert menu[2][4] == "food3"


def test_restaurant_remove_item(client, auth, app):
    # test redirect to login page if not signed in
    response = client.get("/restaurant/delete_from_menu?item_id=1413414103")
    assert response.headers["Location"] == "/restaurant/login"

    auth.login_restaurant()
    response = client.get("/restaurant/delete_from_menu?item_id=1413414103")
    with app.app_context():
        db = get_db()
        with db.connect() as conn:
            item = conn.execute(
                text(
                    "SELECT * FROM menus WHERE restaurant_id = :id AND menu_id = :item_id ORDER BY menu_id"
                ),
                {"id": 14134141, "item_id": 1413414103},
            ).all()
            assert len(item) == 0
            full_menu = conn.execute(
                text("SELECT * FROM menus WHERE restaurant_id = :id ORDER BY menu_id"),
                {"id": 14134141},
            ).all()
            assert len(full_menu) == 2
