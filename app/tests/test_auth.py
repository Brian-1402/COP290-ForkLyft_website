import pytest
from flask import g
from flask import session
from sqlalchemy import text
from forklyft_app.db import get_db


def test_register_user(client, app):
    # test that viewing the page renders without template errors
    assert client.get("/signup").status_code == 200

    # test that successful registration redirects to the login page
    response = client.post(
        "/signup",
        data={
            "username": "tester_signup",
            "password": "tester_signup",
            "mail": "tester_signup@tests.com",
            "contact": "1234567890",
            "name": "tester_signup",
        },
    )
    assert response.headers["Location"] == "/login"

    # test for invalid user details
    wrong_response1 = client.post(
        "/signup",
        data={
            "username": "tester_login",
            "password": "tester_signup",
            "mail": "tester_signup@tests.com",
            "contact": "1234567890",
            "name": "tester_signup",
        },
        follow_redirects=True,
    )
    assert b"Account already exists" in wrong_response1.data

    # wrong_response2 = client.post("/signup", data={"username": "tester_signup", "password": "tester_signup", "mail":"testscom","contact":"1234567890","name":"tester_signup"}, follow_redirects=True)
    # assert b"Invalid email address" in wrong_response2.data
    # wrong_response3 = client.post("/signup", data={"username": "tester_signup&*&%#", "password": "tester_signup", "mail":"tester_signup@tests.com","contact":"1234567890","name":"tester_signup"}, follow_redirects=True)
    # assert b"name must contain only characters and numbers" in wrong_response3.data
    # * may not even have to test the above commented lines because checking is done in browser js

    # test that the user was inserted into the database
    with app.app_context():
        with get_db().connect() as conn:
            assert (
                conn.execute(
                    text("SELECT * FROM users WHERE username = 'tester_signup'")
                ).fetchone()
                is not None
            )


def test_login_user(client, auth):
    # test that viewing the page renders without template errors
    assert client.get("/login").status_code == 200

    # test that successful login redirects to the index page
    response = auth.login_user()
    assert response.headers["Location"] == "/user"

    # already logged in account should not be able to access login page and login again
    assert auth.login_user().headers["location"] == "/user"

    # test flash message in redirected page
    auth.logout_user()
    response = auth.login_user(redirect=True)
    assert b"successfully logged in" in response.data

    # login request set the user_id in the session
    # check that the user is loaded from the session
    with client:
        client.get("/")
        assert session["id"] == 121098561
        assert session["username"] == "tester_login"


@pytest.mark.parametrize(
    ("username", "password", "message"),
    (
        ("incorrect_username1", "incorrect_password1", b"incorrect"),
        ("incorrect_username2", "incorrect_password2", b"incorrect"),
    ),
)
def test_login_user_validate_input(auth, username, password, message):
    response = auth.login_user(username, password)
    assert message in response.data


def test_logout_user(client, auth):
    auth.login_user()

    with client:
        response = auth.logout_user()
        assert "id" not in session
        assert response.headers["Location"] == "/"


def test_register_restaurant(client, auth, app):
    # test that viewing the page renders without template errors
    assert client.get("/restaurant/signup").status_code == 200

    # test that successful registration redirects to the login page
    response = client.post(
        "/restaurant/signup",
        data={
            "username": "tester_signup_res1",
            "password": "tester_signup_res",
            "location": "test_res_address",
            "restaurant_name": "tester_signup_res",
        },
    )
    assert response.headers["Location"] == "/restaurant/login"

    # test that after logged in, opening signup redirects to home page
    assert (
        auth.login_restaurant(
            username="tester_signup_res1", password="tester_signup_res"
        ).headers["Location"]
        == "/restaurant"
    )
    assert client.get("/restaurant/signup").headers["location"] == "/restaurant"
    auth.logout_restaurant()

    # test for invalid user details
    wrong_response1 = client.post(
        "/restaurant/signup",
        data={
            "username": "tester_login_res",
            "password": "tester_login_res",
            "location": "test_res_address",
            "restaurant_name": "tester_login_res",
        },
        follow_redirects=True,
    )
    assert b"already exists" in wrong_response1.data

    # wrong_response2 = client.post("/restaurant/signup", data={"password": "tester_login_res", "location":"test_res_address","restaurant_name":"tester_login_res"}, follow_redirects=True)
    # assert b"Please fill out the form"  in wrong_response2.data

    # test that the user was inserted into the database
    with app.app_context():
        with get_db().connect() as conn:
            assert (
                conn.execute(
                    text(
                        "SELECT * FROM restaurants WHERE restaurant_username = 'tester_signup_res1'"
                    )
                ).fetchone()
                is not None
            )


def test_login_restaurant(client, auth):
    # test that viewing the page renders without template errors
    assert client.get("/restaurant/login").status_code == 200

    # test that successful login redirects to the index page
    response = auth.login_restaurant()
    assert response.headers["Location"] == "/restaurant"

    # already logged in account should not be able to access login page and login again
    assert auth.login_restaurant().headers["Location"] == "/restaurant"

    # test flash message in redirected page
    auth.logout_restaurant()
    response = auth.login_restaurant(redirect=True)
    assert b"successfully logged in" in response.data

    # login request set the user_id in the session
    # check that the user is loaded from the session
    with client:
        client.get("/")
        assert session["id1"] == 14134141
        assert session["username"] == "tester_login_res"


@pytest.mark.parametrize(
    ("username", "password", "message"),
    (
        ("incorrect_username1", "incorrect_password1", b"incorrect"),
        ("incorrect_username2", "incorrect_password2", b"incorrect"),
    ),
)
def test_login_restaurant_validate_input(auth, username, password, message):
    response = auth.login_restaurant(username, password)
    assert message in response.data


def test_logout_restaurant(client, auth):
    auth.login_restaurant()

    with client:
        auth.logout_restaurant()
        assert "id" not in session
        # ! test that redirected to index page, also test logout flash message
