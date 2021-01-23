import torch
import cv2

model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

class YoloV5:
    def __init__(self):
        self.model = model
        self.risk_score = 0
        self.number_detections = 0
        self.final_num_bkgnd = 0

    def make_prediction(self, frame, risk_score, face_net):
        self.risk_score = risk_score - (face_net.num_unauthorized + face_net.num_authorized) * 5
        pred = model(frame)
        detections = pred.xyxy[0].numpy()
        for box in detections:
            if int(box[5]) == 0:# and box[4] >= 0.75:
                self.risk_score += 5
                self.number_detections += 1
                cv2.rectangle(frame, (round(box[0]),round(box[1])), (round(box[2]),round(box[3])), (255, 0, 0), 2)
        if self.risk_score < 0:
            self.risk_score = 0
        return frame

    def dump(self):
        self.number_detections = 0

if __name__ == '__main__':
    video_capture = cv2.VideoCapture(0)
    cv2.namedWindow('video')
    while True:
        yolo_net = YoloV5()
        ret, frame = video_capture.read()
        frame = yolo_net.make_prediction(frame, 0, 0)
        cv2.imshow('video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()