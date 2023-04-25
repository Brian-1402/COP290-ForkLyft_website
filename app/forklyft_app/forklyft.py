from flask import Flask, render_template, redirect, url_for, flash, request, session, Blueprint
from forklyft_app.db import get_db
from sqlalchemy import text
import re
from werkzeug.exceptions import abort
from forklyft_app import create_app # potential rename
# app=create_app()
bp=Blueprint("forklyft_bp",__name__)
# app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# app.config['MYSQL_DATABASE_USER']='root'
# app.config['MYSQL_DATABASE_PASSWORD']='password'
# app.config['MYSQL_DATABASE_DB']='restaurant'
# app.config['MYSQL_DATABASE_HOST']='localhost'
# mysql=MySQL(app)

# order_id1=19

def find_restaurant(restaurant_id):
	with get_db().connect() as conn:
		result = conn.execute(text("SELECT * FROM restaurants WHERE restaurant_id = :restaurant_id"),{'restaurant_id':restaurant_id}).all()
		if len(result)==0:
			abort(404)
		return result

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
	
def get_menu_item(food_name):
	with get_db().connect() as conn:
		result = conn.execute(text("SELECT * FROM menus WHERE UPPER(food_name) LIKE CONCAT('%', UPPER(:1) , '%')   "),{'1':food_name})
		return result.all()

def get_menu_user(restaurant_id):
	with get_db().connect() as conn:
		result = conn.execute(text('SELECT * FROM menus WHERE restaurant_id = :rest_id'),{'rest_id':restaurant_id})
		return result.all()
	
def get_restaurant():
	with get_db().connect() as conn:
		result = conn.execute(text('SELECT * FROM restaurants'))
		return result.all()

def find_menu(restaurant_id):
	with get_db().connect() as conn:
		result = conn.execute(text("SELECT * FROM menus WHERE restaurant_id = :restaurant_id"),{'restaurant_id':restaurant_id})
		# if result is None:
		# 	abort(404)
		return result.all()
	
def find_orders(client_id,client,status):
	with get_db().connect() as conn:
		result = conn.execute(text(f"SELECT * FROM orders WHERE {client}_id = :id AND order_status = :status ORDER BY order_item_id"),{'id':client_id, 'status':status})
		# if result is None:
		#     abort(404)
		return result.all()



def find_user(user_id):
	with get_db().connect() as conn:
		result = conn.execute(text("SELECT * FROM users WHERE user_id = :user_id"),{'user_id':user_id})
		# if result is None:
		# 	abort(404)
		return result.all()

def find_menu_category(menu,category):
	menu_category_items = []
	for item in menu:
		if item[3]==category:
			menu_category_items.append(item)
	return menu_category_items

def get_restaurant_items(res_name):
	with get_db().connect() as conn:
		result = conn.execute(text("SELECT * FROM restaurants WHERE UPPER(restaurant_name) LIKE CONCAT('%', UPPER(:1) , '%')   "),{'1':res_name})
		return result


@bp.route('/restaurant/login', methods = ['GET', 'POST'])
def res_login():
	if session.get('id1'):
		if session['id1']:
			return redirect(url_for('forklyft_bp.display_restaurant'))
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
			return redirect(url_for('forklyft_bp.display_restaurant'))
		else:
			flash("try again!! incorrect username or password!! sign up if new restaurant",'error')
	return render_template('restaurant-login.html')

@bp.route('/restaurant/signup', methods = ('GET', 'POST'))
def restaurant_register():
	if session.get('id1'):
		if session['id1']:
			return redirect(url_for('forklyft_bp.display_restaurant'))
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
		else:
			with get_db().connect() as conn:
				conn.execute(text("INSERT INTO restaurants (restaurant_username, restaurant_password, restaurant_name, restaurant_location) VALUES (:uname, :pass, :name, :loc)"),
						{'uname':username, 'pass':password, 'name':name, 'loc':location})
				conn.commit()
			msg1='You have successfully registered !'
			e1='success'
			a=True
		flash(msg1,e1)
		if(a):return redirect(url_for('forklyft_bp.res_login'))
		else: return redirect(url_for('forklyft_bp.restaurant_register'))
	return render_template('index.html')

@bp.route("/restaurant")
def display_restaurant():
	if not session.get('id1'):
		flash("you need to login first!!","error")
		return redirect(url_for('forklyft_bp.res_login'))
	restaurant_id=session['id1']
	rest1 = find_restaurant(restaurant_id)
	order = find_orders(restaurant_id,"restaurant","done")
	menu = find_menu(restaurant_id)
	return render_template("restaurant-home.html",rest=rest1,order=order,menu=menu)

@bp.route("/restaurant/menu")
def display_menu_restaurant():
	if not session.get('id1'):
		flash("you need to login first!!","error")
		return redirect(url_for('forklyft_bp.res_login'))
	restaurant_id = session['id1']
	rest = find_restaurant(restaurant_id)
	menu = find_menu(restaurant_id)
	menu_starter = find_menu_category(menu,"starter")
	menu_dessert = find_menu_category(menu,"dessert")
	menu_main = find_menu_category(menu,"main")
	menu_drink = find_menu_category(menu,"drink")
	return render_template("restaurant-menu.html",rest=rest, menu_s=menu_starter, menu_d = menu_dessert, menu_m = menu_main, menu_dr = menu_drink)

@bp.route("/restaurant/delete_from_menu")
def delete_from_menu():
	item_id=int(request.args.get('item_id'))
	if not session.get('id1'):
		flash("you need to login first!!","error")
		return redirect(url_for('forklyft_bp.res_login'))
	with get_db().connect() as conn:
			conn.execute(text('DELETE FROM menus WHERE menu_id=:item_id'),{'item_id':item_id})
			conn.commit()
	return redirect(url_for('forklyft_bp.display_menu_restaurant'))


@bp.route("/restaurant/add_item", methods = ('GET','POST'))
def display_add_form():
	if not session.get('id1'):
		flash("you need to login first!!","error")
		return redirect(url_for('forklyft_bp.res_login'))
	restaurant_id=session['id1']
	if(request.method == 'POST'):
		fname=request.form.get('food_name')
		fprice=request.form.get('price')
		ftype=request.form.get('type')
		furl=request.form.get('url')
		with get_db().connect() as conn:
			conn.execute(text('INSERT INTO menus(restaurant_id, image_url, food_name, food_price, food_type) VALUES (:1, :2, :3, :4, :5)'),
							{'1':restaurant_id, '2':furl, '3':fname, '4':fprice, '5':ftype})
			conn.commit()
		flash("item added","success")
		return redirect(url_for('forklyft_bp.display_menu_restaurant'))
	return render_template("restaurant-add-item.html",restaurant_id=restaurant_id)

@bp.route("/restaurant/order_his")
def order_history():
	if not session.get('id1'):
		flash("you need to login first!!","error")
		return redirect(url_for('forklyft_bp.res_login'))
	restaurant_id = session['id1']
	rest = find_restaurant(restaurant_id)
	menu = find_orders(restaurant_id,"restaurant","done")
	list=[]
	for row in menu:
		list.append(row[1])
	return render_template("order_history.html",rest=rest,menu=menu,list=list)


@bp.route("/restaurant/pending")
def pending():
	if not session.get('id1'):
		flash("you need to login first!!","error")
		return redirect(url_for('forklyft_bp.res_login'))
	restaurant_id = session['id1']
	# rest = find_restaurant(restaurant_id)
	menu = find_orders(restaurant_id,"restaurant","pending")
	list=[]
	for row in menu:
		list.append(row[1])
	return render_template("restaurant_pending.html",menu=menu,list=list)


@bp.route("/delete_order")
def delete_order_pending():
	if not session.get('id1'):
		flash("you need to login first!!","error")
		return redirect(url_for('forklyft_bp.res_login'))
	res_id = session['id1']
	order_id = request.args.get('order_id')
	with get_db().connect() as conn:
		conn.execute(text('UPDATE orders SET order_status = :status WHERE order_id = :order_id AND restaurant_id =:res_id'),{'status':'done' , 'order_id':order_id,'res_id':res_id})
		conn.commit()
	flash("order delivered!!","success")
	return redirect(url_for("forklyft_bp.pending"))


@bp.route("/user/<string:item1>")
def search(item1):
	if not session.get('id'):
		flash("you need to login first!!","error")
		return redirect(url_for('forklyft_bp.login'))
	user_id = session['id']
	items = get_menu_item(item1)
	name_items = get_restaurant_items(item1)
	if(items):
		restaurants=[]
		menus={}
		for item in items:
			restaurant = find_restaurant(item[2])[0]
			if restaurant not in restaurants:
				restaurants.append(restaurant)
			menu = find_menu(restaurant[0])[0][1]
			menus[restaurant[0]]=menu
	elif(name_items):
		name_items=name_items.all()
		restaurants=[]
		menus={}
		for item in name_items:
			restaurant = item
			restaurants.append(restaurant)
			menu = find_menu(restaurant[0])[0][1]
			menus[restaurant[0]]=menu
		return render_template("user-home-search-res.html",user_id=user_id,restaurants=restaurants, menus=menus)
	else:
		items=[]
		restaurants=[]
		menus={}
	return render_template("user-home-search.html",user_id=user_id, restaurants=restaurants, menus=menus,item1=item1)

@bp.route("/user",methods=('GET','POST'))
def user_home():
	if not session.get('id'):
		flash("you need to login first!!","error")
		return redirect(url_for('forklyft_bp.login'))
	user_id = session['id']
	if(request.method=='POST'):
		fsearch = request.form.get('search')
		return redirect(url_for('forklyft_bp.search',item1=fsearch))
	#! potential bug: assumes there are 8 restaurants existing already
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

	return render_template("user-home.html",user_id=user_id,menu=result, dict=dict, restaurant=restaurant,image=image)

@bp.route("/user/addresses",methods=('GET','POST'))
def address():
	if not session.get('id'):
		flash("you need to login first!!","error")
		return redirect(url_for('forklyft_bp.login'))
	user_id=session['id']
	user = find_user(user_id)
	if(request.method=='POST'):
		fhome = request.form.get('home')
		fwork = request.form.get('work')
		fother = request.form.get('other')
		with get_db().connect() as conn:
			conn.execute(text("UPDATE users SET home = :1, work_add = :2, other_add =:3 WHERE user_id = :user_id"),{'1':fhome, '2':fwork, '3':fother, 'user_id':user_id})
			conn.commit()
		if(fhome!=user[0][1] or fwork!=user[0][2] or fother!=user[0][3]):
			flash("addresses updated!!","success")
		return redirect(url_for('forklyft_bp.view_profile'))
	return render_template("addresses.html",user=user,id=user_id)

@bp.route("/user/profile",methods=('GET','POST'))
def view_profile():
	if not session.get('id'):
		flash("you need to login first!!","error")
		return redirect(url_for('forklyft_bp.login'))
	user_id=session['id']
	user= find_user(user_id)
	if(request.method=='POST'):
		username=request.form.get('username')
		mail=request.form.get('email_id')
		contact=request.form.get('contact')
		with get_db().connect() as conn:
			conn.execute(text("UPDATE users SET username = :1, mail = :2, phone_number =:3 WHERE user_id = :user_id"),{'1':username, '2':mail, '3':contact, 'user_id':user_id})
			conn.commit()
		if(username!=user[0][4] or mail!=user[0][7] or contact!=user[0][8]):
			flash("profile updated!! ","success")
		return redirect(url_for('forklyft_bp.view_profile'))
	return render_template("my-profile.html",user=user,id=user_id)

@bp.route("/user/orders")
def view_orders():
	if not session.get('id'):
		flash("you need to login first!!","error")
		return redirect(url_for('forklyft_bp.login'))
	user_id=session['id']
	orders = find_orders(user_id,"user","done")
	list=[]
	item={}
	for row in orders:
		with get_db().connect() as conn:
			result = conn.execute(text("SELECT food_name, food_price, image_url FROM menus WHERE menu_id = :item_id"),{'item_id':row[4]})
			item[row[4]]=result.all()
		list.append(row[1])
	return render_template("my-orders.html",menu=orders,list=list,user_id=user_id, item=item)


@bp.route("/user/contact_us",methods=('GET','POST'))
def contact():
	if not session.get('id'):
		flash("you need to login first!!","error")
		return redirect(url_for('forklyft_bp.login'))
	user_id=session['id']
	if(request.method=='POST'):
		name=request.form.get('name')
		mail=request.form.get('mail')
		message=request.form.get('message')
		with get_db().connect() as conn:
			conn.execute(text("INSERT INTO contact_us (user_id, name_user, mail, message) VALUES (:1, :2, :3, :4)"),{'1':user_id, '2':name, '3':mail, '4':message})
			conn.commit()
		flash("successfully submitted!!","success")
		return redirect(url_for('forklyft_bp.contact'))
	return render_template("contact-us.html",id=user_id)


@bp.route("/user/cart")
def cart():
	if not session.get('id'):
		flash("you need to login first!!","error")
		return redirect(url_for('forklyft_bp.login'))
	user_id = session['id']
	total_price=0
	dict1={}
	dict2={}
	delivery_price=0
	with get_db().connect() as conn:
		cart = conn.execute(text('SELECT * FROM orders WHERE user_id = :id AND order_status="cart" ORDER BY order_item_id'),{'id':user_id}).all()
	if(len(cart)):
		for row in cart:
			item_id = row[4]
			restaurant_id = row[2]
			with get_db().connect() as conn:
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

@bp.route("/add_to_cart", methods=['GET','POST'])
def add_to_cart():
	if not session.get('id'):
		flash("you need to login first!!","error")
		return redirect(url_for('forklyft_bp.login'))
	restaurant_id=request.args.get('restaurant_id')
	item_id=request.args.get('item_id')
	user_id=session['id']
	with get_db().connect() as conn:
		cart = conn.execute(text('SELECT * FROM orders WHERE user_id = :id AND order_status = "cart" ORDER BY order_item_id'),{'id':user_id}).all()
	if(len(cart)==0): # if user's cart is empty
		with get_db().connect() as conn:
			# order id is 1+ the order_id of the last row of the orders table, i.e., the previous cart's order_id+1
			orders=conn.execute(text('SELECT order_id FROM orders ORDER BY order_item_id DESC LIMIT 1')).fetchone()
			if orders==None:
				order_id=1
			else:
				order_id=orders[0]+1
			conn.execute(text('INSERT INTO orders (item_id, restaurant_id, user_id, order_id, order_status, quantity) VALUES (:1, :2, :3, :4, "cart", 1)'),{'1':item_id,'2':restaurant_id,'3':user_id, '4':order_id})
			conn.commit()
	else:
		order_id=cart[0][1]
		cart_item=[row for row in cart if row[4]==int(item_id)] # gets the item's row from cart
		with get_db().connect() as conn:
			if(len(cart_item)==0): # if item not in cart, insert
				conn.execute(text('INSERT INTO orders (item_id, restaurant_id, user_id, order_id, order_status, quantity) VALUES (:1, :2, :3, :4, "cart", 1)'),{'1':item_id,'2':restaurant_id,'3':user_id, '4':order_id})
			else: # if item in cart, increase quantity
				conn.execute(text('UPDATE orders SET quantity = :quantity WHERE user_id = :id AND item_id = :item_id  AND order_status = "cart"'),{'quantity':cart_item[0][5]+1,'id':user_id,'item_id':item_id})
			conn.commit()
	flash("item added to cart","success")
	return redirect(url_for("forklyft_bp.user_rest_menu",restaurant_id=restaurant_id))


@bp.route("/increase")
def increase_quantity():
	if not session.get('id'):
		flash("you need to login first!!","error")
		return redirect(url_for('forklyft_bp.login'))
	item_id=request.args.get('item_id')
	user_id=session['id']
	quantity=int(request.args.get('quantity')) #! resolve pylance error
	with get_db().connect() as conn:
		conn.execute(text('UPDATE orders SET quantity = :quantity WHERE item_id =:id AND user_id =:user_id AND order_status = "cart"'),{'quantity':quantity+1,'id':item_id,'user_id':user_id})
		conn.commit()
	return redirect(url_for("forklyft_bp.cart"))

@bp.route("/decrease")
def decrease_quantity():
	if not session.get('id'):
		flash("you need to login first!!","error")
		return redirect(url_for('forklyft_bp.login'))
	item_id=request.args.get('item_id')
	user_id=session['id']
	quantity=int(request.args.get('quantity'))
	with get_db().connect() as conn:
		if(quantity>1):
			conn.execute(text('UPDATE orders SET quantity = :quantity WHERE item_id =:id AND user_id =:user_id AND order_status = "cart"'),{'quantity':quantity-1,'id':item_id,'user_id':user_id})
			conn.commit()
		else:
			conn.execute(text('DELETE FROM orders WHERE item_id =:id AND user_id =:user_id AND order_status = "cart"'),{'id':item_id,'user_id':user_id})
			conn.commit()
	return redirect(url_for("forklyft_bp.cart"))

@bp.route("/remove")
def remove():
	if not session.get('id'):
		flash("you need to login first!!","error")
		return redirect(url_for('forklyft_bp.login'))
	item_id=request.args.get('item_id')
	user_id=session['id']
	with get_db().connect() as conn:
		conn.execute(text('DELETE FROM orders WHERE item_id =:id AND user_id =:user_id AND order_status = "cart"'),{'id':item_id,'user_id':user_id})
		conn.commit()
	return redirect(url_for("forklyft_bp.cart"))


@bp.route("/user/<int:restaurant_id>")
def user_rest_menu(restaurant_id):
	if not session.get('id'):
		flash("you need to login first!!","error")
		return redirect(url_for('forklyft_bp.login'))
	menu = get_menu_user(restaurant_id)
	with get_db().connect() as conn:
		restaurant=find_restaurant(restaurant_id)[0]
	menu_starter = find_menu_category(menu,"starter")
	menu_dessert = find_menu_category(menu,"dessert")
	menu_main = find_menu_category(menu,"main")
	menu_drink = find_menu_category(menu,"drink")
	return render_template("user-restaurant-menu.html",menu_s = menu_starter, menu_d = menu_dessert, menu_m = menu_main, menu_dr = menu_drink, rest=restaurant)


@bp.route("/user/pay",methods=('GET','POST'))
def pay():
	if not session.get('id'):
		flash("you need to login first!!","error")
		return redirect(url_for('forklyft_bp.login'))
	user_id=session['id']
	user = find_user(user_id)
	if(request.method=='POST'):
		option=request.form.get('flexRadioDefault')
		with get_db().connect() as conn:
			cart = conn.execute(text('UPDATE orders SET order_status = "pending", address = :address WHERE user_id =:user_id AND order_status = "cart"'),{'user_id':user_id, 'address':option})
			conn.commit()
		flash("payment successful!! will reach to you soon!!",'success')
		return redirect(url_for("forklyft_bp.user_home"))
	return render_template("pay.html",user=user)

@bp.route('/')
def main():
	return render_template("main.html")

@bp.route('/login', methods = ['GET', 'POST'])
def login():
	if session.get('id'):
		if (session['id']): 
			return redirect(url_for('forklyft_bp.user_home'))
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
			return redirect(url_for('forklyft_bp.user_home'))
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
		else:
			with get_db().connect() as conn:
				conn.execute(text("INSERT INTO users (username, user_pass, name_user, phone_number, mail) VALUES (:uname, :pass, :name, :contact, :email)"),
						{'uname':username, 'pass':password, 'name':name, 'contact':contact, 'email':email})
				conn.commit()
			msg1='You have successfully registered !'
			e1='success'
			a=True
		flash(msg1,e1)
		if(a):return redirect(url_for('forklyft_bp.login'))
		else: return redirect(url_for('forklyft_bp.register'))
	return render_template('user-signup.html')

@bp.route('/logout')
def logout():
	session.pop('loggedin', None)
	session.pop('id', None)
	session.pop('username', None)   
	return redirect(url_for('forklyft_bp.main'))

@bp.route('/restaurant/logout')
def restaurant_logout():
	session.pop('loggedin', None)
	session.pop('id1', None)
	session.pop('username', None)   
	return redirect(url_for('forklyft_bp.main'))


# if(__name__=='__main__'):
# 	app.run(debug=True)
