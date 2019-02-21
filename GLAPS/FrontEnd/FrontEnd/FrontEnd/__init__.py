"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)

from . import db #seems to be working
db.init_app(app)

from . import auth
app.register_blueprint(auth.bp)

import FrontEnd.views