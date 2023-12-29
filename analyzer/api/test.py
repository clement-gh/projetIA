import jwt
#pip install pyjwt
from flask import Flask, request, jsonify
#pip install python-dotenv
import hashlib
import sys
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
from flask_cors import CORS

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
cors = CORS(app, resources={r"/*": {"origins": "*"}})
load_dotenv()

user

app.config['SECRET_KEY'] = os.getenv("SECRET_KEY_TOKEN")

token= jwt.encode