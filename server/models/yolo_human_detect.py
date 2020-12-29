import cv2
import numpy as np

class HumanDetector:
    def __init__(self):
        self.net = cv2.dnn.readNet('./models/weights/yolov3.weights', './models/weights/yolov3.cfg')
        self.classes = self.get_yolo_classes()
        self.outs = None
        self.process_this_frame = True
        self.risk_score = 0
        self.number_detections = 0
        self.final_num_bkgnd = 0

    def get_yolo_classes(self):
        with open('./models/weights/coco.names', 'r') as f:
            classes = [line.strip() for line in f.readlines()]
        return classes

    def make_yolo_prediction(self, frame):
        self.net.setInput(cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False))
        layer_names = self.net.getLayerNames()
        output_layers = [layer_names[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]
        self.outs = self.net.forward(output_layers)

    def extract_box(self, detection, Width, Height):
        center_x = int(detection[0] * Width)
        center_y = int(detection[1] * Height)
        w = int(detection[2] * Width)
        h = int(detection[3] * Height)
        x = center_x - w / 2
        y = center_y - h / 2
        return x, y, w, h

    def list_to_dict(self, lst):
        res_dct = {str(i): lst[0][i] for i in range(0, len(lst[0]))}
        return res_dct

    def get_bounding_box(self, frame):
        class_ids = []
        confidences = []
        boxes = []
        Width = frame.shape[1]
        Height = frame.shape[0]
        for out in self.outs:
            
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.1:
                    x, y, w, h = self.extract_box(detection, Width, Height)
                    class_ids.append(class_id)
                    confidences.append(float(confidence))
                    boxes.append([x, y, w, h])
        return boxes, confidences, class_ids, class_id

    def draw_yolo_result(self, frame, boxes, confidences, class_ids, class_id):
        indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.1, 0.1)
        #check if is people detection
        for i in indices:
            i = i[0]
            box = boxes[i]
            if class_ids[i] == 0:
                # Adding here to re-increase risk score
                self.risk_score += 5
                self.number_detections += 1
                label = str(self.classes[class_id])
                cv2.rectangle(frame, (round(box[0]),round(box[1])),
                              (round(box[0]+box[2]),round(box[1]+box[3])), (0, 255, 0), 2)
                cv2.putText(frame, label, (round(box[0])-10,round(box[1])-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        return frame

    def yolo_main(self, frame, risk_score, face_net):
        self.risk_score = risk_score - (face_net.num_unauthorized + face_net.num_authorized) * 5
        if self.process_this_frame:
            self.make_yolo_prediction(frame)
            boxes, confidences, class_ids, class_id = self.get_bounding_box(frame)
            frame = self.draw_yolo_result(frame, boxes, confidences, class_ids, class_id)
        self.process_this_frame = not self.process_this_frame
        if self.risk_score < 0:
            self.risk_score = 0
        return frame

    def dump(self):
        self.number_detections = 0

