import pytest

from forklyft_app import create_app
from forklyft_app.db import get_db
from forklyft_app.db import init_db

@pytest.fixture
def app():
    db_path="mysql+pymysql://z16v371xaw89sglx9gvn:pscale_pw_ZfNGzpN8w111NiMpenlF5p2f8yq9gDUNsG99dvUxET@aws.connect.psdb.cloud/forklyft_test?charset=utf8mb4"
    # create the app with common test config
    app = create_app({"TESTING": True, "DATABASE": db_path})

    # create the database and load test data
    with app.app_context():
        init_db() #! Execute schema.sql
        # get_db().executescript(_data_sql)
        #! Add fake data

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

    def login(self, username="tester", password="tester_pass"):
        return self._client.post(
            "/login", data={"username": username, "password": password}
        )

    def logout(self):
        #! wrong
        return self._client.get("/logout")


@pytest.fixture
def auth(client):
    return AuthActions(client)
