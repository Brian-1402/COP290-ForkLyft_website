from flask import Flask, render_template, redirect, url_for, flash, request, session
from database import engine
from sqlalchemy import text
import re
from werkzeug.exceptions import abort
def create_app():
	app = Flask(__name__)
	app.config['DEBUG']=True
	return app

app=create_app()
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# app.config['MYSQL_DATABASE_USER']='root'
# app.config['MYSQL_DATABASE_PASSWORD']='password'
# app.config['MYSQL_DATABASE_DB']='restaurant'
# app.config['MYSQL_DATABASE_HOST']='localhost'
# mysql=MySQL(app)

order_id1=19

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

def get_menu():
	with engine.connect() as conn:
		result = conn.execute(text('SELECT * FROM menus'))
		return result.all()
	

def get_menu_user(restaurant_id):
	with engine.connect() as conn:
		result = conn.execute(text('SELECT * FROM menus WHERE restaurant_id = :rest_id'),{'rest_id':restaurant_id})
		return result.all()
	
def get_restaurant():
	with engine.connect() as conn:
		result = conn.execute(text('SELECT * FROM restaurants'))
		return result.all()

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
	
def find_order_pending(restaurant_id):
	with engine.connect() as conn:
		result = conn.execute(text("SELECT * FROM pending_orders WHERE restaurant_id = :restaurant_id"),{'restaurant_id':restaurant_id})
		# if result is None:
		#     abort(404)
		return result.all()
	
def find_user_order(user_id):
	with engine.connect() as conn:
		result = conn.execute(text("SELECT * FROM orders WHERE user_id = :user_id"),{'user_id':user_id})
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


@app.route('/restaurant/login', methods = ['GET', 'POST'])
def res_login():
	if request.method == 'POST' and 'restaurant_username' in request.form and 'restaurant_password' in request.form:
		username = request.form['restaurant_username']
		password = request.form['restaurant_password']
		with engine.connect() as conn:
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

@app.route('/restaurant/signup', methods = ('GET', 'POST'))
def restaurant_register():
	if request.method == 'POST' and 'restaurant_name' in request.form and 'username' in request.form and 'password' in request.form and 'location' in request.form:
		username = request.form['username']
		password = request.form['password']
		location = request.form['location']
		name = request.form['restaurant_name']
		a=False
		with engine.connect() as conn:
			restaurant=conn.execute(text('SELECT * FROM restaurants WHERE restaurant_username = :username'), {'username':username})
		restaurant=restaurant.all()
		if len(restaurant):
			msg1 = 'restaurant already exists !'
			e1='error'
		elif not re.match(r'[A-Za-z0-9]+', username):
			msg1 = 'username must contain only characters and numbers !'
			e1='error'
		else:
			with engine.connect() as conn:
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

@app.route("/restaurant")
def display_restaurant():
	restaurant_id=session['id1']
	rest1 = find_restaurant(restaurant_id)
	order = find_order(restaurant_id)
	menu = find_menu(restaurant_id)
	return render_template("restaurant-home.html",rest=rest1,order=order,menu=menu)

@app.route("/restaurant/menu")
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

@app.route("/restaurant/add_item", methods = ('GET','POST'))
def display_add_form():
	restaurant_id=session['id1']
	if(request.method == 'POST'):
		fname=request.form.get('food_name')
		fprice=request.form.get('price')
		ftype=request.form.get('type')
		fdesc=request.form.get('description')
		furl=request.form.get('url')
		# return ("yes")
		if not (fname and fprice and ftype and furl):
			flash('please fill complete information')
		else:
			with engine.connect() as conn:
				conn.execute(text('INSERT INTO menus(restaurant_id, image_url, food_name, food_price, food_type, food_desc) VALUES (:1, :2, :3, :4, :5, :6)'),
								{'1':restaurant_id, '2':furl, '3':fname, '4':fprice, '5':ftype, '6':fdesc})
			return redirect(url_for('display_menu_restaurant'))
	return render_template("restaurant-add-item.html",restaurant_id=restaurant_id)

@app.route("/restaurant/order_his")
def order_history():
	restaurant_id = session['id1']
	rest = find_restaurant(restaurant_id)
	menu = find_order(restaurant_id)
	list=[]
	for row in menu:
		list.append(row[1])
	return render_template("order_history.html",rest=rest,menu=menu,list=list)


@app.route("/restaurant/pending")
def pending():
	restaurant_id = session['id1']
	# rest = find_restaurant(restaurant_id)
	menu = find_order_pending(restaurant_id)
	list=[]
	for row in menu:
		list.append(row[6])
	return render_template("restaurant_pending.html",menu=menu,list=list)


@app.route("/delete_order")
def delete_order_pending():
	res_id = session['id1']
	order_id = request.args.get('order_id')
	with engine.connect() as conn:
		order = conn.execute(text('SELECT * FROM pending_orders WHERE order_id = :order_id AND restaurant_id =:res_id'),{'order_id':order_id,'res_id':res_id}).all()
	for row in order:
		with engine.connect() as conn:
			conn.execute(text('INSERT INTO orders (order_id,restaurant_id,user_id,item_id,quantity) VALUES (:1,:2,:3,:4,:5)'),{'1':order_id,'2':res_id,'3':row[1],'4':row[3],'5':row[4]})
	with engine.connect() as conn:
		conn.execute(text('DELETE FROM pending_orders WHERE order_id = :order_id AND restaurant_id= :id'),{'order_id':order_id,'id':res_id})
	return redirect(url_for("pending"))

































@app.route("/user")
def user_home():
	result = get_menu()[-8:]
	dict={}
	for row in result:
		with engine.connect() as conn:
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
		with engine.connect() as conn:
			link = conn.execute(text('SELECT image_url FROM menus WHERE restaurant_id = :id'),{'id':row[1]}).all()[0]
		image.append(link)
	user_id = session['id']
	return render_template("user-home.html",user_id=user_id,menu=result, dict=dict, restaurant=restaurant,image=image)

@app.route("/user/addresses",methods=('GET','POST'))
def address():
	user_id=session['id']
	user = find_user(user_id)
	if(request.method=='POST'):
		fhome = request.form.get('home')
		fwork = request.form.get('work')
		fother = request.form.get('other')
		with engine.connect() as conn:
			conn.execute(text("UPDATE users SET home = :1, work_add = :2, other_add =:3 WHERE user_id = :user_id"),{'1':fhome, '2':fwork, '3':fother, 'user_id':user_id})
		# return "updated!!"
		return redirect(url_for('view_profile'))
	return render_template("addresses.html",user=user,id=user_id)

@app.route("/user/profile",methods=('GET','POST'))
def view_profile():
	user_id=session['id']
	user= find_user(user_id)
	if(request.method=='POST'):
		username=request.form.get('username')
		mail=request.form.get('email_id')
		contact=request.form.get('contact')
		with engine.connect() as conn:
			conn.execute(text("UPDATE users SET username = :1, mail = :2, phone_number =:3 WHERE user_id = :user_id"),{'1':username, '2':mail, '3':contact, 'user_id':user_id})
		return redirect(url_for('view_profile'))
	return render_template("my-profile.html",user=user,id=user_id)

@app.route("/user/orders")
def view_orders():
	user_id=session['id']
	menu = find_user_order(user_id)
	list=[]
	item={}
	for row in menu:
		with engine.connect() as conn:
			result = conn.execute(text("SELECT food_name, food_price, image_url FROM menus WHERE menu_id = :item_id"),{'item_id':row[4]})
			item[row[4]]=result.all()
		list.append(row[1])
	return render_template("my-orders.html",menu=menu,list=list,user_id=user_id, item=item)


@app.route("/user/contact_us",methods=('GET','POST'))
def contact():
	user_id=session['id']
	if(request.method=='POST'):
		name=request.form.get('name')
		mail=request.form.get('mail')
		message=request.form.get('message')
		with engine.connect() as conn:
			conn.execute(text("INSERT INTO contact_us (user_id, name_user, mail, message) VALUES (:1, :2, :3, :4)"),{'1':user_id, '2':name, '3':mail, '4':message})
		flash("succesfully submitted!!","success")
		return redirect(url_for('contact'))
	return render_template("contact-us.html",id=user_id)



@app.route("/user/cart")
def cart():
	user_id = session['id']
	total_price=0
	dict1={}
	dict2={}
	delivery_price=0
	with engine.connect() as conn:
		cart = conn.execute(text('SELECT * FROM my_cart WHERE user_id = :id'),{'id':user_id}).all()
	if(len(cart)):
		for row in cart:
			item_id = row[1]
			restaurant_id = row[2]
			with engine.connect() as conn:
				item = conn.execute(text('SELECT food_name, food_price, image_url FROM menus WHERE menu_id = :item_id'),{'item_id':item_id}).all()[0]
				name = conn.execute(text('SELECT restaurant_name FROM restaurants WHERE restaurant_id = :id'),{'id':restaurant_id}).all()[0]
			dict1[item_id]=item
			dict2[item_id]=name
			total_price+=row[5]*dict1[item_id][1]
			if total_price < 500:
				delivery_price = 50
			else: delivery_price = 0
	else: flash("you have not added any item to the cart!! pls add some thing.",'error')
	return render_template("my-cart.html", cart=cart, dict1=dict1, dict2=dict2, total_price=total_price, delivery_price=delivery_price)



@app.route("/add_to_cart")
def add_to_cart():
	restaurant_id=request.args.get('restaurant_id')
	item_id=request.args.get('item_id')
	user_id=session['id']
	with engine.connect() as conn:
		cart = conn.execute(text('SELECT * FROM my_cart WHERE user_id = :id AND item_id = :item_id'),{'id':user_id,'item_id':item_id}).all()
	if(len(cart)==0):
		with engine.connect() as conn:
			conn.execute(text('INSERT INTO my_cart (item_id, restaurant_id, user_id) VALUES (:1, :2, :3)'),{'1':item_id,'2':restaurant_id,'3':user_id})
	else:
		with engine.connect() as conn:
			conn.execute(text('UPDATE my_cart SET quantity = :quantity WHERE user_id = :id AND item_id = :item_id'),{'quantity':cart[0][5]+1,'id':user_id,'item_id':item_id})
	return redirect(url_for("user_rest_menu",restaurant_id=restaurant_id))


@app.route("/increase")
def increase_quantity():
	item_id=request.args.get('item_id')
	user_id=session['id']
	quantity=int(request.args.get('quantity'))
	with engine.connect() as conn:
		conn.execute(text('UPDATE my_cart SET quantity = :quantity WHERE item_id =:id AND user_id =:user_id'),{'quantity':quantity+1,'id':item_id,'user_id':user_id})
	return redirect(url_for("cart"))

@app.route("/decrease")
def decrease_quantity():
	item_id=request.args.get('item_id')
	user_id=session['id']
	quantity=int(request.args.get('quantity'))
	with engine.connect() as conn:
		if(quantity>1):
			conn.execute(text('UPDATE my_cart SET quantity = :quantity WHERE item_id =:id AND user_id =:user_id'),{'quantity':quantity-1,'id':item_id,'user_id':user_id})
		else:
			conn.execute(text('DELETE FROm my_cart WHERE item_id =:id AND user_id =:user_id'),{'id':item_id,'user_id':user_id})
	return redirect(url_for("cart"))

@app.route("/remove")
def remove():
	item_id=request.args.get('item_id')
	user_id=session['id']
	with engine.connect() as conn:
		conn.execute(text('DELETE FROM my_cart WHERE item_id =:id AND user_id =:user_id'),{'id':item_id,'user_id':user_id})
	return redirect(url_for("cart"))


@app.route("/user/<int:restaurant_id>")
def user_rest_menu(restaurant_id):
	menu = get_menu_user(restaurant_id)
	with engine.connect() as conn:
		restaurant=conn.execute(text('SELECT * FROM restaurants WHERE restaurant_id = :id'),{'id':restaurant_id}).all()[0]
	menu_starter = find_starter(menu)
	menu_dessert = find_dessert(menu)
	menu_main = find_main(menu)
	menu_drink = find_drink(menu)
	return render_template("user-restaurant-menu.html",menu_s = menu_starter, menu_d = menu_dessert, menu_m = menu_main, menu_dr = menu_drink, rest=restaurant)


@app.route("/user/pay",methods=('GET','POST'))
def pay():
	user_id=session['id']
	user = find_user(user_id)
	if(request.method=='POST'):
		global order_id1
		order_id1=order_id1+1
		option=request.form.get('flexRadioDefault')
		with engine.connect() as conn:
			cart = conn.execute(text('SELECT * FROM my_cart WHERE user_id =:user_id'),{'user_id':user_id}).all()
		for row in cart:
			with engine.connect() as conn:
				conn.execute(text('INSERT INTO pending_orders (user_id,restaurant_id,item_id,quantity,address, order_id) VALUES (:1,:2,:3,:4,:5, :6)'),{'1':user_id,'2':row[2],'3':row[1],'4':row[5],'5':option, '6':order_id1})
		with engine.connect() as conn:
			conn.execute(text('DELETE FROM my_cart WHERE user_id=:id'),{'id':user_id})
		flash("payment successful!! will reach to you soon!!",'success')
		return redirect(url_for("user_home"))
	return render_template("pay.html",user=user)

	# @app.route("/restaurant/pending")
	# def pending():


@app.route('/login', methods = ['GET', 'POST'])
def login():
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		password = request.form['password']
		with engine.connect() as conn:
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


@app.route('/signup', methods = ('GET', 'POST'))
def register():
	if request.method == 'POST' and 'name' in request.form and 'username' in request.form and 'password' in request.form and 'mail' in request.form and 'contact' in request.form:
		username = request.form['username']
		password = request.form['password']
		email = request.form['mail']
		contact = request.form['contact']
		name = request.form['name']
		a=False
		with engine.connect() as conn:
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
			with engine.connect() as conn:
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

@app.route('/logout')
def logout():
	session.pop('loggedin', None)
	session.pop('id', None)
	session.pop('username', None)   
	return redirect(url_for('login'))

@app.route('/restaurant/logout')
def restaurant_logout():
	session.pop('loggedin', None)
	session.pop('id1', None)
	session.pop('username', None)   
	return redirect(url_for('res_login'))

if(__name__=='__main__'):
	app.run(debug=True)
