-- drop table if exists restaurants;
-- drop table if exists menus;
-- drop table if exists orders;
drop table if exists my_cart;
-- drop table if exists orders;
-- drop table if exists pending_orders;
drop table if exists users;
-- drop table if exists contact_us;


-- create table restaurants ( restaurant_id integer primary key auto_increment, restaurant_name text not null, restaurant_location text not null, restaurant_rating_sum integer default 1, restaurant_rating_count integer default 1, restaurant_username text not null, restaurant_password text not null);

-- create table menus ( menu_id integer primary key auto_increment, image_url text not null, restaurant_id integer, food_type text not null, food_name text not null, food_price integer not null, food_desc text );

-- create table orders ( order_index integer not null primary key auto_increment, order_id integer not null, restaurant_id integer not null, user_id integer not null, item_id integer not null, quantity integer not null );

create table my_cart (cart_id integer primary key auto_increment not null, item_id integer not null, restaurant_id integer not null, user_id integer not null, order_id integer NOT NULL, quantity integer not null default 1);

-- create table pending_orders (p_order_id integer primary key auto_increment, user_id integer not null, restaurant_id integer not null, item_id integer, quantity integer not null, address text not null, order_id int NOT NULL);

create table users (user_id integer primary key auto_increment, home varchar(255), work_add text, other_add text, username text not null, name_user text not null, user_pass text not null, mail text, phone_number text);

-- create table contact_us (contact_id integer primary key auto_increment, user_id integer not null, name_user text not null, mail text not null, message text);