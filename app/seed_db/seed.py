import pandas as pd
import random
# from forklyft_app.db import get_db
from sqlalchemy import create_engine, text

engine=create_engine("mysql://forklyft_project:forklyft@10.17.50.188:3306/forklyft_main")

def add_restaurant_details():
    resto = pd.read_csv("zomato.csv")
    res = "Res"
    for i in range(50):
        c = random.randint(1, 20)
        avg = random.randint(1, 5)
        s = avg*c
        name = res + str(i+1)
        pas = name[::-1]
        with engine.connect() as conn:
            conn.execute(text("INSERT INTO restaurants (restaurant_name, restaurant_location, restaurant_rating_sum, restaurant_rating_count, restaurant_username, restaurant_password) VALUES (:name, :location, :sum, :count, :username, :password)"),
                    {'name':resto['name'][i], 'location':resto['address'][i], 'sum':s, 'count':c, 'username':name,'password':pas})
            conn.commit()
            
    # # with engine.connect() as conn:
    # #         result = conn.execute(text("SELECT * FROM restaurants WHERE restaurant_id = :restaurant_id"),{'restaurant_id':restaurant_id})
    # #         return result.all()

def add_food_items():
    food = pd.read_csv("food.csv")
    for i in range(1,51):
        increment = random.randint(0, 100)
        for j in range(1,6):
            res_id = i
            item = random.randint(0,24)
            price = int(food['Price'][item] + increment)
            url = food['Url'][item]
            name = food['Item_name'][item]
            ftype = food['Category'][item]
            coun = random.randint(7,15)
            desc = coun*"Very" + "Tasty"
            with engine.connect() as conn:
                conn.execute(text("INSERT INTO menus (image_url, restaurant_id, food_type, food_name, food_price, food_desc) VALUES (:image_url, :restaurant_id, :food_type, :food_name, :food_price, :food_desc)"),{'image_url':url, 'restaurant_id':res_id, 'food_type':ftype, 'food_name':name, 'food_price':price, 'food_desc':desc})
                conn.commit()



def create_restaurant_menus():
        
    menu = pd.read_csv("menu.csv")
    u = "James"
    address = "221B Baker Street, London - 2010"
    for i in range(20):
        order_id = i
        j = random.randint(1,5)
        res = random.randint(1, 50)
        start = res*5 - 3
        end = res*5 + 1
        user = random.randint(1, 10)
        for ono in range(j):
            item = random.randint(start, end)
            q = random.randint(1,3)
            with engine.connect() as conn:
                conn.execute(text("INSERT INTO orders (order_id, restaurant_id, user_id, item_id, quantity) VALUES (:order, :res, :user, :item, :qty)"),
                        {'order':order_id, 'res':res, 'user':user, 'item':item, 'qty':q})
                conn.commit()
                
    #     # with engine.connect() as conn:
    #     #         result = conn.execute(text("SELECT * FROM restaurants WHERE restaurant_id = :restaurant_id"),{'restaurant_id':restaurant_id})
    #     #         return result.all())

def create_restaurant_credentials():
    u = "rest"
    address = "221B Baker Street, London - 2010"
    for i in range(52):
        user = u + str(i)
        passw = user[::-1]
        rid = i+1
        with engine.connect() as conn:
            conn.execute(text("UPDATE restaurants SET restaurant_username =:usr, restaurant_password=:pass WHERE restaurant_id = :id"),
                    {'usr':user, 'pass':passw, 'id':rid})
            conn.commit()
            
            
def print_all():
    with engine.connect() as conn:
        # print(conn.execute(text("select * from restaurants")).all())
        # conn.execute(text('insert into restaurants values (4,"3holistics","aravali", 10, 4, "holistics123", "2holistics")'));
        # input()
        print(conn.execute(text("select * from restaurants")).all())
        # input()
        conn.commit()
        # conn.close()



add_restaurant_details()
add_food_items()
create_restaurant_menus()
create_restaurant_credentials()
# print_all()