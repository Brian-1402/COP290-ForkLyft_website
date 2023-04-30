from forklyft_app import create_app
from forklyft_app.db import init_db, get_db
from seed_db import (
    add_restaurants,
    add_menu_items,
    add_users,
    add_past_orders,
    add_restaurants_imgs,
)
import os


def seeder_app(db_path):
    app = create_app({"DATABASE": db_path})
    with app.app_context():
        # init_db() # executes schema.sql
        db = get_db()
        add_restaurants(db)
        add_menu_items(db)
        # add_users(db)
        add_restaurants_imgs(db)


db_path = os.environ.get("SEED_DB_PATH")
if db_path is None:  # use the baadalvm link by default
    db_path = "mysql://forklyft_project:forklyft@10.17.50.188:3306/forklyft_main"

seeder_app(db_path)
