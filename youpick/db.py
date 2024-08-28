import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from . import db, migrate

# db = SQLAlchemy()
# migrate = Migrate()

def init_app(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')  # PostgreSQL URL
    db.init_app(app)
    migrate.init_app(app, db)
    
    @app.cli.command('init-db')
    def init_db_command():
        """Initialize the database."""
        with app.app_context():
            db.create_all()
        click.echo('Initialized the database')