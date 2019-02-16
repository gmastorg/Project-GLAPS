import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext

sqlite_file = 'users.db' #Needs to be changed to a data base not just a schema place holder
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

conn.commit()
conn.close()

def init_app(app):
	"""Register database functions with the Flask app. This is called by
	the application factory.
	"""
	app.teardown_appcontext(close_db)
	app.cli.add_command(init_db_command)