import os
import pandas as pd
import random

# food = pd.read_csv(open(os.path.join(os.path.dirname(__file__), "data/food.csv")))
# print(food.T.to_dict())
# # print(random.sample(sorted(food.T.to_dict(),key=lambda x: x[0]),5))
# d=food.T.to_dict()
# arr=[d[i] for i in d.keys()]
# print(random.sample(arr,5))


# makes 5 random items for each 50 restaurants
def add_menu_items():
    food = pd.read_csv(open(os.path.join(os.path.dirname(__file__), "data/food.csv")))
    # for i in range(50):
    increment = random.randint(0, 100)
    random.sample(list(food.T),5)
    j=0
    d=food.T.to_dict()
    arr=[d[i] for i in d.keys()]
    for item in random.sample(arr,5):
        res_id =  1
        item_id = res_id*100 + j + 1
        # item = random.randint(0,24)
        price = int(item['Price'] + increment)
        url = item['Url']
        #! above, modify so that url image returns a lower resolution
        name = item['Item_name']
        ftype = item['Category']
        coun = random.randint(7,15)
        desc = coun*"Very" + "Tasty"
        print(price, name, ftype , item_id)
        j+=1;

add_menu_items()