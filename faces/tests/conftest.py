# pylint: disable=redefined-outer-name
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
from base64 import b64encode
from pymongo import MongoClient
import pymongoarrow.monkey
import pytest
from faces import create_app
from faces.common.helpers import Collection, create_user_encodings


MONGO_DB = 'celso_test'
MONGO_URL = os.environ.get('MONGODB_URI', 'mongodb://localhost/')
META = 'data:image/jpeg;base64,'
OBAMA_NAME = 'Barack Obama'
AMLO_NAME = 'Andres M. Lopez O.'
ZELE_NAME = 'Volodymyr Zelenskyy'
with open('tests/obama1.jpg', 'rb') as OBAMA1:
    OBAMA1R = OBAMA1.read()
    B64OBAMA1 = META + b64encode(OBAMA1R).decode('ascii')
with open('tests/obama2.jpg', 'rb') as OBAMA2:
    OBAMA2R = OBAMA2.read()
    B64OBAMA2 = META + b64encode(OBAMA2R).decode('ascii')
with open('tests/obama3.jpg', 'rb') as OBAMA3:
    OBAMA3R = OBAMA3.read()
    B64OBAMA3 = META + b64encode(OBAMA3R).decode('ascii')
with open('tests/amlo.jpg', 'rb') as AMLO:
    AMLOR = AMLO.read()
    B64AMLO = META +  b64encode(AMLOR).decode('ascii')
with open('tests/zelensky.jpg', 'rb') as ZELENSKYY:
    ZELENSKYYR = ZELENSKYY.read()
    B64ZELENSKYY = META +  b64encode(ZELENSKYYR).decode('ascii')
with open('tests/people.jpg', 'rb') as PEOPLE:
    PEOPLER = PEOPLE.read()
    B64PEOPLE = META + b64encode(PEOPLER).decode('ascii')
with open('tests/none.jpg', 'rb') as NO_FACE:
    NO_FACER = NO_FACE.read()
    B64NO_FACE = META + b64encode(NO_FACER).decode('ascii')
OBAMA1.close()
OBAMA2.close()
OBAMA3.close()
AMLO.close()
PEOPLE.close()
NO_FACE.close()
mongo_uri = MONGO_URL + MONGO_DB + '?retryWrites=true&w=majority'
pymongoarrow.monkey.patch_all()
mongo_client = MongoClient(mongo_uri)
db = mongo_client[MONGO_DB]

db.drop_collection(Collection.USER_ENCODINGS.value)
create_user_encodings(db)

@pytest.fixture()
def app():
    """Flask app fixture"""
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    # Other setup
    yield app
    # Clean up

@pytest.fixture()
def client(app):
    """Flask test app client"""
    return app.test_client()

@pytest.fixture()
def runner(app):
    """Flask test app runner"""
    return app.test_cli_runner()
