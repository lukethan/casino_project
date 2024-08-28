import os

from flask import Flask, redirect, render_template, url_for
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from . import models

    
load_dotenv()

db = SQLAlchemy()
migrate = Migrate()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = os.getenv('SECRET_KEY'),
        SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')    
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    from .db import init_app
    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        import youpick.models

    
    from . import auth
    app.register_blueprint(auth.bp)

    @app.route("/test")
    def test():
        return "Success!"
        
    from . import picks
    app.register_blueprint(picks.bp)
    app.add_url_rule('/', endpoint='index')
    
    return app
