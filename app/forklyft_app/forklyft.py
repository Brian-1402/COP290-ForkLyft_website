"""Main Flask Blueprint for forklyft_app

Contains the main helper functions and Flask views for our flask app.

"""


from flask import render_template, redirect, url_for, flash, request, session, Blueprint
from forklyft_app.db import get_db
from sqlalchemy import text
from werkzeug.exceptions import abort
import json
import requests

bp = Blueprint("forklyft_bp", __name__)


def find_restaurant(restaurant_id: int):
    """Returns restaurant details from the database using restaurant_id."""

    with get_db().connect() as conn:
        result = conn.execute(
            text("SELECT * FROM restaurants WHERE restaurant_id = :restaurant_id"),
            {"restaurant_id": restaurant_id},
        ).all()
        if len(result) == 0:
            abort(404)
        return result


def get_menu():
    """Returns entire menus table from the database."""

    with get_db().connect() as conn:
        result = conn.execute(text("SELECT * FROM menus"))
        return result.all()


def get_menu_item(food_name: str):
    """Searches the menus table in the database for specific menu item."""

    with get_db().connect() as conn:
        result = conn.execute(
            text(
                "SELECT * FROM menus WHERE UPPER(food_name) LIKE CONCAT('%', UPPER(:1) , '%')"
            ),
            {"1": food_name},
        )
        return result.all()


def get_menu_user(restaurant_id: int):
    """Returns items from menus table in the database specific to a restaurant.

    Used for displaying content in user restaurant menu page.
    """

    with get_db().connect() as conn:
        result = conn.execute(
            text("SELECT * FROM menus WHERE restaurant_id = :rest_id"),
            {"rest_id": restaurant_id},
        )
        return result.all()


def get_restaurant():
    """Returns all restaurants data from the database."""

    with get_db().connect() as conn:
        result = conn.execute(text("SELECT * FROM restaurants"))
        return result.all()


def find_menu(restaurant_id: int):
    """Returns menus data for the given restaurant from the database."""

    with get_db().connect() as conn:
        result = conn.execute(
            text("SELECT * FROM menus WHERE restaurant_id = :restaurant_id"),
            {"restaurant_id": restaurant_id},
        )
        # if result is None:
        # 	abort(404)
        return result.all()


def find_orders(client_id: int, client: str, status: str):
    """Returns data from orders table in the database, filtered on
    whether the client is user or restaurant, the client_id, and the order status.

    client : "user" or "restaurant"
    status : "done" or "pending" or "cart"
    """

    with get_db().connect() as conn:
        result = conn.execute(
            text(
                f"SELECT * FROM orders WHERE {client}_id = :id AND order_status = :status ORDER BY order_item_id"
            ),
            {"id": client_id, "status": status},
        )
        # if result is None:
        #     abort(404)
        return result.all()


def find_user(user_id: int):
    """Returns database data of a specific user from users table."""

    with get_db().connect() as conn:
        result = conn.execute(
            text("SELECT * FROM users WHERE user_id = :user_id"), {"user_id": user_id}
        )
        # if result is None:
        # 	abort(404)
        return result.all()


def find_menu_category(menu, category: str):
    """Takes the database menus table output as input,
    and filters out the menu items based on their category.

    category: "starter", "dessert", "main", "drink".
    """

    menu_category_items = []
    for item in menu:
        if item[3] == category:
            menu_category_items.append(item)
    return menu_category_items


def get_restaurant_items(res_name: str):
    """Searches for restaurants in the database using the keyword res_name."""

    with get_db().connect() as conn:
        result = conn.execute(
            text(
                "SELECT * FROM restaurants WHERE UPPER(restaurant_name) LIKE CONCAT('%', UPPER(:1) , '%')   "
            ),
            {"1": res_name},
        )
        return result


@bp.route("/restaurant/login", methods=["GET", "POST"])
def res_login():
    """Via GET request:
    Renders and displays the restaurant login page.

    Via POST request: submitting login form

    Searches for restaurant credentials in database,
        if not found, throw error flash message.
        If found, sets session values and redirect to restaurant home.
    """

    # If already logged in, redirect to restaurant home page
    if session.get("id1"):
        if session["id1"]:
            return redirect(url_for("forklyft_bp.display_restaurant"))

    if (
        request.method == "POST"
        and "restaurant_username" in request.form
        and "restaurant_password" in request.form
    ):
        username = request.form["restaurant_username"]
        password = request.form["restaurant_password"]
        with get_db().connect() as conn:
            restaurant = conn.execute(
                text(
                    "SELECT * FROM restaurants WHERE restaurant_username = :username AND BINARY restaurant_password = :password"
                ),
                {"username": username, "password": password},
            )
        restaurant = restaurant.all()

        if len(restaurant):
            restaurant = restaurant[0]
            session["loggedin"] = True
            session["id1"] = restaurant[0]
            session["username"] = restaurant[5]
            flash("successfully logged in!!", "success")
            return redirect(url_for("forklyft_bp.display_restaurant"))
        else:
            flash(
                "try again!! incorrect username or password!! sign up if new restaurant",
                "error",
            )

    return render_template("restaurant-login.html")


@bp.route("/restaurant/signup", methods=("GET", "POST"))
def restaurant_register():
    """Via GET request:
    Renders and displays the restaurant signup page.

    Via POST request: submitting signup form

    Form syntax checking (no empty fields correct email format, no special characters etc)
    are done in browser javascript.

    Searches for restaurant credentials in database,
        If found, throws error flash message.
        if not found, inserts the credentials into the database,
        redirects to login page and displays success flash message.
    """

    if session.get("id1"):
        if session["id1"]:
            return redirect(url_for("forklyft_bp.display_restaurant"))
    if (
        request.method == "POST"
        and "restaurant_name" in request.form
        and "username" in request.form
        and "password" in request.form
        and "location" in request.form
    ):
        username = request.form["username"]
        password = request.form["password"]
        location = request.form["location"]
        name = request.form["restaurant_name"]
        a = False
        with get_db().connect() as conn:
            restaurant = conn.execute(
                text("SELECT * FROM restaurants WHERE restaurant_username = :username"),
                {"username": username},
            )
        restaurant = restaurant.all()

        if len(restaurant):
            msg1 = "restaurant already exists !"
            e1 = "error"
        # elif not re.match(r'[A-Za-z0-9]+', username):
        # 	msg1 = 'username must contain only characters and numbers !'
        # 	e1='error'
        else:
            with get_db().connect() as conn:
                conn.execute(
                    text(
                        "INSERT INTO restaurants (restaurant_username, restaurant_password, restaurant_name, restaurant_location) VALUES (:uname, :pass, :name, :loc)"
                    ),
                    {
                        "uname": username,
                        "pass": password,
                        "name": name,
                        "loc": location,
                    },
                )
                conn.commit()
            msg1 = "You have successfully registered !"
            e1 = "success"
            a = True
        flash(msg1, e1)

        if a:
            return redirect(url_for("forklyft_bp.res_login"))
        else:
            return redirect(url_for("forklyft_bp.restaurant_register"))

    return render_template("index.html")


@bp.route("/restaurant")
def display_restaurant():
    """Home page for the restaurant portal.

    Takes reviews data from the database and displays according to their status.

    Forwards menu, past orders, restaurant data and reviews from
    the database to the html template and renders the restaurant home page.
    """

    if not session.get("id1"):
        flash("you need to login first!!", "error")
        return redirect(url_for("forklyft_bp.res_login"))
    restaurant_id = session["id1"]

    # The following block deals with classifying reviews
    cp = 0
    cn = 0
    color = {}
    with get_db().connect() as conn:
        review1 = conn.execute(
            text(
                "SELECT user_id,review,sentiment FROM restaurant_reviews WHERE restaurant_id = :rest_id"
            ),
            {"rest_id": restaurant_id},
        ).all()
    dict = {}
    for review in review1:
        if review[2] == "positive":
            cp = cp + 1
            color[review] = "green"
        else:
            cn = cn + 1
            color[review] = "red"
        user = find_user(review[0])[0]
        dict[review[0]] = user[4]

    rest1 = find_restaurant(restaurant_id)
    order = find_orders(restaurant_id, "restaurant", "done")
    menu = find_menu(restaurant_id)

    return render_template(
        "restaurant-home.html",
        rest=rest1,
        order=order,
        menu=menu,
        review1=review1,
        dict=dict,
        cp=cp,
        cn=cn,
        color=color,
    )


@bp.route("/restaurant/menu")
def display_menu_restaurant():
    """Menu page for restaurant portal

    Takes menu data, classifies it into categories,
    renders the menu page for the restaurant portal.
    """

    if not session.get("id1"):
        flash("you need to login first!!", "error")
        return redirect(url_for("forklyft_bp.res_login"))

    restaurant_id = session["id1"]
    rest = find_restaurant(restaurant_id)
    menu = find_menu(restaurant_id)
    menu_starter = find_menu_category(menu, "starter")
    menu_dessert = find_menu_category(menu, "dessert")
    menu_main = find_menu_category(menu, "main")
    menu_drink = find_menu_category(menu, "drink")

    return render_template(
        "restaurant-menu.html",
        rest=rest,
        menu_s=menu_starter,
        menu_d=menu_dessert,
        menu_m=menu_main,
        menu_dr=menu_drink,
    )


@bp.route("/restaurant/delete_from_menu")
def delete_from_menu():
    """Deletes menu item from database.

    Request is sent from delete button in restaurant portal menu page.

    Takes item_id from request parameters, deletes that item from
    menus table in the database.
    """

    if not session.get("id1"):
        flash("you need to login first!!", "error")
        return redirect(url_for("forklyft_bp.res_login"))

    item_id = int(request.args.get("item_id"))

    with get_db().connect() as conn:
        conn.execute(
            text("DELETE FROM menus WHERE menu_id=:item_id"), {"item_id": item_id}
        )
        conn.commit()

    return redirect(url_for("forklyft_bp.display_menu_restaurant"))


@bp.route("/restaurant/add_item", methods=("GET", "POST"))
def display_add_form():
    """Via GET request:
    Renders add item page for restaurant.

    Via POST request: filling add item form
    Inserts new menu item into the menus table in the database.
    """

    if not session.get("id1"):
        flash("you need to login first!!", "error")
        return redirect(url_for("forklyft_bp.res_login"))

    restaurant_id = session["id1"]
    if request.method == "POST":
        fname = request.form.get("food_name")
        fprice = request.form.get("price")
        ftype = request.form.get("type")
        furl = request.form.get("url")
        with get_db().connect() as conn:
            conn.execute(
                text(
                    "INSERT INTO menus(restaurant_id, image_url, food_name, food_price, food_type) VALUES (:1, :2, :3, :4, :5)"
                ),
                {"1": restaurant_id, "2": furl, "3": fname, "4": fprice, "5": ftype},
            )
            conn.commit()
        flash("item added", "success")
        return redirect(url_for("forklyft_bp.display_menu_restaurant"))

    return render_template("restaurant-add-item.html", restaurant_id=restaurant_id)


@bp.route("/restaurant/order_his")
def order_history():
    """Displays order history page for restaurant

    Takes completed orders from orders table in database for
    corresponding restaurant and renders order history page.
    """

    if not session.get("id1"):
        flash("you need to login first!!", "error")
        return redirect(url_for("forklyft_bp.res_login"))

    restaurant_id = session["id1"]
    rest = find_restaurant(restaurant_id)
    menu = find_orders(restaurant_id, "restaurant", "done")
    list = []
    for row in menu:
        list.append(row[1])

    return render_template("order_history.html", rest=rest, menu=menu, list=list)


@bp.route("/restaurant/pending")
def pending():
    """Displays pending orders page for restaurant

    Takes pending orders from orders table in database for
    corresponding restaurant and renders pending orders page.
    """

    if not session.get("id1"):
        flash("you need to login first!!", "error")
        return redirect(url_for("forklyft_bp.res_login"))

    restaurant_id = session["id1"]
    menu = find_orders(restaurant_id, "restaurant", "pending")
    list = []
    for row in menu:
        list.append(row[1])

    return render_template("restaurant_pending.html", menu=menu, list=list)


@bp.route("/delete_order")
def delete_order_pending():
    """Updates order status from pending to done.

    Takes order_id from request parameter, and updates corresponding
    restaurant's specific pending order to "done" status in the database.
    """

    if not session.get("id1"):
        flash("you need to login first!!", "error")
        return redirect(url_for("forklyft_bp.res_login"))

    res_id = session["id1"]
    order_id = request.args.get("order_id")
    with get_db().connect() as conn:
        conn.execute(
            text(
                "UPDATE orders SET order_status = :status WHERE order_id = :order_id AND restaurant_id =:res_id"
            ),
            {"status": "done", "order_id": order_id, "res_id": res_id},
        )
        conn.commit()
    flash("order delivered!!", "success")

    return redirect(url_for("forklyft_bp.pending"))


@bp.route("/user/<string:item1>")
def search(item1):
    """Displays a user search page after entering a particular string

    The string parameter item1 is the search term.

    Considers the search term as both menu item or restaurant name,
    searches the database seperately for either case. Renders different
    templates for the two cases also.
    """

    if not session.get("id"):
        flash("you need to login first!!", "error")
        return redirect(url_for("forklyft_bp.login"))

    user_id = session["id"]
    items = get_menu_item(item1)
    name_items = get_restaurant_items(item1)
    restaurants = []
    menus = {}

    # If the searched term is for a menu item
    if items:
        restaurants = []
        menus = {}
        for item in items:
            restaurant = find_restaurant(item[2])[0]
            if restaurant not in restaurants:
                restaurants.append(restaurant)
            menu = find_menu(restaurant[0])[0][1]
            menus[restaurant[0]] = menu

    # If the searched term is for a restaurant name
    elif name_items:
        name_items = name_items.all()
        restaurants = []
        menus = {}
        for item in name_items:
            restaurant = item
            restaurants.append(restaurant)
            menu = find_menu(restaurant[0])[0][1]
            menus[restaurant[0]] = menu

        return render_template(
            "user-home-search-res.html",
            user_id=user_id,
            restaurants=restaurants,
            menus=menus,
        )

    return render_template(
        "user-home-search.html",
        user_id=user_id,
        restaurants=restaurants,
        menus=menus,
        item1=item1,
    )


@bp.route("/user", methods=("GET", "POST"))
def user_home():
    """User home page suggesting 8 newest menu items and 8 top rated restaurants"""

    if not session.get("id"):
        flash("you need to login first!!", "error")
        return redirect(url_for("forklyft_bp.login"))

    user_id = session["id"]

    # When value is entered in search bar
    if request.method == "POST":
        fsearch = request.form.get("search")
        return redirect(url_for("forklyft_bp.search", item1=fsearch))

    # Gets latest 8 items added to menus table in database, to display in page as "hot new picks"
    result = get_menu()[-8:]
    dict = {}
    # rest_images={}
    for row in result:
        with get_db().connect() as conn:
            name = conn.execute(
                text(
                    "SELECT restaurant_name FROM restaurants WHERE restaurant_id = :id"
                ),
                {"id": row[2]},
            ).all()[0]
            # image = conn.execute(text('SELECT restaurant_img FROM restaurants WHERE restaurant_id = :id'),{'id':row[2]}).all()[0]
        dict[row[0]] = name
        # rest_images[row[0]]=image

    # calculates rating of all restaurants
    restaurant = get_restaurant()
    Li = []
    for row in restaurant:
        row = list(row)
        rating_sum = row[3]
        rating_count = row[4]
        row.insert(0, rating_sum / rating_count)
        row = tuple(row)
        Li.append(row)

    # sorts restaurants by rating, and takes highest 8 to display as "top rated restaurants"
    restaurant = sorted(Li, key=lambda x: x[0])
    restaurant = restaurant[-8:]
    image = []
    for row in restaurant:
        with get_db().connect() as conn:
            link = conn.execute(
                text("SELECT image_url FROM menus WHERE restaurant_id = :id"),
                {"id": row[1]},
            ).all()[0]
        image.append(link)

    return render_template(
        "user-home.html",
        user_id=user_id,
        menu=result,
        dict=dict,
        restaurant=restaurant,
        image=image,
    )


@bp.route("/user/addresses", methods=("GET", "POST"))
def address():
    """Via GET request:
    Renders addresses page showing user's 3 addresses.

    Via POST request:
    Assumes the address text field has been modified and updates
    the new values into the database.
    """

    if not session.get("id"):
        flash("you need to login first!!", "error")
        return redirect(url_for("forklyft_bp.login"))

    user_id = session["id"]
    user = find_user(user_id)

    # If update addresses button is pressed
    if request.method == "POST":
        fhome = request.form.get("home")
        fwork = request.form.get("work")
        fother = request.form.get("other")
        with get_db().connect() as conn:
            conn.execute(
                text(
                    "UPDATE users SET home = :1, work_add = :2, other_add =:3 WHERE user_id = :user_id"
                ),
                {"1": fhome, "2": fwork, "3": fother, "user_id": user_id},
            )
            conn.commit()
        if fhome != user[0][1] or fwork != user[0][2] or fother != user[0][3]:
            flash("addresses updated!!", "success")
        return redirect(url_for("forklyft_bp.view_profile"))

    return render_template("addresses.html", user=user, id=user_id)


@bp.route("/user/profile", methods=("GET", "POST"))
def view_profile():
    """Via GET request:
    Renders user profile page using details from users database

    Via POST request:
    Assumes the displayed text fields has been modified and updates
    the new values into the database.
    """

    if not session.get("id"):
        flash("you need to login first!!", "error")
        return redirect(url_for("forklyft_bp.login"))

    user_id = session["id"]
    user = find_user(user_id)

    # If update button is pressed
    if request.method == "POST":
        username = request.form.get("username")
        mail = request.form.get("email_id")
        contact = request.form.get("contact")
        with get_db().connect() as conn:
            conn.execute(
                text(
                    "UPDATE users SET username = :1, mail = :2, phone_number =:3 WHERE user_id = :user_id"
                ),
                {"1": username, "2": mail, "3": contact, "user_id": user_id},
            )
            conn.commit()
        if username != user[0][4] or mail != user[0][7] or contact != user[0][8]:
            flash("profile updated!! ", "success")
        return redirect(url_for("forklyft_bp.view_profile"))

    return render_template("my-profile.html", user=user, id=user_id)


@bp.route("/user/orders")
def view_orders():
    """Displays order history of user

    Accesses done orders of the user from orders table, and its
    corresponding details from the menus table in the database.
    """

    if not session.get("id"):
        flash("you need to login first!!", "error")
        return redirect(url_for("forklyft_bp.login"))

    user_id = session["id"]
    orders = find_orders(user_id, "user", "done")
    list = []
    item = {}
    for row in orders:
        with get_db().connect() as conn:
            result = conn.execute(
                text(
                    "SELECT food_name, food_price, image_url FROM menus WHERE menu_id = :item_id"
                ),
                {"item_id": row[4]},
            )
            if result:
                item[row[4]] = result.all()
        list.append(row[1])

    return render_template(
        "my-orders.html", menu=orders, list=list, user_id=user_id, item=item
    )


@bp.route("/user/contact_us", methods=("GET", "POST"))
def contact():
    """Via GET request:
    Renders the contact us page with text field inputs

    Via POST request:
    Inserts the inputted details into the contact_us table of the database.
    """

    if not session.get("id"):
        flash("you need to login first!!", "error")
        return redirect(url_for("forklyft_bp.login"))

    user_id = session["id"]
    if request.method == "POST":
        name = request.form.get("name")
        mail = request.form.get("mail")
        message = request.form.get("message")
        with get_db().connect() as conn:
            conn.execute(
                text(
                    "INSERT INTO contact_us (user_id, name_user, mail, message) VALUES (:1, :2, :3, :4)"
                ),
                {"1": user_id, "2": name, "3": mail, "4": message},
            )
            conn.commit()
        flash("successfully submitted!!", "success")
        return redirect(url_for("forklyft_bp.contact"))

    return render_template("contact-us.html", id=user_id)


@bp.route("/user/cart")
def cart():
    """Renders users cart page containing restaurant items

    Takes the users orders in "cart" status from the database,
    takes their corresponding details from menus and restaurants table
    and displays them.
    """

    if not session.get("id"):
        flash("you need to login first!!", "error")
        return redirect(url_for("forklyft_bp.login"))

    user_id = session["id"]
    total_price = 0
    dict1 = {}
    dict2 = {}
    delivery_price = 0
    with get_db().connect() as conn:
        cart = conn.execute(
            text(
                'SELECT * FROM orders WHERE user_id = :id AND order_status="cart" ORDER BY order_item_id'
            ),
            {"id": user_id},
        ).all()

    if len(cart):
        for row in cart:
            item_id = row[4]
            restaurant_id = row[2]
            with get_db().connect() as conn:
                item = conn.execute(
                    text(
                        "SELECT food_name, food_price, image_url FROM menus WHERE menu_id = :item_id"
                    ),
                    {"item_id": item_id},
                ).all()[0]
                name = conn.execute(
                    text(
                        "SELECT restaurant_name FROM restaurants WHERE restaurant_id = :id"
                    ),
                    {"id": restaurant_id},
                ).all()[0]
            dict1[item_id] = item
            dict2[item_id] = name
            total_price += row[5] * dict1[item_id][1]
            if total_price < 500:
                delivery_price = 50
            else:
                delivery_price = 0
    else:
        flash("you have not added any item to the cart!! pls add some thing.", "error")

    return render_template(
        "my-cart.html",
        cart=cart,
        dict1=dict1,
        dict2=dict2,
        total_price=total_price,
        delivery_price=delivery_price,
    )


@bp.route("/add_to_cart", methods=["GET", "POST"])
def add_to_cart():
    """Adds corresponding menu item to user cart

    Triggered when pressing the add to cart button under each item in
    restaurant menu page.

    Items added to cart are inserted into the orders table in database
    with "cart" as order_status.
    """

    if not session.get("id"):
        flash("you need to login first!!", "error")
        return redirect(url_for("forklyft_bp.login"))

    restaurant_id = request.args.get("restaurant_id")
    item_id = request.args.get("item_id")
    user_id = session["id"]
    with get_db().connect() as conn:
        cart = conn.execute(
            text(
                'SELECT * FROM orders WHERE user_id = :id AND order_status = "cart" ORDER BY order_item_id'
            ),
            {"id": user_id},
        ).all()
    if len(cart) == 0:  # if user's cart is empty
        with get_db().connect() as conn:
            # order id is 1+ the order_id of the last row of the orders table, i.e., the previous cart's order_id+1
            orders = conn.execute(
                text("SELECT order_id FROM orders ORDER BY order_item_id DESC LIMIT 1")
            ).fetchone()
            if orders == None:
                order_id = 1
            else:
                order_id = orders[0] + 1
            conn.execute(
                text(
                    'INSERT INTO orders (item_id, restaurant_id, user_id, order_id, order_status, quantity) VALUES (:1, :2, :3, :4, "cart", 1)'
                ),
                {"1": item_id, "2": restaurant_id, "3": user_id, "4": order_id},
            )
            conn.commit()
    else:
        order_id = cart[0][1]
        cart_item = [
            row for row in cart if row[4] == int(item_id)
        ]  # gets the item's row from cart
        with get_db().connect() as conn:
            if len(cart_item) == 0:  # if item not in cart, insert
                conn.execute(
                    text(
                        'INSERT INTO orders (item_id, restaurant_id, user_id, order_id, order_status, quantity) VALUES (:1, :2, :3, :4, "cart", 1)'
                    ),
                    {"1": item_id, "2": restaurant_id, "3": user_id, "4": order_id},
                )
            else:  # if item in cart, increase quantity
                conn.execute(
                    text(
                        'UPDATE orders SET quantity = :quantity WHERE user_id = :id AND item_id = :item_id  AND order_status = "cart"'
                    ),
                    {
                        "quantity": cart_item[0][5] + 1,
                        "id": user_id,
                        "item_id": item_id,
                    },
                )
            conn.commit()
    flash("item added to cart", "success")

    return redirect(url_for("forklyft_bp.user_rest_menu", restaurant_id=restaurant_id))


@bp.route("/increase")
def increase_quantity():
    """Increments quantity of item in cart in orders table in database

    Link is on a button under each item shown in user's my_cart page.
    """

    if not session.get("id"):
        flash("you need to login first!!", "error")
        return redirect(url_for("forklyft_bp.login"))

    item_id = request.args.get("item_id")
    user_id = session["id"]
    quantity = int(request.args.get("quantity"))
    with get_db().connect() as conn:
        conn.execute(
            text(
                'UPDATE orders SET quantity = :quantity WHERE item_id =:id AND user_id =:user_id AND order_status = "cart"'
            ),
            {"quantity": quantity + 1, "id": item_id, "user_id": user_id},
        )
        conn.commit()

    return redirect(url_for("forklyft_bp.cart"))


@bp.route("/decrease")
def decrease_quantity():
    """Decrements quantity of item in cart in orders table in database

    Link is on a button under each item shown in user's my_cart page.

    If quantity was 1 when button was pressed, deletes the cart item
    from orders table in database.
    """

    if not session.get("id"):
        flash("you need to login first!!", "error")
        return redirect(url_for("forklyft_bp.login"))

    item_id = request.args.get("item_id")
    user_id = session["id"]
    quantity = int(request.args.get("quantity"))
    with get_db().connect() as conn:
        if quantity > 1:
            conn.execute(
                text(
                    'UPDATE orders SET quantity = :quantity WHERE item_id =:id AND user_id =:user_id AND order_status = "cart"'
                ),
                {"quantity": quantity - 1, "id": item_id, "user_id": user_id},
            )
            conn.commit()
        # if quantity is 1, delete item
        else:
            conn.execute(
                text(
                    'DELETE FROM orders WHERE item_id =:id AND user_id =:user_id AND order_status = "cart"'
                ),
                {"id": item_id, "user_id": user_id},
            )
            conn.commit()

    return redirect(url_for("forklyft_bp.cart"))


@bp.route("/remove")
def remove():
    """deletes item in cart from orders table in database

    Link is a button under each item shown in user's my_cart page.
    """

    if not session.get("id"):
        flash("you need to login first!!", "error")
        return redirect(url_for("forklyft_bp.login"))

    item_id = request.args.get("item_id")
    user_id = session["id"]
    with get_db().connect() as conn:
        conn.execute(
            text(
                'DELETE FROM orders WHERE item_id =:id AND user_id =:user_id AND order_status = "cart"'
            ),
            {"id": item_id, "user_id": user_id},
        )
        conn.commit()

    return redirect(url_for("forklyft_bp.cart"))


@bp.route("/user/<int:restaurant_id>", methods=("GET", "POST"))
def user_rest_menu(restaurant_id):
    """Via GET request:
    Renders the restaurant menu page in user portal.

    Takes menu data of the restaurant from the database,
    categorises them and displays in rendered webpage.

    Also takes reviews data from database, categorises them
    and displays with appropriate color, green for positive,
    red for negative.

    Via POST request:
    Takes review text as input, makes use of ML API to classify
    review as positive or negative, gives appropriate flash response
    and adds review and its category to database.


    """

    if not session.get("id"):
        flash("you need to login first!!", "error")
        return redirect(url_for("forklyft_bp.login"))

    menu = get_menu_user(restaurant_id)
    with get_db().connect() as conn:
        restaurant = find_restaurant(restaurant_id)[0]
    menu_starter = find_menu_category(menu, "starter")
    menu_dessert = find_menu_category(menu, "dessert")
    menu_main = find_menu_category(menu, "main")
    menu_drink = find_menu_category(menu, "drink")
    user_id = session["id"]

    cp = 0
    cn = 0
    color = {}
    with get_db().connect() as conn:
        review1 = conn.execute(
            text(
                "SELECT user_id,review,sentiment FROM restaurant_reviews WHERE restaurant_id = :rest_id"
            ),
            {"rest_id": restaurant_id},
        ).all()
    dict = {}
    for review in review1:
        if review[2] == "positive":
            cp = cp + 1
            color[review] = "green"
        else:
            cn = cn + 1
            color[review] = "red"
        user = find_user(review[0])[0]
        dict[review[0]] = user[4]

    if request.method == "POST":
        rating = int(request.form.get("rating"))
        review = request.form.get("review")
        url = "https://hf.space/embed/Amrrs/gradio-sentiment-analyzer/+/api/predict/"
        headers = {"Content-Type": "application/json"}
        data = {"data": [review]}
        response = requests.post(url, headers=headers, data=json.dumps(data))
        result = json.loads(response.text)

        if result["data"][0][12:20] == "POSITIVE":
            message = "Thank you for your kind feedback!!"
            s = "positive"
        else:
            message = "Thank you for your feedback, We shall try to improve!!"
            s = "negative"
        with get_db().connect() as conn:
            conn.execute(
                text(
                    "INSERT INTO restaurant_reviews(review,restaurant_id,user_id,sentiment) VALUES (:1, :2, :3, :4)"
                ),
                {"1": review, "2": restaurant_id, "3": user_id, "4": s},
            )
            conn.commit()
        with get_db().connect() as conn:
            conn.execute(
                text(
                    "UPDATE restaurants SET restaurant_rating_sum = restaurant_rating_sum + :1 , restaurant_rating_count = restaurant_rating_count + 1 WHERE restaurant_id = :rest_id "
                ),
                {"1": rating, "rest_id": restaurant_id},
            )
            conn.commit()
        flash(message, "success")

        return redirect(
            url_for("forklyft_bp.user_rest_menu", restaurant_id=restaurant_id)
        )

    return render_template(
        "user-restaurant-menu.html",
        menu_s=menu_starter,
        menu_d=menu_dessert,
        menu_m=menu_main,
        menu_dr=menu_drink,
        rest=restaurant,
        review1=review1,
        dict=dict,
        color=color,
        cp=cp,
        cn=cn,
    )


@bp.route("/user/pay", methods=("GET", "POST"))
def pay():
    """Via GET request:
    Renders payment portal where user chooses address.

    Via POST request:

    Considers payment done and updates order status from "cart"
    to "pending" in the database.
    """

    if not session.get("id"):
        flash("you need to login first!!", "error")
        return redirect(url_for("forklyft_bp.login"))

    user_id = session["id"]
    user = find_user(user_id)

    if request.method == "POST":
        option = request.form.get("flexRadioDefault")
        with get_db().connect() as conn:
            cart = conn.execute(
                text(
                    'UPDATE orders SET order_status = "pending", address = :address WHERE user_id =:user_id AND order_status = "cart"'
                ),
                {"user_id": user_id, "address": option},
            )
            conn.commit()
        flash("payment successful!! will reach to you soon!!", "success")
        return redirect(url_for("forklyft_bp.user_home"))

    return render_template("pay.html", user=user)


@bp.route("/")
def main():
    """Renders the index page of the website"""

    return render_template("main.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    """Via GET request:
    renders user login page.

    Via POST request:
    Takes form input values, checks if they already exist in database,
    if exists, updates the session values and redirects to home page.
    if does not exist, throws error flash message.
    """

    if session.get("id"):
        if session["id"]:
            return redirect(url_for("forklyft_bp.user_home"))

    if (
        request.method == "POST"
        and "username" in request.form
        and "password" in request.form
    ):
        username = request.form["username"]
        password = request.form["password"]
        with get_db().connect() as conn:
            user = conn.execute(
                text(
                    "SELECT * FROM users WHERE username = :username AND BINARY user_pass = :password"
                ),
                {"username": username, "password": password},
            )
        user = user.all()

        if len(user):
            user = user[0]
            session["loggedin"] = True
            session["id"] = user[0]
            session["username"] = user[4]
            flash("successfully logged in!!", "success")
            return redirect(url_for("forklyft_bp.user_home"))
        else:
            flash(
                "try again!! incorrect username or password!! sign up if new user",
                "error",
            )

    return render_template("user-login.html")


@bp.route("/signup", methods=("GET", "POST"))
def register():
    """Via GET request:
    renders user signup page.

    Via POST request:
    Takes form input, checks with database whether user already exists,
    if exists, throws error flash message,
    if doesn't exist, inserts into the database the credentials and
    redirects to login page.

    Assumes that the form validation (proper email address, no symbols etc)
    are done in browser javascript.
    """

    if (
        request.method == "POST"
        and "name" in request.form
        and "username" in request.form
        and "password" in request.form
        and "mail" in request.form
        and "contact" in request.form
    ):
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["mail"]
        contact = request.form["contact"]
        name = request.form["name"]
        a = False
        with get_db().connect() as conn:
            user = conn.execute(
                text("SELECT * FROM users WHERE username = :username"),
                {"username": username},
            )
        user = user.all()
        if len(user):
            msg1 = "Account already exists !"
            e1 = "error"
        else:
            with get_db().connect() as conn:
                conn.execute(
                    text(
                        "INSERT INTO users (username, user_pass, name_user, phone_number, mail) VALUES (:uname, :pass, :name, :contact, :email)"
                    ),
                    {
                        "uname": username,
                        "pass": password,
                        "name": name,
                        "contact": contact,
                        "email": email,
                    },
                )
                conn.commit()
            msg1 = "You have successfully registered !"
            e1 = "success"
            a = True
        flash(msg1, e1)
        if a:
            return redirect(url_for("forklyft_bp.login"))
        else:
            return redirect(url_for("forklyft_bp.register"))
    return render_template("user-signup.html")


@bp.route("/logout")
def logout():
    """Removes session values and redirects to index page"""

    session.pop("loggedin", None)
    session.pop("id", None)
    session.pop("username", None)
    return redirect(url_for("forklyft_bp.main"))


@bp.route("/restaurant/logout")
def restaurant_logout():
    """Removes session values and redirects to index page"""

    session.pop("loggedin", None)
    session.pop("id1", None)
    session.pop("username", None)
    return redirect(url_for("forklyft_bp.main"))


# if(__name__=='__main__'):
# 	app.run(debug=True)
