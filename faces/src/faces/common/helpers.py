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
from enum import Enum
from pymongo import MongoClient, ASCENDING
import pymongoarrow.monkey


MONGO_URL = os.environ.get('MONGODB_URI', 'mongodb://localhost/')
MONGO_DB = os.environ.get('MONGODB_DB', 'celso')
mongo_uri = MONGO_URL + MONGO_DB + '?retryWrites=true&w=majority'
pymongoarrow.monkey.patch_all()
client = MongoClient(mongo_uri)
db = client[MONGO_DB]

class Collection(Enum):
    """MongoDB Collections for celso"""
    USER_ENCODINGS = 'UserEncodings'

def get_db():
    """Return db instance."""
    return db

def get_connection():
    """Reurn the MongoClient instance."""
    return client

def get_mongo_uri():
    """Return MongoDB URI"""
    return mongo_uri

def create_user_encodings(_db):
    """Create UserEncoding collection"""
    _db.create_collection('UserEncodings')
    user_encodings = _db.get_collection(Collection.USER_ENCODINGS.value)
    user_encodings.create_index([('username', ASCENDING)], unique=True)
