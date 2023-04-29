drop table if exists restaurants;
drop table if exists menus;
drop table if exists orders;
drop table if exists users;
drop table if exists contact_us;
drop table if exists restaurant_reviews;


create table restaurants ( restaurant_id integer primary key auto_increment, restaurant_name text not null, restaurant_location text not null, restaurant_rating_sum integer default 1, restaurant_rating_count integer default 1, restaurant_username text not null, restaurant_password text not null, restaurant_img text);

create table menus ( menu_id integer primary key auto_increment, image_url text not null, restaurant_id integer, food_type text not null, food_name text not null, food_price integer not null, food_desc text );

create table orders ( order_item_id integer not null primary key auto_increment, order_id integer not null, restaurant_id integer not null, user_id integer not null, item_id integer not null, quantity integer not null, order_status text not null, address text default null);

create table users (user_id integer primary key auto_increment, home varchar(255), work_add text, other_add text, username text not null, name_user text not null, user_pass text not null, mail text, phone_number text);

create table contact_us (contact_id integer primary key auto_increment, user_id integer not null, name_user text not null, mail text not null, message text);

create table restaurant_reviews (review_id integer primary key auto_increment, review text, restaurant_id integer, user_id integer not null, sentiment text);