from pymongo import MongoClient


client = MongoClient('localhost', 27017)
db = client['mongo_movies']

if 'concessions' not in db.list_collection_names():
    concessions_data = [
     {
       "ItemID": 1,
       "ItemName": "Popcorn",
       "Cost": 5
     },
     {
       "ItemID": 2,
       "ItemName": "Drink",
       "Cost": 3
     },
     {
       "ItemID": 3,
       "ItemName": "Pretzel",
       "Cost": 4
     },
     {
       "ItemID": 4,
       "ItemName": "Nachos",
       "Cost": 6
     },
     {
       "ItemID": 5,
       "ItemName": "Candy",
       "Cost": 2
     }
    ]
    concessions_collection = db['concessions']
    concessions_collection.insert_many(concessions_data)

if 'movies' not in db.list_collection_names():

    movies_data = [
     {
       "movieID": 1,
       "Name": "The Avengers",
       "end_date": "4/30/24",
       "ACost": 8,
       "KCost": 6,
       "rating": "PG13"
     },
     {
       "movieID": 2,
       "Name": "Avatar",
       "end_date": "4/25/24",
       "ACost": 8,
       "KCost": 6,
       "rating": "PG"
     },
     {
       "movieID": 3,
       "Name": "Harry Potter and the Sorcerers Stone",
       "end_date": "4/30/24",
       "ACost": 8,
       "KCost": 6,
       "rating": "PG"
     },
     {
       "movieID": 4,
       "Name": "The Conjuring",
       "end_date": "4/27/24",
       "ACost": 8,
       "KCost": 6,
       "rating": "R"
     },
     {
       "movieID": 5,
       "Name": "The Notebook",
       "end_date": "4/29/24",
       "ACost": 8,
       "KCost": 6,
       "rating": "PG13"
     }
    ]
    movies_collection = db['movies']
    movies_collection.insert_many(movies_data)

if 'showings' not in db.list_collection_names():
    showings_data = [
     {
       "theatreID": 1,
       "movieID": 1,
       "time": "15:00:00"
     },
     {
       "theatreID": 1,
       "movieID": 1,
       "time": "18:00:00"
     },
     {
       "theatreID": 1,
       "movieID": 1,
       "time": "21:00:00"
     },
     {
       "theatreID": 2,
       "movieID": 2,
       "time": "16:00:00"
     },
     {
       "theatreID": 2,
       "movieID": 2,
       "time": "17:00:00"
     },
     {
       "theatreID": 2,
       "movieID": 2,
       "time": "20:00:00"
     },
     {
       "theatreID": 3,
       "movieID": 3,
       "time": "17:00:00"
     },
     {
       "theatreID": 3,
       "movieID": 3,
       "time": "20:00:00"
     },
     {
       "theatreID": 3,
       "movieID": 3,
       "time": "23:00:00"
     },
     {
       "theatreID": 4,
       "movieID": 4,
       "time": "18:00:00"
     },
     {
       "theatreID": 4,
       "movieID": 4,
       "time": "21:00:00"
     },
     {
       "theatreID": 4,
       "movieID": 4,
       "time": "23:00:00"
     },
     {
       "theatreID": 5,
       "movieID": 5,
       "time": "15:00:00"
     },
     {
       "theatreID": 5,
       "movieID": 5,
       "time": "18:00:00"
     },
     {
       "theatreID": 5,
       "movieID": 5,
       "time": "21:00:00"
     }
    ]
    showings_collection = db['movies']
# showings_collection.insert_many(showings_data)
print(showings_collection.find_one())
client.close()
'''

client = MongoClient('localhost', 27017)

# Access the database
db = client['mongo_movies']

# Drop all collections in the database
db.drop_collection('concessions')
db.drop_collection('movies')
db.drop_collection('showings')

# Close the connection
client.close()

'''
