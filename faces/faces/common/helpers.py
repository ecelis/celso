"""
MongoDB helpers for Celso by @ecelis

   Copyright 2023 Ernesto A. Celis de la Fuente

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

import os
from bson import ObjectId
from pymongo import MongoClient
import pymongoarrow.monkey

MONGO_URL = os.environ.get('MONGODB_URI', 'mongodb://localhost/')
MONGO_DB = os.environ.get('MONGODB_DB', 'celso')
mongo_uri = MONGO_URL + MONGO_DB + '?retryWrites=true&w=majority'
pymongoarrow.monkey.patch_all()
client = MongoClient(mongo_uri)
db = client[MONGO_DB]

collection = {
    'USER_ENCODINGS': 'UserEncodings'
}

def get_db():
    """Return db instance."""
    return db

def get_connection():
    """Reurn the MongoClient instance."""
    return client

def get_mongo_uri():
    return mongo_uri

def save_encodings(username, encodings):
    """"Persist to MongoDB a list representation of the face encodings."""
    user_encodings = db.get_collection(collection['USER_ENCODINGS'])
    # TODO Consider using bson instead
    # https://stackoverflow.com/questions/12272642/serialize-deserialize-float-arrays-to-binary-file-using-bson-in-python
    encodings_list = [encoding[0].tolist() for encoding in encodings]
    document = {
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

def find_encodings_by_id(_id):
    """Find encodings by ID"""
    user_encodings = db.get_collection(collection['USER_ENCODINGS'])
    result = user_encodings.find_one({'_id': ObjectId(_id)})
    return result
