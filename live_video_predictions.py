import os

from ultralytics import YOLO
import cv2 as cv

model_path = os.path.join('C:/Users/dezmu/PycharmProjects/Web Scraping Images/runs/detect/train13', 'weights', 'last.pt')
model = YOLO(model_path)  # load a custom model

threshold = 0.7

cap = cv.VideoCapture(0)
# Get a frame from the capture device
while cap.isOpened():
    ret, frame = cap.read()

    frame = cv.flip(frame, 1)

    results = model(frame)[0]

    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result
        if score > threshold:
            label = results.names[int(class_id)].upper()

            if int(class_id) == 0:
                class_color = (121, 242, 238)
            elif int(class_id) == 1:
                class_color = (255, 0, 0)
            elif int(class_id) == 2:
                class_color = (247, 203, 203)
            elif int(class_id) == 3:
                class_color = (128, 128, 128)
            elif int(class_id) == 4:
                class_color = (244, 250, 7)
            elif int(class_id) == 5:
                class_color = (154, 31, 237)

            width = frame.shape[1]
            height = frame.shape[0]
            cv.circle(frame, (height//2, width//2), radius = 5, color = (0, 0, 0), thickness =-1)

            label_text = f"{label} ({score:.2f})"  # Include the score in the label text
            cv.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), class_color, 2)
            x_center = int((x1 + x2) / 2)
            y_center = int((y1 + y2) / 2)
            cv.circle(frame, (x_center, y_center), radius=5, color=class_color, thickness=-1)
            cv.putText(frame, label_text, (int(x1), int(y1) - 10), cv.FONT_HERSHEY_SIMPLEX, 1.1, class_color, 1,
                        cv.LINE_AA)
            if ((x_center == width // 2) and (y_center == height // 2)):
                cv.putText(frame, label, (0, 0), cv.FONT_HERSHEY_SIMPLEX, 1.1, (0, 0, 0), 1)



    # for result in results.boxes.data.tolist():
    #     x1, y1, x2, y2, score, class_id = result
    #     if score > threshold:
    #         cv.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 2)
    #         cv.putText(frame, results.names[int(class_id)].upper(), (int(x1), int(y1 - 10)),
    #                     cv.FONT_HERSHEY_SIMPLEX, 1.3, (255, 0, 0), 2, cv.LINE_AA)
    # Show image
    cv.imshow('Webcam', frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
