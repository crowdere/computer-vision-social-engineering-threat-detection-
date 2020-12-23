import cv2
import requests
import numpy as np
from security_features import EnterpriseShield
import base64
import json


def nothing():
    pass


def encode_image(current_frame):
    return base64.b64encode(cv2.imencode('.jpg', current_frame)[1]).decode()


def decode_image(img_string):
    jpg_original = base64.b64decode(img_string)
    jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
    return cv2.imdecode(jpg_as_np, flags=1)


if __name__ == '__main__':
    video_capture = cv2.VideoCapture(0)
    enterprise_shield = EnterpriseShield()
    cv2.namedWindow('video')

    while True:
        ret, frame = video_capture.read()
        frame_json = {'image': encode_image(frame)}
        json_response = json.loads(requests.post(f'http://localhost:80/processImage', files=frame_json).text)

        image_b64 = json_response['image']
        risk_score = int(json_response['risk_score'])

        frame = decode_image(image_b64)

        # enterprise_shield.unleash_defense(risk_score)

        cv2.imshow('video', frame)

        # check for unknown entiites and alert user every ~30 seconds or so
        # if face_net.face_names != []:
        #     enterprise_shield.notify_reset_timer(face_net.face_names[-1])

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()
