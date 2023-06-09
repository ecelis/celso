"""
UserEncodings DAO for Celso by @ecelis

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

from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from faces.common.helpers import Collection
from faces.common.strings import FacesError

class UserEncodings:
    """UserENcodings collection DAO"""
    def __init__(self, _db) -> None:
        self._db = _db

    def save_encodings(self, username: str, encodings: list):
        """"Persist to MongoDB a list representation of the face encodings."""
        error = None
        try:
            if isinstance(encodings, list) is False:
                raise AttributeError(FacesError.VALUE_ERROR.value)
            user_encodings = self._db.get_collection(Collection.USER_ENCODINGS.value)
            # TODO Consider using bson instead
            # https://stackoverflow.com/questions/12272642/serialize-deserialize-float-arrays-to-binary-file-using-bson-in-python
            encodings_list = [encoding[0].tolist() for encoding in encodings]
            document = {
                'username': username,
                'encodings': encodings_list
            }
            result = user_encodings.insert_one(document)
            return result
        except (DuplicateKeyError, AttributeError) as ex:
            error = ex
        return error

    def find_all(self):
        """Fetch all known samples encodings"""
        user_encodings = self._db.get_collection(Collection.USER_ENCODINGS.value)
        result = user_encodings.find()
        return result

    def find_encodings_by_id(self, _id: str):
        """Find encodings by ID"""
        user_encodings = self._db.get_collection(Collection.USER_ENCODINGS.value)
        result = user_encodings.find_one({'_id': ObjectId(_id)})
        return result
