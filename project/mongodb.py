from os import getenv
import pymongo


DB_NAME = 'spotify-1m'

connection_string = f"mongodb+srv://{getenv('MONGODB_USERNAME')}:{getenv('MONGODB_PASSWORD')}@cluster0.rajwn.mongodb.net/{DB_NAME}?retryWrites=true&w=majority"

client = pymongo.MongoClient(connection_string)

db = client[DB_NAME]

tracks_features = db.tracks_features
