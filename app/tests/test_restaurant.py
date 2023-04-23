from forklyft_app.db import get_db
from sqlalchemy import text
from flask import session

def test_restaurant_home(client,auth):
    auth.login_restaurant()
    response = client.get("/restaurant")
    assert response.status_code == 200
    assert b"tester_login_res" in response.data 
    assert b"Our Menu" in response.data

def test_restaurant_menu(client,auth):
    auth.login_restaurant()
    response = client.get("/restaurant/menu")
    assert response.status_code == 200
    assert b"food1" in response.data

def test_restaurant_order_his(client,auth):
    auth.login_restaurant()
    response = client.get("/restaurant/order_his")
    assert response.status_code == 200
    assert b"No orders yet" in response.data

def test_restaurant_add_item(client, auth, app):
    auth.login_restaurant()
    response = client.get("/restaurant/add_item")
    assert response.status_code == 200
    assert b"Add item" in response.data
    response = client.post("/restaurant/add_item", data={"food_name":"food3","price":"200","type":"starter", "url":"https://images.unsplash.com/photo-1606755456206-b25206cde27e"}, follow_redirects=True)
    with app.app_context():
        db = get_db()
        with db.connect() as conn:
            menu = conn.execute(text('SELECT * FROM menus WHERE restaurant_id = :id ORDER BY menu_id'),{'id':14134141}).all()
            assert len(menu)==3
            assert menu[2][4]=="food3"
    
