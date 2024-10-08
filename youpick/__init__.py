import os

from flask import Flask, redirect, render_template, url_for
from dotenv import load_dotenv
    
load_dotenv()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = os.getenv('SECRET_KEY'),
        DATABASE = os.path.join(app.instance_path, os.getenv('DATABASE_NAME'))
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    from . import db
    db.init_app(app)

    
    from . import auth
    app.register_blueprint(auth.bp)

    @app.route("/test")
    def test():
        return "Success!"
        
    from . import picks
    app.register_blueprint(picks.bp)
    app.add_url_rule('/', endpoint='index')
    
    return app
