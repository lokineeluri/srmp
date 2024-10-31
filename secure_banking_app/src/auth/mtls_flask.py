from flask import Flask, request, jsonify
from .jwt_handler import verify_jwt
from ..db import users_collection
import os




app = Flask(__name__)

@app.route('/profile', methods=['GET'])
def profile():
    # Extract and validate JWT and API key
    auth_header = request.headers.get('Authorization')
    api_key = request.headers.get('X-API-Key')

    if not auth_header or not api_key:
        return jsonify({"error": "Unauthorized access"}), 403

    token = auth_header.split(" ")[1]
    user_id = verify_jwt(token)
    if user_id == "Token has expired" or user_id == "Invalid token":
        return jsonify({"error": user_id}), 403

    # Verify API key with stored value
    user = users_collection.find_one({"username": user_id, "api_key": api_key})
    if not user:
        return jsonify({"error": "Invalid API key"}), 403

    # Return profile data
    profile_data = {
        "name": user.get("name", user_id),
        "balance": user.get("balance", 0.0)
    }
    return jsonify(profile_data), 200

@app.route('/profile/balance', methods=['PUT'])
def update_balance():
    # Extract and validate JWT and API key
    auth_header = request.headers.get('Authorization')
    api_key = request.headers.get('X-API-Key')
    data = request.json

    if not auth_header or not api_key or 'balance' not in data:
        return jsonify({"error": "Unauthorized access or invalid data"}), 403

    token = auth_header.split(" ")[1]
    user_id = verify_jwt(token)
    if user_id == "Token has expired" or user_id == "Invalid token":
        return jsonify({"error": user_id}), 403

    # Verify API key with stored value
    user = users_collection.find_one({"username": user_id, "api_key": api_key})
    if not user:
        return jsonify({"error": "Invalid API key"}), 403

    # Update the balance in MongoDB
    new_balance = data["balance"]
    users_collection.update_one({"username": user_id}, {"$set": {"balance": new_balance}})
    return jsonify({"message": "Balance updated successfully"}), 200

def run_app():
    
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    CERT_DIR = os.path.join(BASE_DIR, 'src', 'certificates')
    context = (
        os.path.join(CERT_DIR, 'server.pem'),
        os.path.join(CERT_DIR, 'server.key')
    )
    
    print("Certificate paths:", context)  # Debug print
    app.run(ssl_context=context, port=5000)
    print("Certificate paths:", context)  # Should print the full paths to your cert files

    
if __name__ == "__main__":
    run_app()
    
    
