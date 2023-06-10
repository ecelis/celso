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

import pytest
import numpy as np
from tests.conftest import (db,
    OBAMA_NAME,
    ZELE_NAME,
    OBAMA1,
    B64OBAMA1,
    B64OBAMA2,
    B64OBAMA3,
    B64AMLO,
    B64ZELENSKYY,
    B64PEOPLE,
    B64NO_FACE)
from faces.common.strings import FacesError
from faces.db.user_encodings import UserEncodings
from faces.detect import Detect


class TestDetect:
    """Tests for detect module"""
    def test_to_cv_image(self):
        """Test to_cv_image succesfully"""
        detect = Detect(db)
        cv_image = detect.to_cv_image(B64AMLO)
        assert isinstance(cv_image, np.ndarray) is True

    def test_to_cv_image_attribute_error(self):
        """Test to_cv_image AttributeError raw image as parameter"""
        detect = Detect(db)
        cv_image = detect.to_cv_image(OBAMA1)
        assert cv_image is None

    def test_get_encodings(self):
        """Test get_encodings succesfully"""
        detect = Detect(db)
        cv_image = detect.to_cv_image(B64AMLO)
        result = detect.get_encodings(cv_image)
        assert isinstance(result, list) is True
        assert len(result) > 0

    def test_get_encodings_type_error(self):
        """Test get_encodings TypeError raw image passed as parameter"""
        detect = Detect(db)
        result = detect.get_encodings(OBAMA1)
        assert result is None

    def test_get_encodings_more_than_one(self):
        """Test get_encodings more thano one persone in picture"""
        detect = Detect(db)
        cv_image = detect.to_cv_image(B64PEOPLE)
        result = detect.get_encodings(cv_image)
        assert result == FacesError.GT_ONE_FACE.value

    @pytest.mark.xfail(reason="hog model fails to detect no-face")
    def test_get_encodings_no_faces(self):
        """Test get_encodings no faces"""
        detect = Detect(db)
        cv_image = detect.to_cv_image(B64NO_FACE)
        result = detect.get_encodings(cv_image)
        assert result == FacesError.LT_ONE_FACE.value

    def test_match_encodings(self):
        """Test match_encodings sucesfully"""
        user_encodings = UserEncodings(db)
        detect = Detect(db)
        known_cv_image = detect.to_cv_image(B64OBAMA1)
        known_encodings = detect.get_encodings(known_cv_image)
        user_encodings.save_encodings(OBAMA_NAME,
                                               [known_encodings])
        cv_image = detect.to_cv_image(B64OBAMA2)
        encodings = detect.get_encodings(cv_image)
        result = detect.match_encodings(encodings)
        print(result)
        assert isinstance(result, dict)
        assert result['success'] is True

    def test_match_encodings_unknown(self):
        """Test match_encodings no match"""
        detect = Detect(db)
        cv_image = detect.to_cv_image(B64AMLO)
        encodings = detect.get_encodings(cv_image)
        result = detect.match_encodings(encodings)
        assert isinstance(result, dict)
        assert result['success'] is False
        assert result['error'] == FacesError.NO_MATCH.value

    def test_encode(self):
        """Test encode faces"""
        detect = Detect(db)
        result = detect.encode([B64ZELENSKYY],
                               ZELE_NAME)
        assert isinstance(result, dict) is True
        assert result['success'] is True
        assert result['data'].acknowledged is True

    def test_encode_dupe(self):
        """Test encode duplicated faces"""
        detect = Detect(db)
        result = detect.encode([B64OBAMA3, B64OBAMA2, B64OBAMA1],
                               'Evil Twin')
        assert isinstance(result, ValueError) is True
        assert result.args[0] == FacesError.DUPLICATE.value

    def test_match(self):
        """Test match successfully"""
        detect = Detect(db)
        result = detect.match(B64ZELENSKYY)
        assert isinstance(result, dict) is True
        assert result['success'] is True
        assert result['username'] == ZELE_NAME

    def test_match_no_match(self):
        """Test no match"""
        detect = Detect(db)
        result = detect.match(B64AMLO)
        assert isinstance(result, dict) is True
        assert result['success'] is False
        assert result['error'] == FacesError.NO_MATCH.value
