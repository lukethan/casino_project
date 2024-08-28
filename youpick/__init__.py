import os
from flask import Flask
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    # Load default config and override with test_config if provided
    app.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_KEY', 'default_secret_key'),
        SQLALCHEMY_DATABASE_URI=os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///default.db'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    if test_config:
        app.config.from_mapping(test_config)
    else:
        app.config.from_pyfile('config.py', silent=True)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)



    # Import and register blueprints within app context to avoid circular imports
    with app.app_context():
        from . import models  # Import models here to ensure they're registered with db
        from . import auth
        from . import picks
        try:
            # Ensure all models are imported to register them with SQLAlchemy
            from .models import User, Main, Private, Request, Comment
            db.create_all()  # Create database tables
        except Exception as exception:
            print("Exception occurred during db.create_all(): " + str(exception))
        finally:
            print("db.create_all() was executed.")
    


        app.register_blueprint(auth.bp)
        app.register_blueprint(picks.bp)

        # Define any routes directly in the app context
        @app.route("/test")
        def test():
            return "Success!"
        
        # Add URL rules if needed
        app.add_url_rule('/', endpoint='index')

    return app


# import os

# from flask import Flask, redirect, render_template, url_for
# from dotenv import load_dotenv
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate

    
# load_dotenv()

# db = SQLAlchemy()
# migrate = Migrate()

# def create_app(test_config=None):
#     app = Flask(__name__, instance_relative_config=True)
#     app.config.from_mapping(
#         SECRET_KEY = os.getenv('SECRET_KEY'),
#         SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    
#     )

#     if test_config is None:
#         app.config.from_pyfile('config.py', silent=True)
#     else:
#         app.config.from_mapping(test_config)

#     try:
#         os.makedirs(app.instance_path)
#     except OSError:
#         pass


#     # from .db import init_app
#     db.init_app(app)
#     migrate.init_app(app, db)

#     with app.app_context():
#         import youpick.models

    
#     from . import auth
#     app.register_blueprint(auth.bp)

#     @app.route("/test")
#     def test():
#         return "Success!"
        
#     from . import picks
#     app.register_blueprint(picks.bp)
#     app.add_url_rule('/', endpoint='index')
    
#     return app
