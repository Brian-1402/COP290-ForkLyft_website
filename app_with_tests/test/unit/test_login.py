import pytest
from flask import g
from flask import session
from sqlalchemy import text
from forklyft_app.db import get_db


def test_register(client, app):
    # test that viewing the page renders without template errors
    assert client.get("/signup").status_code == 200

    # test that successful registration redirects to the login page
    response = client.post("/signup", data={"username": "tester", "password": "tester_pass", "mail":"test@email.com","contact":"1234567890","name":"tester"})
    # assert 'Invalid email address !' in response.data
    assert response.headers["Location"] == "/login"

    # test that the user was inserted into the database
    with app.app_context():
        with get_db().connect() as conn:
            assert (
                conn.execute(text("SELECT * FROM users WHERE username = 'tester'")).fetchone() is not None
            )


# @pytest.mark.parametrize(
#     ("username", "password", "message"),
#     (
#         ("", "", b"Username is required."),
#         ("a", "", b"Password is required."),
#         ("test", "test", b"already registered"),
#     ),
# )
# def test_register_validate_input(client, username, password, message):
#     response = client.post(
#         "/auth/register", data={"username": username, "password": password}
#     )
#     assert message in response.data


def test_login(client, auth):
    # test that viewing the page renders without template errors
    assert client.get("/login").status_code == 200

    # test that successful login redirects to the index page
    # response = auth.login()
    # assert response.headers["Location"] == "/user"

    # login request set the user_id in the session
    # check that the user is loaded from the session
    # with client:
    #     client.get("/")
    #     # assert session["user_id"] == 1
    #     assert g.user["username"] == "tester"


# @pytest.mark.parametrize(
#     ("username", "password", "message"),
#     (("a", "test", b"Incorrect username."), ("test", "a", b"Incorrect password.")),
# )
# def test_login_validate_input(auth, username, password, message):
#     response = auth.login(username, password)
#     assert message in response.data


# def test_logout(client, auth):
#     auth.login()

#     with client:
#         auth.logout()
#         assert "user_id" not in session
