import cv2
import json
import numpy as np
from azure import AzureConnector
import time
# For production server
from waitress import serve

from models.yolo_human_detect import HumanDetector
from models.face_classifier import FaceDetector
from models.gaze_tracking.gaze_tracking import GazeTracking
from evaluation.Doctor import Doctor

from flask import Flask
from flask_cors import CORS
from flask import request

import base64
import logging

# Log file
# Structure
# Timestamp | Username | Risk Score | Number of background actors (no face or gaze)
# | Number of unauthorized or unknown faces
logging.basicConfig(filename='./logs/risk.csv', level=logging.INFO)
# logging.info("Timestamp,username,risk score,background actors,unauthorized detections")


# log = logging.getLogger('werkzeug')
# log.setLevel(logging.ERROR)

app = Flask(__name__)
cors = CORS(app, resources={r"/processImage": {"origins": "*"}})

# download and replace newest list of authorized people
AzureConnector.update_known_people()

yolo_net = HumanDetector()
face_net = FaceDetector()
gaze = GazeTracking()
doctor = Doctor()


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


def log_event(username, gaze, yolo_net, face_net):

    unauthorized_unknown_count = face_net.num_unauthorized + face_net.num_unknown

    log_string = f"{time.time()},{str(username)},{gaze.final_risk_score}," \
                 f"{yolo_net.final_num_bkgnd},{unauthorized_unknown_count}"

    logging.info(log_string)


@app.route('/processImage', methods=['POST'])
def enterprise_shield_process_per_frame():
    # print(request.files['image'].read())
    frame = decode_image(request.files['image'].read())

    width = int(0.9 * frame.shape[1])
    height = int(0.9 * frame.shape[0])

    rgb_small_frame = preprocess_frame(frame)

    frame = face_net.process_frame(rgb_small_frame, frame)

    frame = yolo_net.yolo_main(frame, face_net.risk_score, face_net)

    frame = gaze.per_face_gaze(frame, yolo_net.risk_score, face_net)

    if not yolo_net.process_this_frame:
        gaze.final_risk_score = str(gaze.risk_score)
        yolo_net.final_num_bkgnd = abs(len(face_net.face_names) - yolo_net.number_detections)
        doctor.log_images(frame, request.files['session_name'].read(), request.files['img_index'].read(),
                          request.files['username'].read())

        yolo_net.dump()

    cv2.rectangle(frame, (int(0.35 * width), int(height*1.01)), (int(0.35 * width + 0.45*width),
                                                                 int(height*1.01 - 60)), (0, 0, 0), -1)

    cv2.putText(frame, "Risk Score: " + gaze.final_risk_score,
                (int(0.35 * width), height), cv2.FONT_HERSHEY_DUPLEX, 2, (255, 255, 255), 2)

    log_event(request.files['username'].read(), gaze, yolo_net, face_net)

    face_net.dump()

    return json.dumps({"image": encode_image(frame), "risk_score": gaze.risk_score})


if __name__ == '__main__':
    # app.run(port=80)
    serve(app, host='0.0.0.0', port=80)
