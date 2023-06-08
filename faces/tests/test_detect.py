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

from base64 import b64encode
import numpy as np
from faces.common.strings import FacesError
from faces.detect import Detect
from tests.conftest import db


meta = 'data:image/jpeg;base64,'
obama1 = open('tests/obama1.jpg', 'rb')
obama1r = obama1.read()
b64obama = meta + b64encode(obama1r).decode('ascii')
obama2 = open('tests/obama2.jpg', 'rb')
obama2r = obama2.read()
b64obama2 = meta + b64encode(obama2r).decode('ascii')
amlo = open('tests/amlo.jpg', 'rb')
amlor = amlo.read()
b64amlo = b64encode(amlor).decode('ascii')
b64obama1 = meta + b64amlo
people = open('tests/people.jpg', 'rb')
peopler = people.read()
b64people = meta + b64encode(peopler).decode('ascii')
obama1.close()
obama2.close()
amlo.close()
people.close()
class TestDetect:
    """Tests for detect module"""
    def test_to_cv_image(self):
        """Test to_cv_image succesfully"""
        detect = Detect()
        cv_image = detect.to_cv_image(b64obama1)
        assert isinstance(cv_image, np.ndarray) is True

    def test_to_cv_image_attribute_error(self):
        """Test to_cv_image AttributeError raw image as parameter"""
        detect = Detect()
        cv_image = detect.to_cv_image(obama1)
        assert cv_image is None

    def test_get_encodings(self):
        """Test get_encodings succesfully"""
        detect = Detect()
        cv_image = detect.to_cv_image(b64obama1)
        result = detect.get_encodings(cv_image)
        assert isinstance(result, list) is True
        assert len(result) > 0

    def test_get_encodings_type_error(self):
        """Test get_encodings TypeError raw image passed as parameter"""
        detect = Detect()
        result = detect.get_encodings(obama1)
        assert result is None

    def test_get_encodings_more_than_one(self):
        """Test get_encodings more thano one persone in picture"""
        detect = Detect()
        cv_image = detect.to_cv_image(b64people)
        result = detect.get_encodings(cv_image)
        assert result == FacesError.GT_ONE_FACE.value

    # def test_encode(self):
    #     """Test encode succesfully"""
    #     detect = Detect()
    #     pictures = [b64obama1, b64obama2]
    #     result = detect.encode(pictures, 'Obama')
    #     print(result)
    #     assert isinstance(result['error'], str)
