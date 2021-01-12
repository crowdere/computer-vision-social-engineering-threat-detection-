import cv2
import time

class Doctor:
    """
    A class that logs the images
    """
    def __init__(self):
        self.image_risk_score = {}

    def log_images(self, frame, session_name, index, username):
        cv2.imwrite(f'./evaluation/ImageData/{str(session_name.decode("utf-8"))}_{str(username.decode("utf-8"))}'
                    f'_{str(index.decode("utf-8"))}.jpg', frame)

