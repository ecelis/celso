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
from pymongo import MongoClient
import pymongoarrow.monkey
from faces.common.helpers import create_user_encodings, get_mongo_uri

mongo_uri = get_mongo_uri()
pymongoarrow.monkey.patch_all()
client = MongoClient(mongo_uri)
db = client[os.environ.get('MONGODB_DB', 'celso')]

create_user_encodings(db)
