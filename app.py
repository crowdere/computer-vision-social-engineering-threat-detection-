import cv2
import json
import numpy as np

from yolo_human_detect import HumanDetector
from face_classifier import FaceDetector
from security_features import EnterpriseShield
from gaze_tracking.gaze_tracking import GazeTracking

from flask import Flask
from flask_cors import CORS
from flask import request

import base64

# import logging
# log = logging.getLogger('werkzeug')
# log.setLevel(logging.ERROR)

app = Flask(__name__)
cors = CORS(app, resources={r"/processImage": {"origins": "*"}})

yolo_net = HumanDetector()
face_net = FaceDetector()
enterprise_shield = EnterpriseShield()
gaze = GazeTracking()


def preprocess_frame(frame):
    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    return small_frame[:, :, ::-1]


def encode_image(current_frame):
    return base64.b64encode(cv2.imencode('.jpg', current_frame)[1]).decode()


def decode_image(img_string):
    jpg_original = base64.b64decode(img_string)
    jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
    return cv2.imdecode(jpg_as_np, flags=1)


@app.route('/processImage', methods=['POST'])
def enterprise_shield_process_per_frame():
    # print(request.files['image'].read())
    frame = decode_image(request.files['image'].read())

    rgb_small_frame = preprocess_frame(frame)

    frame = face_net.process_frame(rgb_small_frame, frame)

    frame = yolo_net.yolo_main(frame)

    frame = gaze.per_face_gaze(frame)

    return encode_image(frame)


if __name__ == '__main__':
    app.run(port=80)
