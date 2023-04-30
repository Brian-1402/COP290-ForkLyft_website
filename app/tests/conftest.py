import pytest
import os
import forklyft_app
from forklyft_app import create_app
from forklyft_app.db import get_db, init_db, execute_db_file
from seed_db import *
from sqlalchemy import text
import tempfile
from flask import g


@pytest.fixture(scope="session")
def app():
    db_path = os.environ.get("TEST_DB_PATH")
    if db_path is None:  # use the baadalvm link by default
        db_path = "mysql://forklyft_project:forklyft@10.17.50.188:3306/forklyft_test"

    # create the app with common test config
    app = create_app({"TESTING": True, "DATABASE": db_path})

    # create the database and load test data
    with app.app_context():
        init_db()  # * Executes schema.sql
        with open(os.path.join(os.path.dirname(__file__), "test_seed.sql"), "rb") as f:
            db = get_db()
            execute_db_file(db, f)  # * executes test_seed.sql
            # add_restaurants(db)
            # add_users(db)
            # add_menu_items(db)
            # add_past_orders(db)

    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()


class AuthActions:
    def __init__(self, client):
        self._client = client

    def login_user(
        self, username="tester_login", password="tester_login", redirect=False
    ):
        return self._client.post(
            "/login",
            data={"username": username, "password": password},
            follow_redirects=redirect,
        )

    def login_restaurant(
        self, username="tester_login_res", password="tester_login_res", redirect=False
    ):
        return self._client.post(
            "/restaurant/login",
            data={"restaurant_username": username, "restaurant_password": password},
            follow_redirects=redirect,
        )

    def logout_user(self, redirect=False):
        return self._client.get("/logout", follow_redirects=redirect)

    def logout_restaurant(self, redirect=False):
        return self._client.get("/restaurant/logout", follow_redirects=redirect)


@pytest.fixture
def auth(client):
    return AuthActions(client)
