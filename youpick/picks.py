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
    picks = db.execute("SELECT * FROM picks").fetchall()
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
        ...    
    return render_template("picks/requests.html")

