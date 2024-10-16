# src/auth/create_users.py
from db import users_collection   # Change this to an absolute import
import bcrypt
import pyotp

def create_initial_users():
    users = [
        {"username": "user1", "password": "password1", "name": "John Doe", "balance": 1000.00},
        {"username": "user2", "password": "password2", "name": "Jane Smith", "balance": 1500.50},
        {"username": "user3", "password": "password3", "name": "Emily Johnson", "balance": 2000.75},
    ]

    for user in users:
        hashed_password = bcrypt.hashpw(user["password"].encode('utf-8'), bcrypt.gensalt())
        totp_secret = pyotp.random_base32()
        users_collection.insert_one({
            "username": user["username"],
            "password": hashed_password,
            "name": user["name"],
            "balance": user["balance"],
            "totp_secret": totp_secret
        })
    print("Users created successfully.")

if __name__ == "__main__":
    create_initial_users()
