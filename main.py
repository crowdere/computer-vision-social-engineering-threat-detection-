import cv2
from yolo_human_detect import HumanDetector
from face_classifier import FaceDetector
from opencv_eye_detection import EyeDetector
from security_features import EnterpriseShield
from gaze_tracking.gaze_tracking import GazeTracking

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

yolo_net = HumanDetector()
face_net = FaceDetector()
eye_net = EyeDetector()
enterprise_shield = EnterpriseShield()
gaze = GazeTracking()


def nothing():
    pass

cv2.namedWindow('video')
cv2.createTrackbar('threshold', 'video', 0, 255, nothing)


def preprocess_frame(frame):
    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    return small_frame[:, :, ::-1]


while True:
    ret, frame = video_capture.read()

    rgb_small_frame = preprocess_frame(frame)

    # Face recognition
    frame = face_net.process_frame(rgb_small_frame, frame)

    # Human detection
    frame = yolo_net.yolo_main(frame)

    frame = gaze.per_face_gaze(frame, face_net, eye_net)

    cv2.imshow('video', frame)

    # check for unknown entiites and alert user every ~30 seconds ish
    if face_net.face_names != []:
        enterprise_shield.notify_reset_timer(face_net.face_names[-1])

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()