import cv2 as cv
import os

def get_next_image_number(save_path):
    image_files = [f for f in os.listdir(save_path) if f.startswith("image") and f.endswith(".png")]
    if not image_files:
        return 1
    image_numbers = [int(f.split("image")[1].split(".png")[0]) for f in image_files]
    return max(image_numbers) + 1

def take_photo(frame, save_path):
    image_count = get_next_image_number(save_path)
    image_filename = f"image{image_count}.png"
    cv.imwrite(os.path.join(save_path, image_filename), frame)

cap = cv.VideoCapture(0)
save_folder = "C:/Users/dezmu/OneDrive/YOLO v8 Material Detection Project/Images_from_capture2"

# Ensure the save folder exists
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

# Get a frame from the capture device
while cap.isOpened():
    ret, frame = cap.read()
    frame = cv.flip(frame, 1)
    # Show the current frame
    cv.imshow('Webcam', frame)

    # Check for key presses
    key = cv.waitKey(1)

    # Press 'q' to exit the loop
    if key & 0xFF == ord('q'):
        break

    # Press the space bar to capture and save the current frame
    if key == 32:  # 32 is the ASCII code for the space bar
        take_photo(frame, save_folder)

cap.release()
cv.destroyAllWindows()


