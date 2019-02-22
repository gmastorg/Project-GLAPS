"""
Routes and views for the flask application.
"""
import functools

from flask import (
	Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from FrontEnd.db import get_db

#bp = Blueprint('auth', __name__, url_prefix='/auth')

from datetime import datetime
from flask import render_template
from FrontEnd import app

@app.route('/')
@app.route('/comingsoon')
def commingsoon():
    """
        Renders the count down page. This page is a place holder for right now.
    """
    return render_template(
        'comingsoon.html',
        title='Coming Soon',
        year=datetime.now().year
    )

@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'home.html',
        title='Home Page',
        year=datetime.now().year
    )

def login_required(view):
	"""View decorator that redirects anonymous users to the login page."""
	@functools.wraps(view)
	def wrapped_view(**kwargs):
		if g.user is None:
			return redirect(url_for('auth.login'))

		return view(**kwargs)

	return wrapped_view


#@app.before_app_request #'Flask' object has no attribute 'before_app_request
#def load_logged_in_user():
#	"""If a user id is stored in the session, load the user object from
#	the database into ``g.user``."""
#	user_id = session.get('user_id')

#	if user_id is None:
#		g.user = None
#	else:
#		g.user = get_db().execute(
#			'SELECT * FROM user WHERE id = ?', (user_id,)
#		).fetchone()

@app.route('/logout')
def logout():
	"""Clear the current session, including the stored user id."""
	session.clear()
	return redirect(url_for('comingsoon'))

@app.route('/login', methods=('GET', 'POST'))
def login():
	"""Log in a registered user by adding the user id to the session."""
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		db = get_db()
		error = None
		user = db.execute(
			'SELECT * FROM user WHERE username = ?', (username,)
		).fetchone()

		if user is None:
			error = 'Incorrect username.'
		elif not check_password_hash(user['password'], password):
			error = 'Incorrect password.'

		if error is None:
			# store the user id in a new session and return to the index
			session.clear()
			session['user_id'] = user['id']
			return redirect(url_for('comingsoon')) #Need to change to a new screen

		flash(error)

	return render_template('auth/login.html', title='Login', year=datetime.now().year)

@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        error = None

        # we're trying to add username to this command string
        #command_string = """SELECT id FROM users WHERE username = ?", (username,)
        #    ).fetchone() is not None:
        #    error = "User {0} is already registered."""
        command_string = "SELECT id from users WHERE username = ?{0}"
        command_string = command_string.format(username)
        print("---\ncommand_string is ", command_string, "\n---\n")
        if not username:
            error = 'Username is required.'
        elif not email:
            error = 'Email is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM users WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute('INSERT INTO users (username, email, password) VALUES (?,?,?)',(username, email, generate_password_hash(password)))
            db.commit()
            return redirect(url_for('login'))

            flash(error)

    return render_template('auth/register.html', title='Register', year=datetime.now().year)

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Learn about Geographic Location Attribute Predictor System (GLAPS).'
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Please Contact us with any questions or concerns.'
    )

#@app.route('/login')
#def login():
#    """Renders the login page."""
#    return render_template(
#        'login.html',
#        title='Login',
#        year=datetime.now().year,
#        message='Please login to continue'
#    )

#@app.route('/register')
#def register():
#    """Renders the register page."""

#    return render_template(
#        'register.html',
#        title='Register',
#        year=datetime.now().year,
#        message='Please register to take full advantage of GLAPS'
#    )