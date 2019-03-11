"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)

app.config.from_mapping(SECRET_KEY='dev',
        DATABASE='glapsdb.sqlite')
from FrontEnd import db #seems to be working
db.init_app(app)

import FrontEnd.views