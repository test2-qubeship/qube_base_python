#/usr/bin/python
"""
Add docstring here
"""

from flask import Flask
from flask_mongoalchemy import MongoAlchemy
import os
from flask_cors import CORS



app = Flask(__name__)
CORS(app)
app.config['MONGOALCHEMY_CONNECTION_STRING'] = os.environ['MONGOALCHEMY_CONNECTION_STRING']
app.config['MONGOALCHEMY_SERVER'] = os.environ['MONGOALCHEMY_SERVER']
app.config['MONGOALCHEMY_PORT'] = os.environ['MONGOALCHEMY_PORT']
app.config['MONGOALCHEMY_DATABASE'] = os.environ['MONGOALCHEMY_DATABASE']

persist_db = MongoAlchemy(app)
