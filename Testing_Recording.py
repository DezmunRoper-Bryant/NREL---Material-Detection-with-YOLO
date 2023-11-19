import os
from ultralytics import YOLO
import cv2

# would like to change the document so that
# Use a past number of frames to determine the actual material. If a label is above the threshold for 10 frames
# (in succession), it is that material

VIDEOS_DIR = os.path.join('C:/Users/dezmu/OneDrive/YOLO v8 Material Detection Project', 'videos')

capture_videos = ['Material Test 003.mp4']
# capture_videos = ['Material Test 001.mp4', 'Material Test 002.mp4', 'Material Test 003.mp4']

for video_name in capture_videos:

    video_path = os.path.join(VIDEOS_DIR, video_name)
    video_path_out = '{}_out.mp4'.format(video_path)

    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()
    H, W, _ = frame.shape
    out = cv2.VideoWriter(video_path_out, cv2.VideoWriter_fourcc(*'MP4V'), int(cap.get(cv2.CAP_PROP_FPS)), (W, H))

    model_path = os.path.join('C:/Users/dezmu/PycharmProjects/Web Scraping Images/runs/detect/train15', 'weights',
                              'best.pt')

    # Load a model
    model = YOLO(model_path)  # load a custom model

    threshold = 0.5

    while ret:
        results = model(frame)[0]

        for result in results.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = result
            if score > threshold:  # Ensures that on values above the threshold get a bounding box
                label = results.names[int(class_id)].upper()

                # Change the color of the bounding box based on the class_id
                if int(class_id) == 0:
                    class_color = (121, 242, 238)
                elif int(class_id) == 1:
                    class_color = (255, 0, 0)
                elif int(class_id) == 2:
                    class_color = (247, 203, 203)
                elif int(class_id) == 3:
                    class_color = (128, 128, 128)
                elif int(class_id) == 4:
                    class_color = (249, 252, 136)
                elif int(class_id) == 5:
                    class_color = (204, 128, 255)

                label_text = f"{label} ({score:.2f})"  # Include the score in the label text
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), class_color, 2)
                cv2.putText(frame, label_text, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.1, class_color, 1,
                            cv2.LINE_AA)

        out.write(frame)
        ret, frame = cap.read()

    cap.release()
    out.release()
    cv2.destroyAllWindows()
