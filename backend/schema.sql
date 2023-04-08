drop table if exists restaurants;
drop table if exists menus;
drop table if exists orders;

create table restaurants(
    restaurant_id integer primary key autoincrement,
    restaurant_name text not null,
    restaurant_location text not null,
    restaurant_rating_sum integer,
    restaurant_rating_count integer,
    restaurant_username text not null distinct,
    restaurant_password text not null,
);

create table menus(
    menu_id integer primary key autoincrement,
    image_url text not null,
    restaurant_id integer,
    food_type text not null,
    food_name text not null,
    food_price integer not null,
    food_desc text
);

create table orders(
    index integer primary key autoincrement,
    order_id integer not null,
    restaurant_id integer not null,
    user_id integer not null,
    item_id integer not null,
    quantity integer not null
);

-- create table users(
--     user_id integer primary key autoincrement,
--     home text,
--     work text,
--     other text,
--     username text not null distinct,
--     name_user text not null,
--     mail text,
--     phone_number text,
--     user_pass text not null
-- );

-- create table contact_us(
-- 	contact_id integer primary key auto_increment,
--     user_id integer not null,
--     name_user text not null,
--     mail text not null,
--     message text
-- );