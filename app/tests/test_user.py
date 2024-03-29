from forklyft_app.db import get_db
from sqlalchemy import text
from flask import session


def test_index(client, auth):
    # test that viewing the page renders without template errors
    assert client.get("/").status_code == 200

    response = client.get("/")
    assert b"About" in response.data
    assert b"Log-In" in response.data
    assert b"Contact" in response.data


def test_user_home(client, auth):
    # test redirect to login page if not signed in
    assert client.get("/user").headers["Location"] == "/login"

    auth.login_user()
    response = client.get("/user")
    assert response.status_code == 200
    assert b"Contact Us" in response.data  # testing navbar
    assert b"Hot new picks" in response.data


def test_search(client, auth):
    # test redirect to login page if not signed in
    assert client.get("/user/food1").headers["Location"] == "/login"

    auth.login_user()
    response = client.post("/user", data={"search": "food1"}, follow_redirects=True)
    assert b"tester_login_res" in response.data
    response = client.post(
        "/user", data={"search": "tester_login_res"}, follow_redirects=True
    )
    assert b"tester_login_res" in response.data
    response = client.post("/user", data={"search": "fffffff"}, follow_redirects=True)
    # print(response.data)
    assert b"no such item" in response.data or b"not available" in response.data


def test_contact_us(client, auth, app):
    # test redirect to login page if not signed in
    assert client.get("/user/contact_us").headers["Location"] == "/login"

    auth.login_user()
    assert client.get("/user/contact_us").status_code == 200
    response = client.get("/user/contact_us")
    assert b"CALL US" in response.data
    response1 = client.post(
        "/user/contact_us",
        data={
            "name": "tester_login",
            "mail": "tester_login@tests.com",
            "message": "test_message1",
        },
        follow_redirects=True,
    )
    assert b"successfully submitted" in response1.data
    # assert len(client.get_flashed_messages()) == 1
    # assert b"successfully submitted" in client.get_flashed_messages()[0]
    response2 = client.post(
        "/user/contact_us",
        data={
            "name": "tester_login",
            "mail": "tester_login@tests.com",
            "message": "test_message2",
        },
        follow_redirects=True,
    )
    assert b"successfully submitted" in response2.data
    # assert len(client.get_flashed_messages()) == 1
    # assert b"successfully submitted" in client.get_flashed_messages()[0]

    with app.app_context():
        db = get_db()
        with db.connect() as conn:
            result1 = conn.execute(
                text(
                    "SELECT user_id, name_user, mail, message FROM contact_us WHERE message = :message1"
                ),
                {"message1": "test_message1"},
            ).all()
            result_all = conn.execute(
                text(
                    "SELECT user_id, name_user, mail, message FROM contact_us WHERE name_user = :name"
                ),
                {"name": "tester_login"},
            ).all()

            assert len(result1) == 1
            assert len(result_all) == 2


def test_profile_page(client, auth, app):
    # test redirect to login page if not signed in
    assert client.get("/user/profile").headers["Location"] == "/login"

    auth.login_user()
    assert client.get("/user/profile").status_code == 200
    # test updating profile details
    response = client.post(
        "/user/profile",
        data={
            "username": "tester_login2",
            "email_id": "tester_login2@tests.com",
            "contact": "9234567890",
            "password": "tester_login",
        },
        follow_redirects=True,
    )
    assert b"profile updated" in response.data
    with app.app_context():
        with get_db().connect() as conn:
            result = conn.execute(
                text("SELECT * FROM users WHERE username = 'tester_login2'")
            ).fetchone()
            # result = (121098561, 'test_home_address', 'test_work_address', 'test_other_address', 'tester_login2', 'tester_login', 'tester_login', 'tester_login2@tests.com', '9234567890')
            assert result[4] == "tester_login2"
            assert result[-1] == "9234567890"
            assert result[-2] == "tester_login2@tests.com"

    # reverting back the account details
    response = client.post(
        "/user/profile",
        data={
            "username": "tester_login",
            "email_id": "tester_login@tests.com",
            "contact": "1234567890",
            "password": "tester_login",
        },
        follow_redirects=True,
    )
    assert b"profile updated" in response.data


def test_user_my_orders(client, auth, app):
    # test redirect to login page if not signed in
    assert client.get("/user/orders").headers["Location"] == "/login"

    auth.login_user()
    response = client.get("/user/orders")
    assert response.status_code == 200
    assert b"Order History" in response.data
    assert b"No orders yet" in response.data


def test_user_my_addresses(client, auth, app):
    # test redirect to login page if not signed in
    assert client.get("/user/addresses").headers["Location"] == "/login"

    auth.login_user()
    response = client.get("/user/addresses")
    assert response.status_code == 200
    assert b"My Addresses" in response.data
    response = client.post(
        "/user/addresses",
        data={
            "home": "test_home_address2",
            "work": "test_work_address2",
            "other": "test_other_address2",
        },
        follow_redirects=True,
    )
    assert b"addresses updated" in response.data
    with app.app_context():
        with get_db().connect() as conn:
            result = conn.execute(
                text("SELECT * FROM users WHERE username = 'tester_login'")
            ).fetchone()
            assert result[1:4] == (
                "test_home_address2",
                "test_work_address2",
                "test_other_address2",
            )

    # reverting back original details
    response = client.post(
        "/user/addresses",
        data={
            "home": "test_home_address",
            "work": "test_work_address",
            "other": "test_other_address",
        },
        follow_redirects=True,
    )
    assert b"addresses updated" in response.data


def test_restaurant_page(client, auth):
    # test redirect to login page if not signed in
    assert client.get("/user/14134141").headers["Location"] == "/login"

    auth.login_user()
    response = client.get("/user/14134141")
    assert response.status_code == 200
    assert b"tester_login_res" in response.data
    assert b"food1" in response.data
    assert client.get("/user/99999999").status_code == 404


def test_user_reviews(client, auth, app):
    auth.login_user()
    response = client.get("/user/14134141")
    assert response.status_code == 200
    assert b"good restaurant" in response.data
    assert b"poor service and terrible food" in response.data
    response = client.post(
        "/user/14134141",
        data={
            "rating": "1",
            "review": "very unpleasant experience",
        },
        follow_redirects=True,
    )
    assert b"We shall try to improve" in response.data
    assert b"2.3" in response.data

    with app.app_context():
        with get_db().connect() as conn:
            result = conn.execute(
                text("SELECT * FROM restaurant_reviews WHERE user_id = 121098561")
            ).all()
            assert len(result) == 3
            assert result[2][4] == "negative"

    response = client.post(
        "/user/14134141",
        data={
            "rating": "5",
            "review": "great service",
        },
        follow_redirects=True,
    )
    assert b"kind feedback" in response.data
    assert b"3" in response.data

    with app.app_context():
        with get_db().connect() as conn:
            result = conn.execute(
                text("SELECT * FROM restaurant_reviews WHERE user_id = 121098561")
            ).all()
            assert len(result) == 4
            assert result[3][4] == "positive"
