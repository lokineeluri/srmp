from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')  # Update this string as necessary
db = client['auth_db']  # Your database name
users_collection = db['users']  # Your collection name for users
