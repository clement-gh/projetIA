import hashlib
import os

def hash_password(user,password):
    return hashlib.sha256((user+password).encode()).hexdigest()

def verify_user_validity(user,password):
    hash_password_user = hash_password(user,password)

    pwd=os.getenv("HASHED_USER")
    return  (hash_password_user == pwd )