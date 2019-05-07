"""
Routes and views for the flask application.
"""
import functools
import os
import csv
import requests
import json

from flask import (
	Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from FrontEnd.db import get_db
from datetime import datetime
from flask import render_template, Markup
from FrontEnd import app

@app.route('/')
@app.route('/home')
def home():
    load_logged_in_user()
    """Renders the home page."""
    return render_template('home.html',
        title='Home Page',
        year=datetime.now().year)

#Region - Log In information
@app.route('/login', methods=('GET', 'POST'))
def login():
	"""Log in a registered user by adding the user id to the session."""
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		db = get_db()
		error = None
		user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()

		if user is None:
			error = 'Incorrect username.'
		elif not check_password_hash(user['password'], password):
			error = 'Incorrect password.'

		if error is None:
			# store the user id in a new session and return to the index
			session.clear()
			session['user_id'] = user['id']
			return redirect(url_for('home'))

		flash(error)

	return render_template('auth/login.html', title='Login', year=datetime.now().year)

def login_required(view):
	"""View decorator that redirects anonymous users to the login page."""
	@functools.wraps(view)
	def wrapped_view(**kwargs):
		if g.user is None:
			return redirect(url_for('auth.login'))

		return view(**kwargs)

	return wrapped_view

def load_logged_in_user():
	"""If a user id is stored in the session, load the user object from
	the database into ``g.user``."""
	user_id = session.get('user_id')

	if user_id is None:
		g.user = None
	else:
		g.user = get_db().execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()

@app.route('/logout')
def logout():
	"""Clear the current session, including the stored user id."""
	session.clear()
	return redirect(url_for('comingsoon'))
#end Region
@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        error = None
        # we're trying to add username to this command string
        #command_string = """SELECT id FROM users WHERE username = ?",
        #(username,)
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
        elif db.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute('INSERT INTO users (username, email, password) VALUES (?,?,?)',(username, email, generate_password_hash(password)))
            db.commit()
            return redirect(url_for('login'))

            flash(error)

    return render_template('auth/register.html', title='Register', year=datetime.now().year)

@app.route('/comingsoon')
def comingsoon():
    """
        Renders the count down page. This page is a place holder for right now.
    """
    return render_template('comingsoon.html',
        title='Coming Soon',
        year=datetime.now().year)

app.config["DEBUG"] = True
@app.route('/glaps', methods=["GET","POST"]) #this section is used for when the data bases are linked.
def glaps():
    load_logged_in_user()
    States_Counties = getState_CountiesList()
    valueError = ""
    countyError = ""
    if request.method == "POST":
        County = None
        HomeVal = None

        County = request.form['County']

        if County == "" or County == None:
            countyError = Markup("<font color = red><bold>Please enter a County<bold></font>")
        try:
            HomeVal = int(request.form["HomeVal"])
        except:
            valueError = Markup("<font color = red><bold>Please enter a Home Value<bold></font>")
        if County != "" and HomeVal is not None and County != None:
            for item in States_Counties:
                if County == item:
                    result = getAPI()
                    result = list(result[0].values())

                    actualNoStad = str("{:,}".format(result[0]))
                    actualWStad = str("{:,}".format(result[1]))
                    medianNoStad = str("{:,}".format(result[2]))
                    medianWStad = str("{:,}".format(result[3]))

                    output = Markup("Current Home Value without a Stadium:   " + '<font color="limegreen">$' + actualNoStad + '</font>' + \
                    "<br><br>Current Home Value with a Stadium:   " + '<font color="limegreen">$' + actualWStad + '</font>' + \
                   "<br><br>Median Value of Homes in " + '<font color="yellow">' + County + '</font>' + " without a Stadium:   " + '<font color="limegreen">$' + medianNoStad + '</font>' + \
                   "<br><br>Median Value of Homes in " + '<font color="yellow">' + County + '</font>' + " with a Stadium:   " + '<font color="limegreen">$' + medianWStad + '</font>' + \
                   "<br><br><br><small>The predicted values have a PERCENT margin of error and were calculated using data from the 2017 U.S. Census</small>")

                    return render_template('glaps.html',
                    title='Home Value Predictor',
                    bytearray=datetime.now().year,
                    message=output)

                countyError = Markup("<font color = red><bold>Please enter a County<bold></font>")

    return render_template('glaps.html',
        title='Home Value Predictor',
        bytearray=datetime.now().year,
        message= 'Enter your location on the map and your current home value below:',
        countyError = countyError, valueError = valueError)

@app.route('/account')
def account():
    load_logged_in_user()
    return render_template('auth/account.html',
        title='Account',
        bytearray=datetime.now().year,
        message= 'Enter your information to display the value')

#View for the facets.html page
@app.route('/visualizations')
def visualizations():
    """Renders the visualizations page."""
    return render_template('visualizations.html')

#method that gets data from GLAPS API
def getAPI():

    myreqs = {"HomeVal":request.form['HomeVal'], "County":request.form['County']}
    url = requests.get("http://gmastorg.pythonanywhere.com/GLAPS", params=myreqs)
    responseJson = json.loads(url.text)

    return responseJson

def getState_CountiesList():

    States_Counties = []
    path = os.path.abspath("States_Counties.csv")
    with open(path) as file:
        inputFile = csv.reader(file)

        for row in inputFile:
             State_County = row[0]
             States_Counties.append(State_County)

    States_Counties.pop(0)
    return States_Counties

#Region Misc Pages
@app.errorhandler(500)
def server_not_found(e):
    # note that we set the 500 status explicitly
    return render_template('errors/500.html'), 500

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('errors/404.html'), 404
#End Region Misc Pages