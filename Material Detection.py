# # This document loads the yolo model and starts training.

import os
from ultralytics import YOLO

def main():
    model = YOLO("yolov8m.yaml")  # build a new model from scratch. Using the lightest version of YOLOv8
    # model.train(data="config.yaml", epochs=300, device=0, cfg="yolov8m.yaml", yolo="--erasing=0.25 --degrees=60 --hsv_h=0.1")

    model.train(data="config.yaml", epochs=200, device=0)  # train the model
    # model_path = os.path.join('C:/Users/dezmu/PycharmProjects/Web Scraping Images/runs/detect/train29', 'weights','last.pt')
    # model = YOLO(model_path)  # load a custom model
    # metrics = model.val()

if __name__ == '__main__':
    main()