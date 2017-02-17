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
app.config['MONGOALCHEMY_CONNECTION_STRING'] = os.getenv('MONGOALCHEMY_CONNECTION_STRING','')
app.config['MONGOALCHEMY_SERVER'] = os.getenv('MONGOALCHEMY_SERVER','')
app.config['MONGOALCHEMY_PORT'] = os.getenv('MONGOALCHEMY_PORT',0)
app.config['MONGOALCHEMY_DATABASE'] = os.getenv('MONGOALCHEMY_DATABASE','')

persist_db = MongoAlchemy(app)
