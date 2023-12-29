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
app.config['SECRET_KEY'] = os.getenv("TOKEN_KEY") # Clé secrète pour la création de JWT

username = "tsapi"
"""
token = jwt.encode({'username': username}, app.config['SECRET_KEY'], algorithm='HS256')
print(token)
jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
"""

from security import hash_password, verify_user_validity



