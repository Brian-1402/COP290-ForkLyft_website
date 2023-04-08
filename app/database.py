from sqlalchemy import create_engine
engine = create_engine("mysql+pymysql://31s9ptbbg8hm4yzgzyqu:pscale_pw_kcIL7MfOJqeuIzKEuxkl3rXtmXQ7g1ETilgwoFI123x@aws.connect.psdb.cloud/forklyft?charset=utf8mb4",
                       connect_args={
                            "ssl":{
                                "ssl_ca":"/etc/ssl/cert.pem"
                            }
                       })



