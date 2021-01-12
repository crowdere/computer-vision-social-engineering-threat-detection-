from __future__ import division
import os
import cv2
import dlib
from .eye import Eye
from .calibration import Calibration


class GazeTracking(object):
    """
    This class tracks the user's gaze.
    It provides useful information like the position of the eyes
    and pupils and allows to know if the eyes are open or closed
    """

    def __init__(self):
        self.frame = None
        self.eye_left = None
        self.eye_right = None
        self.calibration = Calibration()
        self.risk_score = 0
        self.final_risk_score = ''

        # _face_detector is used to detect faces
        self._face_detector = dlib.get_frontal_face_detector()

        # _predictor is used to get facial landmarks of a given face
        cwd = os.path.abspath(os.path.dirname(__file__))
        model_path = os.path.abspath(os.path.join(cwd, "trained_models/shape_predictor_68_face_landmarks.dat"))
        self._predictor = dlib.shape_predictor(model_path)

        # Custom additions for eye detection
        self.x_add = 0
        self.y_add = 0
        self.process_this_frame = True

    @property
    def pupils_located(self):
        """Check that the pupils have been located"""
        # try:
        #     int(self.eye_left.pupil.x)
        #     int(self.eye_left.pupil.y)
        #     int(self.eye_right.pupil.x)
        #     int(self.eye_right.pupil.y)
        #
        #
        #     return True
        # except Exception:
        #     return False
        return True
        # Removing all checking for now, we want to do the check for each pupil at some point

    def _analyze(self, face, frame):
        """Detects the face and initialize Eye objects"""
        try:
            landmarks = self._predictor(frame, face)
            self.eye_left = Eye(frame, landmarks, 0, self.calibration)
            self.eye_right = Eye(frame, landmarks, 1, self.calibration)

        except IndexError:
            self.eye_left = None
            self.eye_right = None

    def refresh(self, face, frame):
        """Refreshes the frame and analyzes it.

        Arguments:
            frame (numpy.ndarray): The frame to analyze
        """
        self.frame = frame
        self._analyze(face, frame)

    def pupil_left_coords(self):
        """Returns the coordinates of the left pupil"""
        if self.pupils_located:
            x = self.eye_left.origin[0] + self.eye_left.pupil.x + self.x_add
            y = self.eye_left.origin[1] + self.eye_left.pupil.y + self.y_add
            return (x, y)

    def pupil_right_coords(self):
        """Returns the coordinates of the right pupil"""
        if self.pupils_located:
            x = self.eye_right.origin[0] + self.eye_right.pupil.x + self.x_add
            y = self.eye_right.origin[1] + self.eye_right.pupil.y + self.y_add
            return (x, y)

    def horizontal_ratio(self):
        """Returns a number between 0.0 and 1.0 that indicates the
        horizontal direction of the gaze. The extreme right is 0.0,
        the center is 0.5 and the extreme left is 1.0
        """
        if self.pupils_located:
            pupil_left = self.eye_left.pupil.x / (self.eye_left.center[0] * 2 - 10)
            pupil_right = self.eye_right.pupil.x / (self.eye_right.center[0] * 2 - 10)
            return (pupil_left + pupil_right) / 2

    def vertical_ratio(self):
        """Returns a number between 0.0 and 1.0 that indicates the
        vertical direction of the gaze. The extreme top is 0.0,
        the center is 0.5 and the extreme bottom is 1.0
        """
        if self.pupils_located:
            pupil_left = self.eye_left.pupil.y / (self.eye_left.center[1] * 2 - 10)
            pupil_right = self.eye_right.pupil.y / (self.eye_right.center[1] * 2 - 10)
            return (pupil_left + pupil_right) / 2

    def is_right(self):
        """Returns true if the user is looking to the right"""
        if self.pupils_located:
            return self.horizontal_ratio() <= 0.35

    def is_left(self):
        """Returns true if the user is looking to the left"""
        if self.pupils_located:
            return self.horizontal_ratio() >= 0.65

    def is_center(self):
        """Returns true if the user is looking to the center"""
        if self.pupils_located:
            return self.is_right() is not True and self.is_left() is not True

    def is_blinking(self):
        """Returns true if the user closes his eyes"""
        if self.pupils_located:
            blinking_ratio = (self.eye_left.blinking + self.eye_right.blinking) / 2
            return blinking_ratio > 3.8

    def extended_frame_annotation(self, original_frame):
        """
        Custom function not in original code
        """
        self.frame = self.annotated_frame(original_frame)
        text = ""
        if self.is_right():
            text = "Looking right"
        elif self.is_left():
            text = "Looking left"
        elif self.is_center():
            text = "Looking center"

        h_ratio = "HR: " + str(self.horizontal_ratio())[:4]
        v_ratio = "VR: " + str(self.vertical_ratio())[:4]

        width = int(0.9 * self.frame.shape[1])
        height = int(0.9 * self.frame.shape[0])

        # cv2.putText(self.frame, text, (60, 60), cv2.FONT_HERSHEY_DUPLEX, 2, (255, 0, 0), 2)
        # cv2.putText(self.frame, h_ratio, (60, height), cv2.FONT_HERSHEY_DUPLEX, 2, (255, 0, 0), 2)
        # cv2.putText(self.frame, v_ratio, (int(0.8 * width), height), cv2.FONT_HERSHEY_DUPLEX, 2, (255, 0, 0), 2)
        return self.frame

    def per_face_gaze(self, frame, risk_score, face_net):
        """
        Custom function 2
        """
        self.risk_score = risk_score
        if self.process_this_frame:
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self._face_detector(frame_gray)

            for face in faces:
                self.refresh(face, frame)
                frame = self.extended_frame_annotation(frame)
        # self.process_this_frame = not self.process_this_frame
            self.risk_score_analysis(faces, face_net.num_authorized)
        return frame

    def annotated_frame(self, original_frame):
        """Returns the main frame with pupils highlighted"""
        frame = original_frame.copy()

        if self.pupils_located:
            color = (0, 255, 0)
            x_left, y_left = self.pupil_left_coords()
            x_right, y_right = self.pupil_right_coords()
            cv2.line(frame, (x_left - 5, y_left), (x_left + 5, y_left), color)
            cv2.line(frame, (x_left, y_left - 5), (x_left, y_left + 5), color)
            cv2.line(frame, (x_right - 5, y_right), (x_right + 5, y_right), color)
            cv2.line(frame, (x_right, y_right - 5), (x_right, y_right + 5), color)

        return frame

    def risk_score_analysis(self, faces, authorized):
        if len(faces) - authorized >= 0:
            self.risk_score += (len(faces) - authorized) * 10

