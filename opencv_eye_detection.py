import cv2
import numpy as np

class EyeDetector:
    def __init__(self):
        self.detector_params = cv2.SimpleBlobDetector_Params()
        self.detector_params.filterByArea = True
        self.detector_params.maxArea = 1500
        self.net = cv2.CascadeClassifier('haarcascade_eye.xml')
        self.detector = cv2.SimpleBlobDetector_create(self.detector_params)
        self.process_this_frame = True

    def crop_face(self, img, x, y, w, h):
        return img[y:y + h, x:x + w]

    def detect_eyes(self, img):
        gray_frame = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        eyes = self.net.detectMultiScale(gray_frame, 1.03, 5)  # detect eyes
        width = np.size(img, 1)  # get face frame width
        height = np.size(img, 0)  # get face frame height
        left_eye = None
        right_eye = None
        for (x, y, w, h) in eyes:
            if y > height / 2:
                pass
            eyecenter = x + w / 2  # get the eye center
            if eyecenter < width * 0.5:
                left_eye = img[y:y + h, x:x + w]
            else:
                right_eye = img[y:y + h, x:x + w]

            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

        return left_eye, right_eye

    def cut_eyebrows(self, img):
        height, width = img.shape[:2]
        eyebrow_h = int(height / 4)
        img = img[eyebrow_h:height, 0:width]  # cut eyebrows out (15 px)
        return img

    def blob_process(self, img, threshold):
        gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, img = cv2.threshold(gray_frame, threshold, 255, cv2.THRESH_BINARY)
        img = cv2.erode(img, None, iterations=2)
        img = cv2.dilate(img, None, iterations=4)
        img = cv2.medianBlur(img, 5)
        keypoints = self.detector.detect(img)
        return keypoints

    def eye_detection_main(self, frame, face_locations):
        if self.process_this_frame:
            for (y, w, h, x) in face_locations:
                cropped_face = self.crop_face(frame, x*4, y*4, w*2, h) ## as done before in face recog display results
                if cropped_face is not None:
                    eyes = self.detect_eyes(cropped_face)
                    threshold = r = cv2.getTrackbarPos('threshold', 'video')
                    for eye in eyes:
                        if eye is not None:
                            eye = self.cut_eyebrows(eye)
                            keypoints = self.blob_process(eye, threshold)
                            eye = cv2.drawKeypoints(eye, keypoints, eye, (0, 0, 255),
                                                    cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        self.process_this_frame = not self.process_this_frame

        return frame