
import click
from flask import current_app
from .db import db

@click.command(name='init-db')
def init_db_command():
    """Initialize the database."""
    app = current_app._get_current_object()
    with app.app_context():
        try:
            db.create_all()
            click.echo('Initialized the database')
        except Exception as e:
            click.echo(f"Exception occurred during db.create_all(): {e}")