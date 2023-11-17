from ultralytics import YOLO

# Load a model
model = YOLO("yolov8n.yaml")  # build a new model from scratch. Using the lightest version of yolo v8


# Use the model
model.train(data="config.yaml", epochs=150)  # train the model
