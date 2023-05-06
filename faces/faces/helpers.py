import os
from pymongo import MongoClient
import pyarrow
import bson
import pymongoarrow.monkey
from pymongoarrow.api import Schema


mongo_uri = os.environ.get('MONGODB_URI', 'mongodb://localhost/') 
pymongoarrow.monkey.patch_all()
client = MongoClient(mongo_uri)
db = client[os.environ.get('MONGODB_DB', 'celso')]

def get_db():
    return db

def get_connection():
    return client

def close_connection(client):
    client = None

def save_encodings(encodings):
    user_encodings = db.get_collection('UserEncodings')
    user_encodings.insert_many(encodings)
