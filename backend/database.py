from sqlalchemy import create_engine
engine = create_engine("mysql+pymysql://qwjra5xnk6kiv8tnb301:pscale_pw_WJm3KptrwmSrZgOGb5hp9tyEi1logg23wviV3LnrKJ5@aws.connect.psdb.cloud/forklyft?charset=utf8mb4",
                       connect_args={
                            "ssl":{
                                "ssl_ca":"/etc/ssl/cert.pem"
                            }
                       })



