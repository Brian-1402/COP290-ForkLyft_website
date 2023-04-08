from flask import Flask, render_template, redirect, url_for, flash, request, session, Blueprint
from forklyft_app.db import get_db
from sqlalchemy import text
import re
from werkzeug.exceptions import abort
from forklyft_app import create_app # potential rename
# app=create_app()
bp=Blueprint("app",__name__)
# app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# app.config['MYSQL_DATABASE_USER']='root'
# app.config['MYSQL_DATABASE_PASSWORD']='password'
# app.config['MYSQL_DATABASE_DB']='restaurant'
# app.config['MYSQL_DATABASE_HOST']='localhost'
# mysql=MySQL(app)

def find_restaurant(restaurant_id):
	with get_db().connect() as conn:
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

def get_menu():
	with get_db().connect() as conn:
		result = conn.execute(text('SELECT * FROM menus'))
		return result.all()
	
def get_restaurant():
	with get_db().connect() as conn:
		result = conn.execute(text('SELECT * FROM restaurants'))
		return result.all()

def find_menu(restaurant_id):
	with get_db().connect() as conn:
		result = conn.execute(text("SELECT * FROM menus WHERE restaurant_id = :restaurant_id"),{'restaurant_id':restaurant_id})
		if result is None:
			abort(404)
		return result.all()
	
def find_order(restaurant_id):
	with get_db().connect() as conn:
		result = conn.execute(text("SELECT * FROM orders WHERE restaurant_id = :restaurant_id"),{'restaurant_id':restaurant_id})
		# if result is None:
		#     abort(404)
		return result.all()
	
def find_user_order(user_id):
	with get_db().connect() as conn:
		result = conn.execute(text("SELECT * FROM orders WHERE user_id = :user_id"),{'user_id':user_id})
		# if result is None:
		#     abort(404)
		return result.all()
	
def find_user(user_id):
	with get_db().connect() as conn:
		result = conn.execute(text("SELECT * FROM users WHERE user_id = :user_id"),{'user_id':user_id})
		if result is None:
			abort(404)
		return result.all()

def update_user(user_id,home_n,work_n,other_n):
	 with get_db().connect() as conn:
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


@bp.route('/restaurant/login', methods = ['GET', 'POST'])
def res_login():
	if request.method == 'POST' and 'restaurant_username' in request.form and 'restaurant_password' in request.form:
		username = request.form['restaurant_username']
		password = request.form['restaurant_password']
		with get_db().connect() as conn:
			restaurant=conn.execute(text('SELECT * FROM restaurants WHERE restaurant_username = :username AND BINARY restaurant_password = :password'), {'username':username, 'password':password })
		restaurant=restaurant.all()
		if len(restaurant):
			restaurant=restaurant[0]
			session['loggedin'] = True
			session['id1'] = restaurant[0]
			session['username'] = restaurant[5]
			flash("successfully logged in!!",'success')
			return redirect(url_for('display_restaurant'))
		else:
			flash("try again!! incorrect username or password!! sign up if new restaurant",'error')
	return render_template('restaurant-login.html')

@bp.route('/restaurant/signup', methods = ('GET', 'POST'))
def restaurant_register():
	if request.method == 'POST' and 'restaurant_name' in request.form and 'username' in request.form and 'password' in request.form and 'location' in request.form:
		username = request.form['username']
		password = request.form['password']
		location = request.form['location']
		name = request.form['restaurant_name']
		a=False
		with get_db().connect() as conn:
			restaurant=conn.execute(text('SELECT * FROM restaurants WHERE restaurant_username = :username'), {'username':username})
		restaurant=restaurant.all()
		if len(restaurant):
			msg1 = 'restaurant already exists !'
			e1='error'
		elif not re.match(r'[A-Za-z0-9]+', username):
			msg1 = 'username must contain only characters and numbers !'
			e1='error'
		else:
			with get_db().connect() as conn:
				conn.execute(text("INSERT INTO restaurants (restaurant_username, restaurant_password, restaurant_name, restaurant_location) VALUES (:uname, :pass, :name, :loc)"),
						{'uname':username, 'pass':password, 'name':name, 'loc':location})
			msg1='You have successfully registered !'
			e1='success'
			a=True
		flash(msg1,e1)
		if(a):return redirect(url_for('res_login'))
		else: return redirect(url_for('restaurant_register'))
	elif request.method == 'POST':
		flash('Please fill out the form !','error')
		return redirect(url_for('restaurant_register'))
	return render_template('index.html')

@bp.route("/restaurant")
def display_restaurant():
	restaurant_id=session['id1']
	rest1 = find_restaurant(restaurant_id)
	order = find_order(restaurant_id)
	menu = find_menu(restaurant_id)
	return render_template("restaurant-home.html",rest=rest1,order=order,menu=menu)

@bp.route("/restaurant/menu")
def display_menu_restaurant():
	restaurant_id = session['id1']
	rest = find_restaurant(restaurant_id)
	menu = find_menu(restaurant_id)
	# return menu[0]['image_url']
	menu_starter = find_starter(menu)
	menu_dessert = find_dessert(menu)
	menu_main = find_main(menu)
	menu_drink = find_drink(menu)
	return render_template("restaurant-menu.html",rest=rest, menu_s=menu_starter, menu_d = menu_dessert, menu_m = menu_main, menu_dr = menu_drink)

@bp.route("/restaurant/add_item", methods = ('GET','POST'))
def display_add_form():
	restaurant_id=session['id1']
	if(request.method == 'POST'):
		fname=request.form.get('food_name')
		fprice=request.form.get('price')
		ftype=request.form.get('type')
		furl=request.form.get('url')
		# return ("yes")
		if not (fname and fprice and ftype and furl):
			flash('please fill complete information')
		else:
			with get_db().connect() as conn:
				conn.execute(text('INSERT INTO menus(restaurant_id, image_url, food_name, food_price, food_type) VALUES (:1, :2, :3, :4, :5)'),
								{'1':restaurant_id, '2':furl, '3':fname, '4':fprice, '5':ftype})
			return redirect(url_for('display_menu_restaurant'))
	return render_template("restaurant-add-item.html",restaurant_id=restaurant_id)

@bp.route("/restaurant/order_his")
def order_history():
	restaurant_id = session['id1']
	rest = find_restaurant(restaurant_id)
	menu = find_order(restaurant_id)
	list=[]
	for row in menu:
		list.append(row[1])
	return render_template("order_history.html",rest=rest,menu=menu,list=list)


@bp.route("/user")
def user_home():
	result = get_menu()[-8:]
	dict={}
	for row in result:
		with get_db().connect() as conn:
			name = conn.execute(text('SELECT restaurant_name FROM restaurants WHERE restaurant_id = :id'),{'id':row[2]}).all()[0]
		dict[row[0]]=name

	restaurant=get_restaurant()
	Li=[]
	for row in restaurant:
		row=list(row)
		rating_sum = row[3]
		rating_count = row[4]
		row.insert(0,rating_sum/rating_count)
		row=tuple(row)
		Li.append(row)

	restaurant=sorted(Li,key=lambda x: x[0])
	restaurant=restaurant[-8:]
	image=[]
	for row in restaurant:
		with get_db().connect() as conn:
			link = conn.execute(text('SELECT image_url FROM menus WHERE restaurant_id = :id'),{'id':row[1]}).all()[0]
		image.append(link)
	user_id = session['id']
	return render_template("user-home.html",user_id=user_id,menu=result, dict=dict, restaurant=restaurant,image=image)

@bp.route("/user/addresses",methods=('GET','POST'))
def address():
	user_id=session['id']
	user = find_user(user_id)
	if(request.method=='POST'):
		fhome = request.form.get('home')
		fwork = request.form.get('work')
		fother = request.form.get('other')
		with get_db().connect() as conn:
			conn.execute(text("UPDATE users SET home = :1, work_add = :2, other_add =:3 WHERE user_id = :user_id"),{'1':fhome, '2':fwork, '3':fother, 'user_id':user_id})
		# return "updated!!"
		return redirect(url_for('view_profile'))
	return render_template("addresses.html",user=user,id=user_id)

@bp.route("/user/profile",methods=('GET','POST'))
def view_profile():
	user_id=session['id']
	user= find_user(user_id)
	if(request.method=='POST'):
		username=request.form.get('username')
		mail=request.form.get('email_id')
		contact=request.form.get('contact')
		with get_db().connect() as conn:
			conn.execute(text("UPDATE users SET username = :1, mail = :2, phone_number =:3 WHERE user_id = :user_id"),{'1':username, '2':mail, '3':contact, 'user_id':user_id})
		return redirect(url_for('view_profile'))
	return render_template("my-profile.html",user=user,id=user_id)

@bp.route("/user/orders")
def view_orders():
	user_id=session['id']
	menu = find_user_order(user_id)
	list=[]
	item={}
	for row in menu:
		with get_db().connect() as conn:
			result = conn.execute(text("SELECT food_name, food_price, image_url FROM menus WHERE menu_id = :item_id"),{'item_id':row[4]})
			item[row[4]]=result.all()
		list.append(row[1])
	return render_template("my-orders.html",menu=menu,list=list,user_id=user_id, item=item)


@bp.route("/user/contact_us",methods=('GET','POST'))
def contact():
	user_id=session['id']
	if(request.method=='POST'):
		name=request.form.get('name')
		mail=request.form.get('mail')
		message=request.form.get('message')
		with get_db().connect() as conn:
			conn.execute(text("INSERT INTO contact_us (user_id, name_user, mail, message) VALUES (:1, :2, :3, :4)"),{'1':user_id, '2':name, '3':mail, '4':message})
		flash("succesfully submitted!!","success")
		return redirect(url_for('contact'))
	return render_template("contact-us.html",id=user_id)


# @bp.route("/user/<int:user_id>/")

@bp.route('/login', methods = ['GET', 'POST'])
def login():
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		password = request.form['password']
		with get_db().connect() as conn:
			user=conn.execute(text('SELECT * FROM users WHERE username = :username AND BINARY user_pass = :password'), {'username':username, 'password':password })
		user=user.all()
		if len(user):
			user=user[0]
			session['loggedin'] = True
			session['id'] = user[0]
			session['username'] = user[4]
			flash("successfully logged in!!",'success')
			return redirect(url_for('user_home'))
		else:
			flash("try again!! incorrect username or password!! sign up if new user",'error')
	return render_template('user-login.html')

@bp.route('/signup', methods = ('GET', 'POST'))
def register():
	if request.method == 'POST' and 'name' in request.form and 'username' in request.form and 'password' in request.form and 'mail' in request.form and 'contact' in request.form:
		username = request.form['username']
		password = request.form['password']
		email = request.form['mail']
		contact = request.form['contact']
		name = request.form['name']
		a=False
		with get_db().connect() as conn:
			user=conn.execute(text('SELECT * FROM users WHERE username = :username'), {'username':username})
		user=user.all()
		if len(user):
			msg1 = 'Account already exists !'
			e1='error'
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
			msg1 = 'Invalid email address !'
			e1='error'
		elif not re.match(r'[A-Za-z0-9]+', username):
			msg1 = 'name must contain only characters and numbers !'
			e1='error'
		else:
			with get_db().connect() as conn:
				conn.execute(text("INSERT INTO users (username, user_pass, name_user, phone_number, mail) VALUES (:uname, :pass, :name, :contact, :email)"),
						{'uname':username, 'pass':password, 'name':name, 'contact':contact, 'email':email})
			msg1='You have successfully registered !'
			e1='success'
			a=True
		flash(msg1,e1)
		if(a):return redirect(url_for('login'))
		else: return redirect(url_for('register'))
	elif request.method == 'POST':
		flash('Please fill out the form !','error')
		return redirect(url_for('register'))
	return render_template('user-signup.html')

@bp.route('/logout')
def logout():
	session.pop('loggedin', None)
	session.pop('id', None)
	session.pop('username', None)   
	return redirect(url_for('login'))

@bp.route('/restaurant/logout')
def restaurant_logout():
	session.pop('loggedin', None)
	session.pop('id1', None)
	session.pop('username', None)   
	return redirect(url_for('res_login'))


# bp.run(debug=True)
