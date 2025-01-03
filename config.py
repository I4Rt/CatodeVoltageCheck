from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
from time import strftime, localtime, time
from model.static.ConnectionHolder import ConnectionHolder
# from model.static.RuntimeStatuser import *


from flask import Flask, request, json
from flask_cors import CORS, cross_origin

SERIAL_NAME = 'COM13'


Base = declarative_base()
e = create_engine("postgresql://postgres:qwerty@localhost:5432/vault_gate_events", echo=False)

app = Flask(__name__, template_folder='resources/templates',  static_folder='resources/static', static_url_path = '')
cors = CORS(app, supports_credentials=True, resources={r"*": {"origins": "*"}})

# runtimeStatuser = RuntimeStatuser.getInstance()



