
from ..db import users_collection  # Ensure this import is present
import pyotp
import bcrypt
import jwt
import datetime
from .jwt_handler import create_jwt
SECRET_KEY = "your-secret-key"
def login_user(username, password):
    # Fetch the user from MongoDB
    user = users_collection.find_one({"username": username})
    if not user:
        return "Invalid username or password"
    
    # Verify the password
    if not bcrypt.checkpw(password.encode('utf-8'), user['password']):
        return "Invalid username or password"
    # Generate OTP for MFA
    totp = pyotp.TOTP(user['totp_secret'])
    otp = totp.now()  # Generate OTP
    print(f"Your OTP is: {otp}")  # Display OTP in the terminal

    return "OTP generated, please enter it."

def verify_otp(username, user_otp):
    # Fetch the user from MongoDB
    user = users_collection.find_one({"username": username})
    if not user:
        return "Invalid OTP"

    # Verify the OTP
    totp = pyotp.TOTP(user['totp_secret'])
    if not totp.verify(user_otp, valid_window=1):  # Allow a 60-second window
        return "Invalid OTP"
    # Generate API key and JWT after successful MFA
    api_key = pyotp.random_base32()  # Generate a random API key
    jwt_token = create_jwt(username)
    # Store the JWT and API key in MongoDB
    users_collection.update_one(
        {"username": username},
        {"$set": {"api_key": api_key, "jwt": jwt_token}}
    )
    
    return f"Login successful! API Key: {api_key}, JWT: {jwt_token}"
