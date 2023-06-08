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


user_1 = 'anne'
user_2 = 'joe'
mock = [
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
                               buffer=np.array(mock),
                               dtype=float)
        user_encodings = UserEncodings(db)
        result = user_encodings.save_encodings(user_1, encodings)
        assert result.acknowledged is True

    def test_save_encodings_dupe_user1(self):
        """Test save_encodings duplicated username"""
        encodings = np.ndarray(shape=(2,2),
                               buffer=np.array(mock),
                               dtype=float)
        user_encodings = UserEncodings(db)
        result = user_encodings.save_encodings(user_1, encodings)
        assert result is None

    def test_save_encodings_invalid_nparray(self):
        """Test save_encodings invalid nparray data"""
        user_encodings = UserEncodings(db)
        result = user_encodings.save_encodings(user_1, mock)
        assert result is None
