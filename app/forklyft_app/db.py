from flask import current_app, g
from sqlalchemy import create_engine, text

def get_db():
    if "db" not in g:
        g.db = create_engine(current_app.config['DATABASE'])
                    #    ,connect_args={
                            # "ssl":{"ssl_ca":"/etc/ssl/cert.pem"}})
                            
    return g.db


# engine = create_engine(current_app.config['DATABASE'],
#                        connect_args={
#                             "ssl":{"ssl_ca":"/etc/ssl/cert.pem"}
#                        })


def init_db():
    with current_app.open_resource("schema.sql") as f:
        with get_db().connect() as conn:
            data=f.readlines()
            for i in data:
                i=i.strip()
                if len(i) < 3 or i[0]=="-":
                    continue
                # print(data.decode('utf-8'))
                conn.execute(text(i.decode('utf-8')))
            # conn.execute(text("drop table if exists users;"))
            # conn.execute(text("create table users ( user_id integer primary key auto_increment, home varchar(255), work_add text, other_add text, username text not null, name_user text not null, mail text, phone_number text, user_pass text not null);"))
            # conn.execute(text("create table restaurants ( restaurant_id integer primary key auto_increment, restaurant_name text not null,restaurant_location text not null, restaurant_rating_sum integer default 1, restaurant_rating_count integer default 1, restaurant_username text not null unique, restaurant_password text not null);"))
                # conn.execute(text(f.readline().decode('utf-8')))
