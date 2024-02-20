# This document is just a demo for the external webcam
import cv2 as cv

def take_photo():
    cap = cv.VideoCapture(0)
    ret, frame = cap.read()
    cv.imwrite('Webcamphoto.png', frame)
    cap.release()


cap = cv.VideoCapture(0)
# Get a frame from the capture device
while cap.isOpened():
    ret, frame = cap.read()
    # Show image
    cv.imshow('Webcam', frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
