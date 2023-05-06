import os
from pymongo import MongoClient
import pymongoarrow.monkey
from pymongoarrow.api import Schema


mongo_uri = os.environ.get('MONGODB_URI', 'mongodb://localhost/') 
pymongoarrow.monkey.patch_all()
client = MongoClient(mongo_uri)
db = client[os.environ.get('MONGODB_DB', 'celso')]

def get_db():
    return db

def get_connection():
    """Reurn the MongoClient instance."""
    return client

def close_connection(client):
    """"Set to None the MongoClient instance."""
    client = None

def save_encodings(id, encodings):
    """"Persist to MongoDB a list representation of the face encodings."""
    user_encodings = db.get_collection('UserEncodings')
    # TODO Consider using bson instead
    # https://stackoverflow.com/questions/12272642/serialize-deserialize-float-arrays-to-binary-file-using-bson-in-python
    encodings_list = [encoding[0].tolist() for encoding in encodings]
    document = {
        'oId': id,
        'encodings': encodings_list
    }
    result = user_encodings.insert_one(document)
    return result


