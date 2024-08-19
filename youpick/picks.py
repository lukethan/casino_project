from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from youpick.auth import login_required
from youpick.db import get_db

bp = Blueprint('picks', __name__)

@bp.route("/picks")
def index():
    if request.method == "GET":
        return render_template("picks/index.html")
