"""
Face detection for Celso by @ecelis.

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

from base64 import b64decode
from io import BytesIO
from PIL import Image
import cv2
import numpy as np
from face_recognition import face_encodings, face_locations, compare_faces, face_distance
from faces.db.user_encodings import UserEncodings
from faces.common.strings import FacesError

class Detect:
    """Face detection library for Celso"""
    def __init__(self, _db):
        super().__init__()

        self._db = _db
        self.locations = 0

    def get_encodings(self, image: np.ndarray):
        """Get faces from one image and return it encoded."""
        error = None
        try:
            locations = face_locations(image,
                number_of_times_to_upsample=1,
                model='hog')
            print(locations)
            locations_len = len(locations)
            if locations_len > 1:
                raise ValueError(FacesError.GT_ONE_FACE.value)
            if locations_len < 1:
                raise ValueError(FacesError.LT_ONE_FACE.value)
            encodings = face_encodings(image, locations)
            return encodings
        except (TypeError, ValueError) as error:
            if isinstance(error, ValueError):
                return error.args[0]
            return None

    def to_cv_image(self, picture: str):
        """Transform Base64 encoded image to CV2 RGB image"""
        try:
            image_data = b64decode(str(picture.split(',')[1]))
            image = Image.open(BytesIO(image_data))
            cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)
            return cv_image
        except AttributeError:
            return None

    def match_encodings(self, candidate: np.ndarray):
        """
        Pass a candidate image encoding and match against known
        encodings in DB
        """
        error = FacesError.NO_MATCH.value
        user_encodings = UserEncodings(self._db)
        known = list(user_encodings.find_all())
        if candidate:
            for face in known:
                _id = str(face['_id'])
                username = str(face['username'])
                sample_encodings = [np.array(x) for x in face['encodings']]
                matches = compare_faces(sample_encodings, candidate[0])
                distances = face_distance(sample_encodings, candidate[0])
                best_match = np.argmin(distances)
                if matches[best_match]:
                    return {'_id': _id, 'username': username, 'success': True}
        return {'error': error, 'success': False}

    def encode(self, pictures: list[str], username: str):
        """
        Encode Base64 pictures to numpy array and save associated with
        username.
        """
        error = None
        try:
            encodings = []
            for picture in pictures:
                image_encodings = self.get_encodings(
                    self.to_cv_image(picture))
                duplicate = self.match_encodings(image_encodings)
                if duplicate['success']:
                    raise ValueError(FacesError.DUPLICATE.value)
                encodings.append(image_encodings)
            user_encodings = UserEncodings(self._db)
            result = user_encodings.save_encodings(username, encodings)
            return {'data': result, 'success': True}
        except (ValueError) as ex:
            error = ex
        return error

    def match(self, picture: str, video: str = None):
        """
        Match face with known encodings from data base.
        
        video param is reserved for future use"""
        error = None
        try:
            image_encodings = self.get_encodings(self.to_cv_image(picture))
            result = self.match_encodings(image_encodings)
            return result
        except ValueError as ex:
            error = ex
        return error
            