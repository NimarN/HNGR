import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

#User authentication for registration
@bp.route('/register', methods=('GET', 'POST'))
def register():
    #check if request is post
    if request.method == 'POST':
        #save user input info 
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        #check if username and pass is both given
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        
        #If no error, try inserting username and password od user into databse
        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            # handles error if user is already in database
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                #if no errors, redirect to log in page
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    
    if request.method == 'POST':
        #save user input for log in 
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        #get username data from database
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        #if no user is returned, flash incorrect username
        if user is None:
            error = 'Incorrect username.'
        # check for correct password
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        #if all is good, redirect to home page
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('home.index'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    #set g to username to show logged in user
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

#logout function to clear session data, redirect to home page after logging out 
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home.index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view