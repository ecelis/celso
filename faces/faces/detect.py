import os
import glob
import cv2
from face_recognition import face_encodings, face_locations
from faces.helpers import save_encodings

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

    def encode(self, id):
        """Read images from file system and encode them all."""
        id_path = os.path.join(samples, id)
        images = [cv2.imread(file) for file in glob.glob(id_path + '/*.jpg')]
        try:
            encodings = list(map(self.get_encodings, images))
            result = save_encodings(id, encodings)
            return result
        except ValueError as error:
            print(error)
            return {'error': repr(error)}
        
    def match(self, id):
        msg = ''
        video_capture = cv2.VideoCapture(0)
        ret, frame = video_capture.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]
        face_locations = face_locations(rgb_small_frame)
        face_encodings = face_encodings(rgb_small_frame, face_locations)
        face_names = []
        if(face_encodings == []):
            msg = 'Faces not found'
        else:
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                if(name == "Unknown"):
                    msg = "You are unknown first register your self"
                else:
                    msg = name
                face_names.append(name)
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            os.chdir(unknown_path)
            rand_no = np.random.random_sample()
            cv2.imwrite(str(rand_no)+".jpg", frame)
