"""
MongoDB setup utility for Celso by @ecelis
"""

import os
from pymongo import MongoClient, ASCENDING
import pymongoarrow.monkey


mongo_uri = os.environ.get('MONGODB_URI', 'mongodb://localhost/')
pymongoarrow.monkey.patch_all()
client = MongoClient(mongo_uri)
db = client[os.environ.get('MONGODB_DB', 'celso')]

db.create_collection('UserEncodings')
user_encodings = db.get_collection('UserEncodings')
user_encodings.create_index([('oId', ASCENDING)], unique=True)
