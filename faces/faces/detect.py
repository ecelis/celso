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

import os
import glob
from base64 import b64decode
from io import BytesIO
from PIL import Image
import cv2
import numpy as np
from face_recognition import face_encodings, face_locations, compare_faces, face_distance
from faces.helpers import find_all, save_encodings

samples = os.environ['CELSO_SAMPLES']
unknown = os.environ['CELSO_UNKNOWN']

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

    def encode(self, pictures, username):
        """Read images from file system and encode them all."""
        error = None
        encodings = []
        for picture in pictures:
            image_data = b64decode(str(picture.split(',')[1]))
            image = Image.open(BytesIO(image_data))
            cv_gray_image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)
            try:
                image_encodings = self.get_encodings(cv_gray_image)
                encodings.append(image_encodings)
            except ValueError as error:
                return { 'error': error }
        try:
            result = save_encodings(username, encodings)
            return result
        except Exception as error:
            return { 'error': error }

    def match(self, picture):
        """Match face with known encodings from data base."""
        error = None
        image_encodings = None
        _id = None
        matches = None
        encodings = list(find_all())
        image_data = b64decode(str(picture.split(',')[1]))
        image = Image.open(BytesIO(image_data))
        cv_gray_image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)
        try:
            image_encodings = self.get_encodings(cv_gray_image)
        except ValueError as error:
            print(error)
            return {'error': error}
        if image_encodings:
            for face in encodings:
                _id = str(face['_id'])
                username = str(face['username'])
                sample_encodings = [np.array(x) for x in face['encodings']]
                matches = compare_faces(sample_encodings, image_encodings[0])
                distances = face_distance(sample_encodings, image_encodings[0])
                best_match = np.argmin(distances)
                if matches[best_match]:
                    return({'_id': _id, 'username': username})
                error = 'No matches.'
        else:
            error = 'Not known.'

        return {'error': error}
