from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from app.routes import login_required
from app import db

bp = Blueprint('dashboard', __name__)

@bp.route('/dashboard', methods=('get'))
def dashboard():
    if 'user_id' not in g:
        flash('You must be logged in to access the dashboard.', 'warning')
        return redirect(url_for('auth.login'))
    else:
        return render_template('dashboard.html')
