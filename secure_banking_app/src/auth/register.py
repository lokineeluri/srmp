import bcrypt
import pyotp
from ..db import users_collection  # MongoDB collection

def register_user(username, password):
    # Check if username exists
    existing_user = users_collection.find_one({"username": username})
    if existing_user:
        return "User already exists!"
    
    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    # Generate a random TOTP secret for MFA
    totp_secret = pyotp.random_base32()

    # Store user in MongoDB
    user_data = {
        "username": username,
        "password": hashed_password,
        "totp_secret": totp_secret,  # Used for MFA
        "api_key": None,  # Will be generated upon login
        "jwt": None  # Will be generated upon login
    }
    users_collection.insert_one(user_data)
    return "User registered successfully!"
