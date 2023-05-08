"""
MongoDB setup utility for Celso by @ecelis

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
from pymongo import MongoClient, ASCENDING
import pymongoarrow.monkey

MONGO_URL = os.environ.get('MONGODB_URI', 'mongodb://localhost/')
MONGO_DB = os.environ.get('MONGODB_DB', 'celso')
mongo_uri = MONGO_URL + MONGO_DB + '?retryWrites=true&w=majority'
pymongoarrow.monkey.patch_all()
client = MongoClient(mongo_uri)
db = client[os.environ.get('MONGODB_DB', 'celso')]

db.create_collection('UserEncodings')
user_encodings = db.get_collection('UserEncodings')
user_encodings.create_index([('oId', ASCENDING)], unique=True)
