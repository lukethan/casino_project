import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash

from .db import db
from .models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')
#Sets up the prefix auth for all routes in this module

#Used the tutorial from flask documentation for the auth setup
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirmation = request.form['confirmation']
        error = None

        if not username.strip():
            error = 'Please enter a username'
        elif not password.strip():
            error = 'Please enter a password'
        elif not confirmation.strip():
            error = 'Please confirm your password'
        elif password.strip() != confirmation.strip():
            error = 'Confirmation password entered incorrectly'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO users (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            #I like this integrity error, because I was querying the db and then comparing it to request.form
            except IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)
        #I like how the error is set by the conditional but it doesnt return until the end
        #I structure my code by returning render template after each flash which is inefficient

    return render_template('auth/register.html')



#Used the tutorital from flask documentation for the auth setup
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        user = db.execute(
            'SELECT * FROM users WHERE username = ?', (username,)
        ).fetchone()
        #This is phenomenal in terms of speeding up query and allowing for easier variable setting
        #It is annoying to specify var = [0]["key"] every time

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        #I understand sessions better now and how it is the server checking but can often be stored client side in a cookie
        #This is why the secret key is set so that the cookie can't be abused

        flash(error)

    return render_template('auth/login.html')

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)

#  @bp.before_app_request
# def load_logged_in_user():
#     user_id = session.get('user_id')

#     if user_id is None:
#         g.user = None
#     else:
#         g.user = get_db().execute(
#             'SELECT * FROM users WHERE id = ?', (user_id,)
#         ).fetchone()
#         #I like the g variable being used here if there is a session

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
    #Identical to finance assignment

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
#This is cool because it is basically taking whatever function the decorator is affixed to
#And passing it as an argument to this function. the **kwargs allows for any number of 
#key word arguments because we don't know how many we will need for each function that we decorate