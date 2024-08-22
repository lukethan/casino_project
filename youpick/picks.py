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
    picks = db.execute("SELECT username, time, title, body FROM main JOIN users ON main.user_id = users.id ORDER BY time DESC").fetchall()
    pending = db.execute('SELECT username FROM users JOIN requests ON users.id = requests.request_id WHERE status = "pending" AND receive_id =?', (g.user["id"],))
    return render_template("picks/index.html", main=picks, pending=pending, page="index")
    
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
            db.execute('INSERT INTO main (user_id, title, body) VALUES(?,?,?)', (g.user["id"], title, body))
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
        elif error == None:
            db = get_db()
            id_receive = db.execute('SELECT id FROM users WHERE username = ?', (receive_user1,)).fetchone() 
            if id_receive == None:
                error = "Please enter valid recipient username"
                flash (error)
                return render_template("picks/requests.html")
            prevrequest = db.execute('SELECT * FROM requests WHERE request_id =? AND receive_id = ?', (id_receive["id"], g.user["id"])).fetchone()
            if prevrequest != None:
                if prevrequest["status"] != "accepted":
                    db.execute('UPDATE requests SET status = ? WHERE requests.id = ?', ("accepted", prevrequest["id"]))
                    db.execute('INSERT INTO requests (request_id, receive_id, status) VALUES(?, ?, ?)', (g.user["id"], id_receive["id"], "accepted"))
                db.execute('INSERT INTO private (user_id, recipient_id, title, body) VALUES(?, ?, ?, ?)', ((g.user["id"], id_receive["id"], title, body)))
                db.commit()
                return redirect("/")
            try:
                db.execute('INSERT INTO requests (request_id, receive_id) VALUES(?, ?)', (g.user["id"], id_receive["id"]))
                db.commit()
            except db.IntegrityError:
                status = db.execute('SELECT status FROM requests WHERE request_id =? AND receive_id = ?', ((g.user["id"]), id_receive["id"])).fetchone()
                if status["status"] == "pending":
                    error = "Request still pending!"
                elif status["status"] == "rejected":
                    error = "Your request has been rejected"
                else:  
                    db.execute('INSERT INTO private (user_id, recipient_id, title, body) VALUES(?, ?, ?, ?)', ((g.user["id"], id_receive["id"], title, body)))
                    db.commit()
                    return redirect("/")
            if error == None:
                db.execute('INSERT INTO private (user_id, recipient_id, title, body) VALUES(?, ?, ?, ?)', ((g.user["id"], id_receive["id"], title, body)))
                db.commit()
                return redirect("/")
        flash (error)
    return render_template("picks/requests.html")

@bp.route("/private", methods = ('GET','POST'))
@login_required
def private():
    db = get_db()
    if request.method == "POST":
        return render_template("picks/private.html", page="private")
    if request.method == "GET":
        pending = db.execute('SELECT username FROM users JOIN requests ON users.id = request_id AND status == "pending"')
        return render_template("picks/private.html", pending=pending)