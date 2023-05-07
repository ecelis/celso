import os
import glob
from PIL import Image
from base64 import b64decode
from io import BytesIO
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
        error = None
        # small_img = cv2.resize(image, (0, 0), fx=0.25, fy=0.25)
        # rgb_small_img = small_img[:, :, ::-1]
        # print(rgb_small_img)
        locations = face_locations(image)
        locations_len = len(locations)
        if locations_len > 1:
           raise ValueError('More than one face detected.')
        if locations_len < 1:
           raise ValueError("Couldn't detect any face.")
        encodings = face_encodings(image, locations)
        return encodings

    def encode(self, id, username):
        """Read images from file system and encode them all."""
        id_path = os.path.join(samples, id)
        images = [cv2.imread(file) for file in glob.glob(id_path + '/*.jpg')]
        try:
            encodings = list(map(self.get_encodings, images))
            result = save_encodings(id, username, encodings)
            return result
        except ValueError as error:
            print(error)
            return {'error': error}
        
    def match(self, picture):
        """Match face with known encodings from data base."""
        error = None
        image_encodings = None
        id = None
        matches = None
        encodings = list(find_all())
        image_data = b64decode(str(picture.split(',')[1]))
        image = Image.open(BytesIO(image_data))
        # image.save('/tmp/image.jpg')
        cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)
        try:
            image_encodings = self.get_encodings(cv_image)
        except ValueError as error:
            print(error)
            return {'error': error}
        # print(image_encodings)
        if image_encodings:
            for face in encodings:
                id = str(face['_id'])
                username = str(face['username'])
                samples = [np.array(x) for x in face['encodings']]
                matches = compare_faces(samples, image_encodings[0])
                # for sample in samples:
                #     matches = compare_faces(sample, image_encodings)
                distances = face_distance(samples, image_encodings[0])
                best_match = np.argmin(distances)
                if matches[best_match]:
                    return({'_id': id, 'username': username})
                else:
                    error = 'No matches.'
        else:
            error = 'Not known.'
            # for (top, right, bottom, left), name in zip(face_locations, face_names):
            #     top *= 4
            #     right *= 4
            #     bottom *= 4
            #     left *= 4
            #     cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            #     cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            #     font = cv2.FONT_HERSHEY_DUPLEX
            #     cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        return {'error': error}
