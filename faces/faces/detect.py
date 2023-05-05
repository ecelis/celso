import os

import cv2
import face_recognition


known_path = os.environ['UPLOADS_DIR']
# unknown_path = os.path.join(os.getcwd(), "Images/Unknown_faces/")


def register(file_name):
    img = cv2.imread(os.path.join(known_path, file_name))
    small_img = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
    rgb_small_img = small_img[:, :, ::-1]
    face_locations = face_recognition.face_locations(rgb_small_img)
    face_encodings = face_recognition.face_encodings(rgb_small_img, face_locations)

    # ret, frame = video_capture.read()
    # small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    # rgb_small_frame = small_frame[:, :, ::-1]
    # face_locations = face_recognition.face_locations(rgb_small_frame)
    # face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
    dir = os.path.join(known_path,name)
    if(not os.path.isdir(dir)):
        os.mkdir(dir)
    os.chdir(dir) 
    rand_no = np.random.random_sample()
    cv2.imwrite(str(rand_no)+".jpg", frame)
    video_capture.release()
    cv2.destroyAllWindows()
    encoding = ""
    for i in face_encodings:
        encoding += str(i)+","
    li = [name, encoding]

def match():
    msg = ''
    video_capture = cv2.VideoCapture(0)
    ret, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
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
