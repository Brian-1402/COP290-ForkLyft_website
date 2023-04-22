import pandas as pd
import random
import os
from forklyft_app.db import get_db
from sqlalchemy import create_engine, text

# engine=create_engine("mysql://forklyft_project:forklyft@10.17.50.188:3306/forklyft_main")

# makes 50 random restaurants
def add_restaurants(db_instance):
    resto = pd.read_csv(open(os.path.join(os.path.dirname(__file__), "data/zomato.csv")))
    res = "Res"
    for i in range(50):
        c = random.randint(1, 20)
        s = int(random.random()*5*c)
        res_id = i + 1
        name = res + str(i+1)
        pas = name[::-1]
        with db_instance.connect() as conn:
            conn.execute(text("INSERT INTO restaurants (restaurant_id, restaurant_name, restaurant_location, restaurant_rating_sum, restaurant_rating_count, restaurant_username, restaurant_password) VALUES (:res_id, :name, :location, :sum, :count, :username, :password)"),
                    {'res_id': res_id, 'name':resto['name'][i], 'location':resto['address'][i], 'sum':s, 'count':c, 'username':name,'password':pas})
            conn.commit()
            
    # # with engine.connect() as conn:
    # #         result = conn.execute(text("SELECT * FROM restaurants WHERE restaurant_id = :restaurant_id"),{'restaurant_id':restaurant_id})
    # #         return result.all()

# makes 5 random items for each 50 restaurants
def add_menu_items(db_instance):
    food = pd.read_csv(open(os.path.join(os.path.dirname(__file__), "data/food.csv")))
    for i in range(50):
        increment = random.randint(0, 100)
        for j in range(5):
            res_id = i + 1
            item_id = res_id*100 + j + 1
            item = random.randint(0,24)
            price = int(food['Price'][item] + increment)
            url = food['Url'][item]
            #! above, modify so that url image returns a lower resolution
            name = food['Item_name'][item]
            ftype = food['Category'][item]
            coun = random.randint(7,15)
            desc = coun*"Very" + "Tasty"
            with db_instance.connect() as conn:
                conn.execute(text("INSERT INTO menus (menu_id, image_url, restaurant_id, food_type, food_name, food_price, food_desc) VALUES (:menu_id, :image_url, :restaurant_id, :food_type, :food_name, :food_price, :food_desc)"),
                             {'menu_id':item_id, 'image_url':url, 'restaurant_id':res_id, 'food_type':ftype, 'food_name':name, 'food_price':price, 'food_desc':desc})
                conn.commit()

# add 10 random users
def add_users(db_instance):
    usr = "user"
    for i in range(10):
        user_id = i + 1
        home = f"Room B{10+i}, Aravali Hostel, IIT Delhi"
        name = usr + str(i+1)
        user_pass = name[::-1]
        mail=name+"@email.com"
        phone_number=int(random.random()*(10**11 - 10**10))+10**10
        with db_instance.connect() as conn:
            conn.execute(text("INSERT INTO users (user_id , home, username, name_user, user_pass, mail, phone_number) VALUES (:user_id, :home, :username, :name_user, :user_pass, :mail, :phone_number)"),
                              {'user_id':user_id,'home':home,'username':name,'name_user':name,'user_pass':user_pass,'mail':mail,'phone_number':phone_number})
            conn.commit()


# adds 20 random orders to random users with random items from random restaurants
def add_past_orders(db_instance):
    menu = pd.read_csv(open(os.path.join(os.path.dirname(__file__), "data/menu.csv")))
    for i in range(20): # number of total orders
        order_id = i+1
        j = random.randint(1,5)
        res = random.randint(1, 51)
        user = random.randint(1, 11)
        for ono in range(j): # number of items in an order
            item = random.randint(res*100+1, res*100+5)
            q = random.randint(1,3)
            with db_instance.connect() as conn:
                conn.execute(text("INSERT INTO orders (order_id, restaurant_id, user_id, item_id, quantity) VALUES (:order, :res, :user, :item, :qty)"),
                        {'order':order_id, 'res':res, 'user':user, 'item':item, 'qty':q})
                conn.commit()
                
    #     # with engine.connect() as conn:
    #     #         result = conn.execute(text("SELECT * FROM restaurants WHERE restaurant_id = :restaurant_id"),{'restaurant_id':restaurant_id})
    #     #         return result.all())

# def set_restaurant_credentials(db_instance):
#     u = "rest"
#     address = "221B Baker Street, London - 2010"
#     for i in range(52):
#         user = u + str(i)
#         passw = user[::-1]
#         rid = i+1
#         with db_instance.connect() as conn:
#             conn.execute(text("UPDATE restaurants SET restaurant_username =:usr, restaurant_password=:pass WHERE restaurant_id = :id"),
#                     {'usr':user, 'pass':passw, 'id':rid})
#             conn.commit()
            
            
def print_all(db_instance):
    with db_instance.connect() as conn:
        # print(conn.execute(text("select * from restaurants")).all())
        # conn.execute(text('insert into restaurants values (4,"3holistics","aravali", 10, 4, "holistics123", "2holistics")'));
        # input()
        print("restaurants:\n\n",conn.execute(text("select * from restaurants")).all())
        print("menus:\n\n",conn.execute(text("select * from restaurants")).all())
        print("orders:\n\n",conn.execute(text("select * from restaurants")).all())
        # input()
        conn.commit()
        # conn.close()
