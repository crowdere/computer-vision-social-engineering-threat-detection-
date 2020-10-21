import cv2
import os
# import torch
import numpy as np
import face_recognition
from glob import glob
import matplotlib.pyplot as plt
## Detectron2
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog

os.environ['KMP_DUPLICATE_LIB_OK']='True'


im = cv2.imread("./input.jpg")


def initialize_detectron2():
    # Create config
    cfg = get_cfg()
    cfg.merge_from_file("./detectron2-master/configs/COCO-Detection/faster_rcnn_R_101_FPN_3x.yaml")
    cfg.MODEL.DEVICE = 'cpu'
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5  # set threshold for this model
    cfg.MODEL.WEIGHTS = "detectron2://COCO-Detection/faster_rcnn_R_101_FPN_3x/137851257/model_final_f6e8b1.pkl"

    # Create predictor
    predictor = DefaultPredictor(cfg)
    return predictor, cfg

def make_detectron2_prediction(frame, predictor):
    frame = cv2.resize(frame, (480, 640))
    return predictor(frame)

def draw_detectron2_result(prediction, frame, cfg):
    v = Visualizer(frame[:, :, ::-1], MetadataCatalog.get(cfg.DATASETS.TRAIN[0]), scale=1.2)
    return v.draw_instance_predictions(prediction.to("cpu"))

if __name__ == '__main__':
    pred, cfg = initialize_detectron2()
    outputs = pred(im)
    person_instances = outputs['instances'][np.where(outputs['instances'].pred_classes == 0)]
    # print(outputs['instances'])
    v = draw_detectron2_result(person_instances, im, cfg)
    plt.imshow(v.get_image()[:, :, ::-1])
    plt.show()