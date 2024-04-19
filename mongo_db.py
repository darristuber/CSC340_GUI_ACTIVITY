from pymongo import MongoClient
import json

# Connect to MongoDB
client = MongoClient('localhost', 27017)  # Assuming MongoDB is running on localhost on default port 27017
db = client['mongo_movies']  # Replace 'your_database_name' with your actual database name

# Read data from file
with open('nosql_tables.json') as f:
    data = json.load(f)

# Insert data into collections
for collection_name, collection_data in data.items():
    collection = db[collection_name]
    collection.insert_many(collection_data)

# Close connection
client.close()