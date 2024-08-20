from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from youpick.auth import login_required
from youpick.db import get_db

bp = Blueprint('picks', __name__)

@bp.route("/")
@login_required
def index():
    db = get_db()
    picks = db.execute("SELECT * FROM picks ORDER BY time DESC").fetchall()
    return render_template("picks/index.html", picks=picks)
    
@bp.route("/make", methods=('GET', 'POST'))
@login_required
def make():
    if request.method == "POST":
        title = request.form["pick_title"]
        body = request.form["pick_body"]
        error = None
        if not title:
            error = "Please add a title"
        elif not body:
            error = "Please add a body"
        if error == None:
            db = get_db()
            db.execute('INSERT INTO picks (user_id, title, body)' 'VALUES(?,?,?)', (g.user["id"], title, body))
            db.commit()
            return redirect("/")
        flash (error)
    return render_template("picks/make.html")
    
@bp.route("/requests", methods=('GET', 'POST'))
@login_required
def requests():
    if request.method == "POST":
        title = request.form["requests_title"]
        body = request.form["requests_body"]
        receive_user1 = request.form["receive_user"]
        error = None
        if not title:
            error = "Please add a title"
        elif not body:
            error = "Please add a body"
        elif receive_user1 == g.user["username"]:
            error = "Please select a recipient other than yourself"
        if error == None:
            db = get_db()
            print (receive_user1)
            receive_id = db.execute('SELECT username FROM users WHERE username = ?', (receive_user1,)).fetchone()
            if not receive_id:
                error = "Please enter valid recipient username"
            else:
                db.execute('INSERT INTO picks (user_id, title, body)' 'VALUES(?,?,?)', (g.user["id"], title, body))
                db.commit()
                picks_id = db.execute('SELECT id FROM picks WHERE user_id = ?', g.user["id"])
                db.execute('INSERT INTO location (id, locate)' 'VALUES(?, ?)', picks_id, "private")
                db.commit()
                db.execute('INSERT INTO requests (request_id, receive_id)' 'VALUES(?, ?)', g.user["id"], receive_id)
                db.commit()
                return redirect("/")
        flash (error)
    return render_template("picks/requests.html")

