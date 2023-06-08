"""
Test UserEncodings collection for Celso by @ecelis

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

import numpy as np
from faces.db.user_encodings import UserEncodings
from tests.conftest import db
from faces.common.helpers import create_user_encodings


USER_1 = 'Ann'
USER_2 = 'Bob'
USER_3 = 'Charly'
MOCK = [
        [ 0.044832512736320496, 0.13082386553287506, 0.11568633466959],
        [0.027178555727005005, -0.0730728879570961, -0.01901322603225708]
        ]

class TestUserEncodings:
    """Test User Encodings functions"""

    def test_create_user_encodings(self):
        """Test create_user_encodings(db)"""
        create_user_encodings(db)

    def test_save_encodings(self):
        """Test save_encodings success"""
        encodings = np.ndarray(shape=(2,2),
                               buffer=np.array(MOCK),
                               dtype=float)
        user_encodings = UserEncodings(db)
        result = user_encodings.save_encodings(USER_1, encodings)
        assert result.acknowledged is True

    def test_save_encodings_dupe_user1(self):
        """Test save_encodings duplicated username"""
        encodings = np.ndarray(shape=(2,2),
                               buffer=np.array(MOCK),
                               dtype=float)
        user_encodings = UserEncodings(db)
        result = user_encodings.save_encodings(USER_1, encodings)
        assert result is None

    def test_save_encodings_invalid_nparray(self):
        """Test save_encodings invalid nparray data"""
        user_encodings = UserEncodings(db)
        result = user_encodings.save_encodings(USER_1, MOCK)
        assert result is None

    def test_find_all(self):
        """Test find all encodings"""
        user_encodings = UserEncodings(db)
        result = user_encodings.find_all()
        assert result is not None
        assert len(list(result)) == 1
    
    def test_find_encodings_by_id(self):
        """Test find encodings by id"""
        user_encodings = UserEncodings(db)
        encodings = np.ndarray(shape=(2,2),
                               buffer=np.array(MOCK),
                               dtype=float)
        user = user_encodings.save_encodings(USER_2, encodings)
        result = user_encodings.find_encodings_by_id(user.inserted_id)
        assert USER_2 == result['username']
