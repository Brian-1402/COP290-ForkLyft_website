from flask import Flask, render_template, redirect, url_for, flash, request
import sqlite3
from werkzeug.exceptions import abort

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('restaurant.db')
    conn.row_factory = sqlite3.Row
    return conn

def find_restaurant(restaurant_id):
    conn = get_db_connection()
    restaurant = conn.execute('SELECT * FROM restaurants WHERE restaurant_id = ?',(restaurant_id,)).fetchone()
    conn.close()
    if restaurant is None:
        abort(404)
    return restaurant

def find_menu(restaurant_id):
    conn = get_db_connection()
    menu = conn.execute('SELECT * FROM menus WHERE restaurant_id = ?',(restaurant_id,)).fetchall()
    conn.close()
    if menu is None:
        abort(404)
    return menu

def find_starter(menu):
    menu_starter = []
    for item in menu:
        if item['food_type']=='starter':
            menu_starter.append(item)
    return menu_starter

def find_dessert(menu):
    menu_dessert = []
    for item in menu:
        if item['food_type']=='dessert':
            menu_dessert.append(item)
    return menu_dessert

def find_main(menu):
    menu_main = []
    for item in menu:
        if item['food_type']=='main':
            menu_main.append(item)
    return menu_main

def find_drink(menu):
    menu_drink = []
    for item in menu:
        if item['food_type']=='drink':
            menu_drink.append(item)
    return menu_drink

@app.route("/")
def hello():
    conn = get_db_connection()
    menu = conn.execute('SELECT * FROM menus').fetchall()
    return render_template("display.html",menu=menu)

@app.route("/restaurant/<int:restaurant_id>")
def display_restaurant(restaurant_id):
    rest1 = find_restaurant(restaurant_id)
    return render_template("restaurant-home.html",rest=rest1)

@app.route("/restaurant/<int:restaurant_id>/menu")
def display_menu_restaurant(restaurant_id):
    menu = find_menu(restaurant_id)
    # return menu[0]['image_url']
    menu_starter = find_starter(menu)
    menu_dessert = find_dessert(menu)
    menu_main = find_main(menu)
    menu_drink = find_drink(menu)
    return render_template("restaurant-menu.html",menu_s=menu_starter, menu_d = menu_dessert, menu_m = menu_main, menu_dr = menu_drink)

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
            conn= get_db_connection()
            conn.execute('INSERT INTO menus(restaurant_id, image_url, food_name, food_price, food_type) VALUES (?, ?, ?, ?, ?)',
                            (restaurant_id, furl, fname, fprice, ftype))
            conn.commit()
            conn.close()
            return redirect(url_for('display_menu_restaurant',restaurant_id=restaurant_id))
            # return "kya !!"
    return render_template("restaurant-add-item.html",restaurant_id=restaurant_id)

app.run(debug=True)
