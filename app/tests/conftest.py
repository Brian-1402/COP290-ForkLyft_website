import pytest
import os
import forklyft_app
from forklyft_app import create_app
from forklyft_app.db import get_db, init_db, execute_db_file

@pytest.fixture
def app():
    db_path="mysql://forklyft_project:forklyft@10.17.50.188:3306/forklyft_test"
    
    # create the app with common test config
    app = create_app({"TESTING": True, "DATABASE": db_path})

    # create the database and load test data
    with app.app_context():
        init_db() #* Executes schema.sql
        # with open("data.sql", "r") as f:
        with open(os.path.join(os.path.dirname(__file__), "data.sql"), "rb") as f:

            db=get_db()
            execute_db_file(db,f) #* Adds fake data

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

    def login(self, username="tester_login", password="tester_login"):
        return self._client.post(
            "/login", data={"username": username, "password": password}
        )

    def logout(self):
        #! wrong
        #* ^ why is it wrong?
        return self._client.get("/logout")


@pytest.fixture
def auth(client):
    return AuthActions(client)
