"""
Routes and views for the flask application.
"""

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

@app.route('/login')
def login():
    """Renders the login page."""
    return render_template(
        'login.html',
        title='Login',
        year=datetime.now().year,
        message='Please login to continue'
    )

@app.route('/register')
def register():
    """Renders the register page."""
    return render_template(
        'register.html',
        title='Register',
        year=datetime.now().year,
        message='Please register to take full advantage of GLAPS'
    )

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