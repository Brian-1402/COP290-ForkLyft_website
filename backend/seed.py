# import pandas as pd
# import random
# from database import engine
# from sqlalchemy import text
# resto = pd.read_csv("zomato.csv")
# food = pd.read_csv("food.csv")

# for i in range(50):
#     c = random.randint(1, 20)
#     avg = random.randint(1, 5)
#     s = avg*c
#     with engine.connect() as conn:
#         conn.execute(text("INSERT INTO restaurants (restaurant_name, restaurant_location, restaurant_rating_sum, restaurant_rating_count) VALUES (:name, :location, :sum, :count)"),
#                 {'name':resto['name'][i], 'location':resto['address'][i], 'sum':s, 'count':c})
# # with engine.connect() as conn:
# #         result = conn.execute(text("SELECT * FROM restaurants WHERE restaurant_id = :restaurant_id"),{'restaurant_id':restaurant_id})
# #         return result.all()
# for i in range(1,51):
#     increment = random.randint(0, 100)
#     for j in range(1,6):
#         res_id = i
#         item = random.randint(0,24)
#         price = int(food['Price'][item] + increment)
#         url = food['Url'][item]
#         name = food['Item_name'][item]
#         ftype = food['Category'][item]
#         with engine.connect() as conn:
#             conn.execute(text("INSERT INTO menus (image_url, restaurant_id, food_type, food_name, food_price) VALUES (:image_url, :restaurant_id, :food_type, :food_name, :food_price)"),{'image_url':url, 'restaurant_id':res_id, 'food_type':ftype, 'food_name':name, 'food_price':price})


# from database import engine
# from sqlalchemy import text
# import random
# import pandas as pd

# menu = pd.read_csv("menu.csv")
# # u = "James"
# # address = "221B Baker Street, London - 2010"
# for i in range(20):
#     order_id = i
#     j = random.randint(1,5)
#     res = random.randint(1, 50)
#     start = res*5 - 3
#     end = res*5 + 1
#     user = random.randint(1, 10)
#     for ono in range(j):
#         item = random.randint(start, end)
#         q = random.randint(1,3)
#         with engine.connect() as conn:
#             conn.execute(text("INSERT INTO orders (order_id, restaurant_id, user_id, item_id, quantity) VALUES (:order, :res, :user, :item, :qty)"),
#                     {'order':order_id, 'res':res, 'user':user, 'item':item, 'qty':q})
#     # with engine.connect() as conn:
#     #         result = conn.execute(text("SELECT * FROM restaurants WHERE restaurant_id = :restaurant_id"),{'restaurant_id':restaurant_id})
#     #         return result.all())

from database import engine
from sqlalchemy import text

u = "James"
address = "221B Baker Street, London - 2010"
for i in range(10):
    user = u + str(i)
    passw = user[::-1]
    ad = address + str(i)
    with engine.connect() as conn:
        conn.execute(text("INSERT INTO users (username, home, user_pass, name_user) VALUES (:name, :addr, :pass, :name1)"),
                {'name':user, 'addr':ad, 'pass':passw, 'name1':u})