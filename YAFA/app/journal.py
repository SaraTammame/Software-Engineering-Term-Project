from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

# from flaskr.auth import login_required
from app import get_db

from app import get_db

bp = Blueprint('journal', __name__, url_prefix='/journal')

@bp.route('/journal')
def journal():
    db = get_db()
    posts = db.execute(
        'SELECT j.id, title, body, created, author_id, username'
        ' FROM entry j JOIN user u ON j.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('journal.html')
