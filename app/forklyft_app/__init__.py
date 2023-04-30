from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__)
    app.config["DEBUG"] = False
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE="mysql://forklyft_project:forklyft@10.17.50.188:3306/forklyft_main",
    )
    if test_config:
        app.config.update(test_config)
    from forklyft_app import forklyft

    app.register_blueprint(forklyft.bp)

    return app
