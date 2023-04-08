from flask import Flask


def create_app(test_config=None):
	app = Flask(__name__)
	app.config['DEBUG'] = True
	app.config.from_mapping(
		SECRET_KEY='dev',
		#default db link when running the app.
		DATABASE="mysql+pymysql://31s9ptbbg8hm4yzgzyqu:pscale_pw_kcIL7MfOJqeuIzKEuxkl3rXtmXQ7g1ETilgwoFI123x@aws.connect.psdb.cloud/forklyft?charset=utf8mb4")
		# DATABASE="mysql+pymysql://qwjra5xnk6kiv8tnb301:pscale_pw_WJm3KptrwmSrZgOGb5hp9tyEi1logg23wviV3LnrKJ5@aws.connect.psdb.cloud/forklyft?charset=utf8mb4") # old, not working
		
		#The above is for our main public database
		# DATABASE="mysql+pymysql://ir24qauqq7jdg7xoedc9:pscale_pw_YqN1PLLXwNkfN3avcbjzPOl6eaw69kNkl60ZFNtmxrZ@aws.connect.psdb.cloud/forklyft_test?charset=utf8mb4")
		#The above is for testing purposes only
	if test_config:
		app.config.update(test_config)
	# import .app as app
	from forklyft_app import forklyft
	app.register_blueprint(forklyft.bp)

	return app
