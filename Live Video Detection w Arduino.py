import math
import os
from ultralytics import YOLO
import cv2 as cv
import pyttsx3
import serial

trial_count = 15

last_num = 0

arduino_port = 'COM3'
baud_rate = 115200
ser = serial.Serial(arduino_port, baud_rate)

closest_distance = float('inf')
closest_label = None
closest_label_last_frame = None
grasp_attempts = 0  # This will be used to determine the number of objects they tried to "grasp"
guess_arr = [[], [], [], [], []]
guess_idx = 0
trial_num = 0

grasp_type = None
grasped = False
grasped_object = None

plastic_counter = 0
bottle_counter = 0
paper_counter = 0
can_counter = 0
styrofoam_counter = 0
all_counters = [plastic_counter, bottle_counter, paper_counter, can_counter, styrofoam_counter]

object_labels = []
object_distances = []


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
    print(f"Saved {image_filename}")


def read_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


not_object_counter = 0

model_path = os.path.join('C:/Users/dezmu/PycharmProjects/Web Scraping Images/runs/detect/train50', 'weights',
                          'best.pt')

model = YOLO(model_path)  # load a custom model

threshold = 0.9

no_label = 0
counts = 60

frame_counter = 15

cap = cv.VideoCapture(0)
save_folder = "C:/Users/dezmu/OneDrive/YOLO v8 Material Detection Project/1-31 Testing Screenshots"

while (True):
    while ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()

    while cap.isOpened():
        # Check for key presses
        key = cv.waitKey(1)

        closest_distance = float('inf')
        ret = False
        while not ret:
            ret, frame = cap.read()
        # frame = cv.rotate(frame, cv.ROTATE_180)

        # Get frame dimensions and put a center dot on the frame
        height, width, _ = frame.shape
        center = (width // 2, height // 2)
        cv.circle(frame, center, 5, (0, 0, 0), -1)

        # Real-time Object Detection
        results = model(frame)[0]

        # Check to see if object detection is active
        # ie The user has not grasped anything already

        if not grasped:  # The user isn't grasping anything
            # Check to see if there are objects in the frame
            if not results.boxes.data.tolist():

                not_object_counter = not_object_counter + 1
                # if not_object_counter == 10:
                #     grasp_type = None
                cv.rectangle(frame, (10, height - 40),
                             (10 + cv.getTextSize(grasp_type, cv.FONT_HERSHEY_SIMPLEX, 0.9, 1)[0][0] + 5,
                              height - 15),
                             (255, 255, 255), -1)
                cv.putText(frame, grasp_type, (10, height - 20), cv.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0), 1)

                no_label += 1
                if no_label >= counts:
                    grasp_type = "Unknown graped"

            # grasp_type = None
            # plastic_counter = bottle_counter = paper_counter = can_counter = styrofoam_counter = 0
            else:
                closest_distance = float('inf')
                object_labels.clear()
                object_distances.clear()
                for result in results.boxes.data.tolist():
                    x1, y1, x2, y2, score, class_id = result
                    if score > threshold:
                        label = results.names[int(class_id)].upper()
                        if class_id == 4:
                            label = "FOAM CUP"
                        object_labels.append(label)

                        # Determine the class colors
                        #    - Water Bottle- 1 light blue
                        #    - Plastic Cup- 0 red
                        #    - Styrofoam Cup- 4 yellow
                        #    - Paper Cup- 2 pink
                        #    - Soda Can- 3 purple
                        color_dictionary = [(255, 0, 0), (121, 242, 238), (247, 0, 100), (161, 31, 237), (244, 250, 7)]
                        class_color = color_dictionary[
                            int(class_id)]  # This accesses the second tuple in color_dictionary

                        # Draw the bounding boxes and the center
                        cv.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), class_color, 2)
                        x_center = int((x1 + x2) / 2)
                        y_center = int((y1 + y2) / 2)
                        cv.circle(frame, (x_center, y_center), radius=5, color=class_color, thickness=-1)

                        # Determine the pixel distance from the center for each know object
                        distance = math.sqrt(((x_center - (width // 2)) ** 2) + ((y_center - (height // 2)) ** 2))
                        object_distances.append(distance)
                        # closest_label_last_frame = closest_label

                        # Show the class id for every object along with drawing a line between the object and the center
                        # label_text = f"{label} ({score:.2f})"  # Include the score in the label text
                        label_text = f"{label}"  # Include the score in the label text
                        score_label = f"{score:.2f}"

                        # label_text = f"{class_id}"
                        cv.putText(frame, label_text, (int(x1), int(y1) - 10), cv.FONT_HERSHEY_SIMPLEX, 0.9, class_color,
                                   1, cv.LINE_AA)
                        cv.putText(frame, score_label, (int(x1) + 4, int(y1) + 32), cv.FONT_HERSHEY_SIMPLEX, 1,
                                    class_color, 1, cv.LINE_AA)

                        # cv.putText(frame, str(distance), (x_center, y_center + 20), cv.FONT_HERSHEY_SIMPLEX, 1,
                        #            class_color, 1,
                        #            cv.LINE_AA)
                        cv.line(frame, (x_center, y_center), center, color=class_color, thickness=1)

                if object_distances:
                    no_label = 0
                    idx_of_closest_object = object_distances.index(min(object_distances))
                    closest_label = object_labels[idx_of_closest_object]

                    if closest_label == results.names[int(0)].upper():
                        plastic_counter += 1
                        # bottle_counter = paper_counter = can_counter = styrofoam_counter = 0
                        if plastic_counter >= frame_counter:
                            bottle_counter = paper_counter = can_counter = styrofoam_counter = 0
                            grasp_type = "Plastic Cup"
                    elif closest_label == results.names[int(1)].upper():
                        bottle_counter += 1
                        # plastic_counter = paper_counter = can_counter = styrofoam_counter = 0
                        if bottle_counter >= frame_counter:
                            plastic_counter = paper_counter = can_counter = styrofoam_counter = 0
                            grasp_type = "Water Bottle"
                    elif closest_label == results.names[int(2)].upper():
                        paper_counter += 1
                        # plastic_counter = bottle_counter = can_counter = styrofoam_counter = 0
                        if paper_counter >= frame_counter:
                            plastic_counter = bottle_counter = can_counter = styrofoam_counter = 0
                            grasp_type = "Paper Cup"
                    elif closest_label == results.names[int(3)].upper():
                        can_counter += 1
                        # plastic_counter = bottle_counter = paper_counter = styrofoam_counter = 0
                        if can_counter >= frame_counter:
                            plastic_counter = bottle_counter = paper_counter = styrofoam_counter = 0
                            grasp_type = "Can grasp"
                            text_to_read = "Acquired"
                    elif closest_label == results.names[int(4)].upper():
                        styrofoam_counter += 1
                        # plastic_counter = bottle_counter = paper_counter = can_counter = 0
                        if styrofoam_counter >= frame_counter:
                            plastic_counter = bottle_counter = paper_counter = can_counter = 0
                            grasp_type = "Foam grasp"
                            text_to_read = "Acquired"
                            # read_text(text_to_read)
                    # else:
                    #     closest_label = None
                    #     grasp_type = "Unknown graped"
                    #     plastic_counter = bottle_counter = paper_counter = can_counter = styrofoam_counter = 0
                else:
                    no_label += 1
                    if no_label >= counts:
                        grasp_type = "Unknown graped"

                label_p = f"Plastic: {plastic_counter}"
                label_pap = f"Paper: {paper_counter}"
                label_s = f"Styro: {styrofoam_counter}"
                label_b = f"Bottle: {bottle_counter}"
                label_c = f"Can: {can_counter}"

                # cv.putText(frame, label_p, (10, height - 260), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)
                # cv.putText(frame, label_pap, (10, height - 240), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)
                # cv.putText(frame, label_s, (10, height - 220), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)
                # cv.putText(frame, label_b, (10, height - 200), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)
                # cv.putText(frame, label_c, (10, height - 180), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)




                # Show the current frame
                # cv.putText(frame, closest_label, (10, height - 60), cv.FONT_HERSHEY_SIMPLEX, 1.1, (0, 0, 0), 1)
                # grasping_label = f"Predicted Target Object: {grasp_type}"
                grasping_label = f"Predicted Target Object:"
                cv.rectangle(frame, (10, height - 80),
                             (10 + cv.getTextSize(grasping_label, cv.FONT_HERSHEY_SIMPLEX, 1, 1)[0][0] + 5,
                              height - 15),
                             (255, 255, 255), -1)
                cv.putText(frame, grasping_label, (10, height - 55), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)
                cv.rectangle(frame, (10, height - 40),
                             (10 + cv.getTextSize(grasp_type, cv.FONT_HERSHEY_SIMPLEX, 1, 1)[0][0] + 5,
                              height - 15),
                             (255, 255, 255), -1)
                cv.putText(frame, grasp_type, (10, height - 21), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)
                # cv.putText(frame, grasp_type, (10, height - 20), cv.FONT_HERSHEY_SIMPLEX, 1.1, (0, 0, 0), 1)

                cv.imshow('Webcam', frame)

                if trial_num >= trial_count:
                    print(guess_arr)
                    break

                if key == 32:  # 32 is the ASCII code for the space bar
                    take_photo(frame, save_folder)

                if ser.in_waiting > 0:
                    line = ser.readline().decode('utf-8').rstrip()
                    try:
                        number = int(line)
                        if number == 1 and not grasped:  # Check if not already grasped
                            number = 0
                            grasp_attempts = grasp_attempts + 1
                            trial_num = trial_num + 1
                            guess_arr[guess_idx].append(grasp_type)
                            if grasp_attempts == 15:
                                grasp_attempts = 0
                                guess_idx = guess_idx + 1
                            text_to_read = "Grasped"
                            # read_text(text_to_read)
                            grasped_object = grasp_type
                            grasped = True
                    except ValueError:
                        print("Received invalid data from Arduino:", line)


        else:
            cv.imshow('Webcam', frame)
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').rstrip()
                try:
                    number = int(line)
                    if number == 2 and grasped:
                        text_to_read = "Released"
                        # read_text(text_to_read)
                        plastic_counter = bottle_counter = paper_counter = can_counter = styrofoam_counter = 0
                        grasped_object = None
                        grasp_type = None
                        grasped = False
                except ValueError:
                    print("Received invalid data from Arduino:", line)



    cap.release()
    cv.destroyAllWindows()

else:
    pass
