from flask import current_app, g
from sqlalchemy import create_engine, text

# get_db() only works in a particular app context
def get_db():
    if "db" not in g:
        g.db = create_engine(current_app.config['DATABASE'])
                    #    ,connect_args={
                            # "ssl":{"ssl_ca":"/etc/ssl/cert.pem"}})
                            
    return g.db

def execute_db_file(db_instance,f):
    with db_instance.connect() as conn:
        data=f.readlines()
        for i in data:
            i=i.strip()
            if len(i)<1 or i[:2]=="--": # if empty line or comment, skip
                continue
            conn.execute(text(i.decode('utf-8')))
        conn.commit()

def init_db():
    with current_app.open_resource("schema.sql") as f:
        db=get_db()
        execute_db_file(db,f)

        # with get_db().connect() as conn:
        #     data=f.readlines()
        #     for i in data:
        #         i=i.strip()
        #         if len(i) < 3 or i[0]=="-":
        #             continue
        #         # print(data.decode('utf-8'))
        #         conn.execute(text(i.decode('utf-8')))


