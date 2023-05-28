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
from faces.common.helpers import find_all, save_encodings

class Detect():
    """Face detection library for Celso"""
    def __init__(self):
        super().__init__()
        self.locations = 0

    def get_encodings(self, image):
        """Get faces from one image and return it encoded."""
        locations = face_locations(image)
        locations_len = len(locations)
        if locations_len > 1:
            raise ValueError('More than one face detected.')
        if locations_len < 1:
            raise ValueError("Couldn't detect any face.")
        encodings = face_encodings(image, locations)
        return encodings

    def to_cv_image(self, picture):
        """Trnasform Base64 encoded image to CV2 RGB image"""
        image_data = b64decode(str(picture.split(',')[1]))
        image = Image.open(BytesIO(image_data))
        cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)
        return cv_image

    def match_encodings(self, candidate):
        """Pass a candidate image encoding and match against known in encodings in DB"""
        error = 'Not known.'
        known = list(find_all())
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
                error = 'No matches.'
        return {'error': error, 'success': False}

    def encode(self, pictures, username):
        """Encode Base64 pictures to numpy array and save associated with username."""
        error = None
        encodings = []
        for picture in pictures:
            try:
                image_encodings = self.get_encodings(self.to_cv_image(picture))
                duplicate = self.match_encodings(image_encodings)
                if duplicate['success']:
                    duplicate['success'] = False
                    return duplicate
                encodings.append(image_encodings)
            except ValueError as ex:
                error = ex
        try:
            result = save_encodings(username, encodings)
            return {'data': result, 'success': True}
        except Exception as ex:
            error = ex
        return { 'error': error }

    def match(self, picture):
        """Match face with known encodings from data base."""
        error = None
        try:
            image_encodings = self.get_encodings(self.to_cv_image(picture))
            result = self.match_encodings(image_encodings)
            return result
        except ValueError as error:
            print(error)
            return {'error': error}
            