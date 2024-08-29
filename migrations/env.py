import os
import logging
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from flask import current_app
from alembic import context
from dotenv import load_dotenv
from youpick import create_app, db  # Ensure you import your create_app function and db from your app module

# Load environment variables
load_dotenv()

# Configure Alembic
config = context.config
config.set_main_option('sqlalchemy.url', os.getenv('DATABASE_URL'))

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')

def get_engine():
    try:
        # This works with Flask-SQLAlchemy<3 and Alchemical
        return current_app.extensions['migrate'].db.get_engine()
    except (TypeError, AttributeError):
        # This works with Flask-SQLAlchemy>=3
        return current_app.extensions['migrate'].db.engine

def get_metadata():
    return db.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode.

    Configures the context with just a URL and not an Engine.
    Calls to context.execute() here emit the given string to the
    script output.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configur
