import os
import cv2
import numpy as np
from glob import glob
import face_recognition

class FaceDetector:
    def __init__(self):
        self.dirname = os.path.dirname("__file__")
        self.path = os.path.join(self.dirname, 'known_people/')
        self.list_of_files, self.number_files, self.names = self.read_images()
        self.known_face_encodings, self.known_face_names = self.get_known_faces()
        self.face_locations = []
        self.face_names = []
        self.face_encodings = []
        self.process_this_frame = True
        self.risk_score = 0
        self.authorized_persons = self.names
        self.num_authorized = 0
        self.num_unauthorized = 0

    def read_images(self):
        """
        Make an array of all the images
        return: list, int,
        """
        list_of_files = [f for f in glob(self.path+'*.jpg')]
        number_files = len(list_of_files)
        names = list_of_files.copy()
        return list_of_files, number_files, names

    def get_known_faces(self):
        """
        get known names and face encodings
        return: two lists
        """
        known_face_encodings = []
        known_face_names = []
        for i in range(self.number_files):
            globals()['image_{}'.format(i)] = face_recognition.load_image_file(self.list_of_files[i])
            globals()['image_encoding_{}'.format(i)] = face_recognition.face_encodings(
                globals()['image_{}'.format(i)]
            )[0]
            known_face_encodings.append(globals()['image_encoding_{}'.format(i)])
            self.names[i] = self.names[i].replace("known_people/", "")
            known_face_names.append(self.names[i])
        return known_face_encodings, known_face_names

    def get_face_names(self, face_encodings):
        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            # If a match was found in known_face_encodings, just use the first one.
            # name = first_match(matches, known_face_names)
            name = self.known_face_match(face_encoding, matches)
            face_names.append(name)
        return face_names

    def process_frame(self, rgb_small_frame, frame):
        self.risk_score = 0
        if self.process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            self.face_locations = face_recognition.face_locations(rgb_small_frame)
            self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)
            self.face_names = self.get_face_names(self.face_encodings)
        self.process_this_frame = not self.process_this_frame
        return self.display_results(frame)

    def display_results(self, frame):
        """
        Displaying results
        return: None
        """
        self.risk_score_analysis()
        for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name.replace('.jpg', ''), (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        return frame

    def first_match(self, matches):
        # If a match was found in known_face_encodings
        if True in matches:
            first_match_index = matches.index(True)
            name = self.known_face_names[first_match_index]
            return name
        return 'Unknown'

    def known_face_match(self, face_encoding, matches):
        # use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = self.known_face_names[best_match_index]
            return name
        return 'Unknown'

    def risk_score_analysis(self):
        final_names = [name.replace('.jpg', '') for name in self.face_names]
        for name in final_names:
            if name.lower() == 'unknown':
                self.risk_score += 25
            elif name in self.authorized_persons:
                self.num_authorized += 1
            else:
                self.risk_score += 15
                self.num_unauthorized += 1

    def dump(self):
        self.num_authorized = 0
        self.num_unauthorized = 0
