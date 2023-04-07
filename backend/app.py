from flask import Flask, render_template, redirect, url_for, flash, request
from database import engine
from sqlalchemy import text
import pymysql
from werkzeug.exceptions import abort

app = Flask(__name__)
# app.config['MYSQL_DATABASE_USER']='root'
# app.config['MYSQL_DATABASE_PASSWORD']='password'
# app.config['MYSQL_DATABASE_DB']='restaurant'
# app.config['MYSQL_DATABASE_HOST']='localhost'
# mysql=MySQL(app)


def find_restaurant(restaurant_id):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM restaurants WHERE restaurant_id = :restaurant_id"),{'restaurant_id':restaurant_id})
        if result is None:
            abort(404)
        return result.all()
    # conn = get_db_connection()
    # restaurant = conn.execute('SELECT * FROM restaurants WHERE restaurant_id = ?',(restaurant_id,)).fetchone()
    # conn.close()
    # if restaurant is None:
    #     abort(404)
    # return restaurant

def find_menu(restaurant_id):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM menus WHERE restaurant_id = :restaurant_id"),{'restaurant_id':restaurant_id})
        if result is None:
            abort(404)
        return result.all()
    
def find_order(restaurant_id):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM orders WHERE restaurant_id = :restaurant_id"),{'restaurant_id':restaurant_id})
        # if result is None:
        #     abort(404)
        return result.all()
    
def find_user(user_id):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM users WHERE user_id = :user_id"),{'user_id':user_id})
        if result is None:
            abort(404)
        return result.all()

def update_user(user_id,home_n,work_n,other_n):
     with engine.connect() as conn:
         conn.execute(text("UPDATE users SET home = :1, work_add = :2, other_add =:3 WHERE user_id = :user_id"),{'1':home_n, '2':work_n, '3':other_n, 'user_id':user_id})
        # if result is None:
        #     abort(404)
        # return result.all()

def find_starter(menu):
    menu_starter = []
    for item in menu:
        if item[3]=='starter':
            menu_starter.append(item)
    return menu_starter

def find_dessert(menu):
    menu_dessert = []
    for item in menu:
        if item[3]=='dessert':
            menu_dessert.append(item)
    return menu_dessert

def find_main(menu):
    menu_main = []
    for item in menu:
        if item[3]=='main':
            menu_main.append(item)
    return menu_main

def find_drink(menu):
    menu_drink = []
    for item in menu:
        if item[3]=='drink':
            menu_drink.append(item)
    return menu_drink

# @app.route("/")
# def hello():
#     conn = get_db_connection()
#     menu = conn.execute('SELECT * FROM menus').fetchall()
#     return render_template("display.html",menu=menu)

@app.route("/restaurant/<int:restaurant_id>")
def display_restaurant(restaurant_id):
    rest1 = find_restaurant(restaurant_id)
    order = find_order(restaurant_id)
    menu = find_menu(restaurant_id)
    return render_template("restaurant-home.html",rest=rest1,order=order,menu=menu)

@app.route("/restaurant/<int:restaurant_id>/menu")
def display_menu_restaurant(restaurant_id):
    rest = find_restaurant(restaurant_id)
    menu = find_menu(restaurant_id)
    # return menu[0]['image_url']
    menu_starter = find_starter(menu)
    menu_dessert = find_dessert(menu)
    menu_main = find_main(menu)
    menu_drink = find_drink(menu)
    return render_template("restaurant-menu.html",rest=rest, menu_s=menu_starter, menu_d = menu_dessert, menu_m = menu_main, menu_dr = menu_drink)

@app.route("/restaurant/<int:restaurant_id>/add_item", methods = ('GET','POST'))
def display_add_form(restaurant_id):
    if(request.method == 'POST'):
        fname=request.form.get('food_name')
        fprice=request.form.get('price')
        ftype=request.form.get('type')
        furl=request.form.get('url')
        # return ("yes")
        if not (fname and fprice and ftype and furl):
            flash('please fill complete information')
        else:
            with engine.connect() as conn:
                conn.execute(text('INSERT INTO menus(restaurant_id, image_url, food_name, food_price, food_type) VALUES (:1, :2, :3, :4, :5)'),
                                {'1':restaurant_id, '2':furl, '3':fname, '4':fprice, '5':ftype})
            return redirect(url_for('display_menu_restaurant',restaurant_id=restaurant_id))
            # return "kya !!"
    return render_template("restaurant-add-item.html",restaurant_id=restaurant_id)

@app.route("/restaurant/<int:restaurant_id>/order_his")
def order_history(restaurant_id):
    rest = find_restaurant(restaurant_id)
    menu = find_order(restaurant_id)
    list=[]
    for row in menu:
        list.append(row[1])
    return render_template("order_history.html",rest=rest,menu=menu,list=list)

@app.route("/user/<int:user_id>/addresses",methods=('GET','POST'))
def address(user_id):
    user = find_user(user_id)
    if(request.method=='POST'):
        fhome = request.form.get('home')
        fwork = request.form.get('work')
        fother = request.form.get('other')
        with engine.connect() as conn:
            conn.execute(text("UPDATE users SET home = :1, work_add = :2, other_add =:3 WHERE user_id = :user_id"),{'1':fhome, '2':fwork, '3':fother, 'user_id':user_id})
        # return "updated!!"
        return redirect(url_for('address',user_id=user_id))
    return render_template("addresses.html",user=user)

app.run(debug=True)
