"""
MongoDB helpers for Celso by @ecelis
"""

import os
from bson import ObjectId
from pymongo import MongoClient
import pymongoarrow.monkey
from pymongoarrow.api import Schema


mongo_uri = os.environ.get('MONGODB_URI', 'mongodb://localhost/') 
pymongoarrow.monkey.patch_all()
client = MongoClient(mongo_uri)
db = client[os.environ.get('MONGODB_DB', 'celso')]

collection = {
    'USER_ENCODINGS': 'UserEncodings'
}

def get_db():
    return db

def get_connection():
    """Reurn the MongoClient instance."""
    return client

def save_encodings(id, username, encodings):
    """"Persist to MongoDB a list representation of the face encodings."""
    user_encodings = db.get_collection(collection['USER_ENCODINGS'])
    # TODO Consider using bson instead
    # https://stackoverflow.com/questions/12272642/serialize-deserialize-float-arrays-to-binary-file-using-bson-in-python
    encodings_list = [encoding[0].tolist() for encoding in encodings]
    document = {
        'oId': id,
        'username': username,
        'encodings': encodings_list
    }
    result = user_encodings.insert_one(document)
    return result

def find_all():
    """Fetch all known samples encodings"""
    user_encodings = db.get_collection(collection['USER_ENCODINGS'])
    result = user_encodings.find()
    return result

def find_encodings_by_id(id):
    """Find encodings by ID"""
    user_encodings = db.get_collection(collection['USER_ENCODINGS'])
    result = user_encodings.find_one({'_id': ObjectId(id)})
    return result
