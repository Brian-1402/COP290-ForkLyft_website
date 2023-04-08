from flask import current_app, g
from sqlalchemy import create_engine

def get_db():
    if "db" not in g:
        g.db = create_engine(current_app.config['DATABASE'],
                       connect_args={
                            "ssl":{"ssl_ca":"/etc/ssl/cert.pem"}
                       })
    return g.db


# engine = create_engine(current_app.config['DATABASE'],
#                        connect_args={
#                             "ssl":{"ssl_ca":"/etc/ssl/cert.pem"}
#                        })



