from forklyft_app.db import get_db
from sqlalchemy import text
from flask import session

def test_add_to_cart1(client, auth, app):
    auth.login_user()
    response = client.get("/user/cart")
    assert b"you have not added any item to the cart" in response.data
    response = client.get("/add_to_cart?item_id=1413414101&restaurant_id=14134141", follow_redirects=True)
    response = client.get("/add_to_cart?item_id=1413414101&restaurant_id=14134141", follow_redirects=True)
    response = client.get("/add_to_cart?item_id=1413414102&restaurant_id=14134141", follow_redirects=True)
    response = client.get("/add_to_cart?item_id=1413414102&restaurant_id=14134141", follow_redirects=True)
    response = client.get("/add_to_cart?item_id=1413414102&restaurant_id=14134141", follow_redirects=True)
    assert b"added to cart" in response.data
    
    with app.app_context():
        db = get_db()
        with db.connect() as conn:
            cart = conn.execute(text('SELECT * FROM orders WHERE user_id = :id AND order_status = "cart" ORDER BY order_item_id'),{'id':121098561}).all()
            assert len(cart)==2
            assert cart[0][1]==1 # assert cart_id
            assert cart[0][5]==2 # assert quantities
            assert cart[1][5]==3
    
    response = client.get("/user/cart")
    assert b"quantity: 2" in response.data
    assert b"quantity: 3" in response.data


def test_pay(client, auth, app):
    auth.login_user()
    response = client.get("/user/pay")
    assert b"Select an address" in response.data
    assert b"test_other_address" in response.data
    response = client.post("/user/pay", data={'flexRadioDefault':'test_other_address'}, follow_redirects=True)
    assert b"payment successful" in response.data
    with app.app_context():
        db = get_db()
        with db.connect() as conn: # testing if the order_status field is updated to "pending"
            cart = conn.execute(text('SELECT * FROM orders WHERE user_id = :id AND order_id = :order_id AND order_status = "pending" ORDER BY order_item_id'),{'id':121098561, 'order_id':1}).all()
            assert len(cart)==2
            assert cart[0][1]==1 # assert order_id

def test_add_to_cart2(client, auth, app):
    auth.login_user()
    # adding to cart again to check if cart_id is getting a new value
    response = client.get("/add_to_cart?item_id=1413414102&restaurant_id=14134141", follow_redirects=True)
    response = client.get("/add_to_cart?item_id=1413414101&restaurant_id=14134141", follow_redirects=True)
    response = client.get("/add_to_cart?item_id=1413414101&restaurant_id=14134141", follow_redirects=True)
    response = client.get("/add_to_cart?item_id=1413414101&restaurant_id=14134141", follow_redirects=True)
    with app.app_context():
        db = get_db()
        with db.connect() as conn:
            cart = conn.execute(text('SELECT * FROM orders WHERE user_id = :id AND order_status = "cart" ORDER BY order_item_id'),{'id':121098561}).all()
            assert len(cart)==2
            assert cart[0][1]==2 # assert order_id again
            assert cart[0][5]==1 # assert quantities
    # client.post("/user/pay", data={'flexRadioDefault':'test_other_address'})

def test_cart_buttons(client, auth, app):
    auth.login_user()
    response = client.get("/increase?item_id=1413414102&quantity=1", follow_redirects=True)
    assert b"quantity: 2" in response.data
    response = client.get("/decrease?item_id=1413414101&quantity=3", follow_redirects=True)
    assert b"quantity: 2" in response.data
    response = client.get("/decrease?item_id=1413414101&quantity=2", follow_redirects=True)
    assert b"quantity: 1" in response.data
    response = client.get("/decrease?item_id=1413414101&quantity=1", follow_redirects=True)
    assert b"quantity: 1" not in response.data
    with app.app_context():
        db = get_db()
        with db.connect() as conn:
            cart = conn.execute(text('SELECT * FROM orders WHERE user_id = :id AND order_status = "cart" ORDER BY order_item_id'),{'id':121098561}).all()
            assert len(cart)==1
            assert cart[0][1]==2 # assert cart_id
            assert cart[0][5]==2 # assert quantities
    response = client.get("/remove?item_id=1413414102", follow_redirects=True)
    assert b"you have not added any item to the cart" in response.data



def test_pending_orders(client, auth, app):
    auth.login_restaurant()
    response = client.get("/restaurant/pending")
    assert response.status_code == 200
    assert b"Order ID #1" in response.data
    assert b"1413414101" in response.data

def test_delete_order_pending(client, auth, app):
    auth.login_restaurant()
    response = client.get("/delete_order?order_id=1", follow_redirects=True)

    with app.app_context():
        db = get_db()
        with db.connect() as conn:
            cart = conn.execute(text('SELECT * FROM orders WHERE order_id = :id AND order_status = "done" ORDER BY order_item_id'),{'id':1}).all()
            assert len(cart)==2
            assert cart[0][3]==121098561 # assert user_id

def test_restaurant_order_history(client, auth):
    auth.login_restaurant()
    response = client.get("/restaurant/order_his")
    assert response.status_code == 200
    assert b"Order ID #1" in response.data
    assert b"1413414101" in response.data

def test_user_order_history(client,auth,app):
    auth.login_user()
    response = client.get("/user/orders")
    assert response.status_code == 200
    assert b"Order ID #1" in response.data
    assert b"1413414101" in response.data
    
    with app.app_context():
        db = get_db()
        with db.connect() as conn:
            conn.execute(text('DELETE FROM orders'))
            conn.commit()
    response = client.get("/user/orders")
    assert b"No orders yet" in response.data
            
def test_end_fixture(client, app):
    with app.app_context():
        db = get_db()
        with db.connect() as conn:
            conn.execute(text('DELETE FROM orders'))
            conn.commit()