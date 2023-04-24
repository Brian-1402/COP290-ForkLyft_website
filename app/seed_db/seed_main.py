from sqlalchemy import create_engine
from seed_db import add_menu_items

engine=create_engine("mysql://forklyft_project:forklyft@10.17.50.188:3306/forklyft_main")

# add_restaurants(engine)
add_menu_items(engine)
# add_past_orders(engine)