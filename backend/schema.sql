drop table if exists restaurants;
drop table if exists menus;

create table restaurants(
    restaurant_id integer primary key autoincrement,
    restaurant_name text not null,
    restaurant_location text not null,
    -- restaurant_reviews text,
    restaurant_rating_sum integer,
    restaurant_rating_count integer
);

create table menus(
    menu_id integer primary key autoincrement,
    image_url text not null,
    restaurant_id integer,
    food_type text not null,
    food_name text not null,
    food_price integer not null,
    foreign key (restaurant_id) references restaurants(restaurant_id)
);