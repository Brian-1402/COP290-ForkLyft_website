from forklyft_app.db import get_db


def test_get_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()

    #! assert that error will happen if you call get_db outside app_context()
