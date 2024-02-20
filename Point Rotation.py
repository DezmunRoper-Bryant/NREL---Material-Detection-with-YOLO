import os
import math

input_folder = "C:/Users/dezmu/OneDrive/YOLO v8 Material Detection Project/labels/dezzy test"  # Replace with the path to your input folder
output_folder = "C:/Users/dezmu/OneDrive/YOLO v8 Material Detection Project/labels/dezzy output"  # Replace with the path to your output folder


def process_yolo_format(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    bounding_boxes = []
    for line in lines:
        parts = line.strip().split()
        if len(parts) == 5 and parts[0].isdigit():
            x, y, width, height = map(float, parts[1:])
            bounding_boxes.append((x, y, width, height))

    return bounding_boxes


def rotate_bounding_boxes(bounding_boxes, angle):
    rotated_boxes = []
    for box in bounding_boxes:
        x, y, width, height = box
        origin_x = 0.5
        origin_y = 0.5
        angle_rad = math.radians(angle)

        # Translate to the origin, rotate, and then translate back
        rotated_x = (x - origin_x) * math.cos(angle_rad) - (y - origin_y) * math.sin(angle_rad) + origin_x
        rotated_y = (x - origin_x) * math.sin(angle_rad) + (y - origin_y) * math.cos(angle_rad) + origin_y

        # Rotate width and height
        rotated_width = abs(width * math.cos(angle_rad)) + abs(height * math.sin(angle_rad))
        rotated_height = abs(width * math.sin(angle_rad)) + abs(height * math.cos(angle_rad))

        rotated_boxes.append((rotated_x, rotated_y, rotated_width, rotated_height))

    return rotated_boxes


def save_rotated_bounding_boxes(file_name, rotated_boxes, output_folder):
    rotated_file_path = os.path.join(output_folder, file_name.replace(".txt", "_rotated.txt"))
    with open(rotated_file_path, 'w') as rotated_file:
        for box in rotated_boxes:
            rotated_file.write(f"1 {box[0]:.6f} {box[1]:.6f} {box[2]:.6f} {box[3]:.6f}\n")


def process_and_save_rotated_bounding_boxes(input_folder, output_folder, angle):
    for file_name in os.listdir(input_folder):
        if file_name.endswith(".txt"):
            file_path = os.path.join(input_folder, file_name)
            bounding_boxes = process_yolo_format(file_path)
            rotated_boxes = rotate_bounding_boxes(bounding_boxes, angle)
            save_rotated_bounding_boxes(file_name, rotated_boxes, output_folder)


# Call the function to process and save rotated bounding boxes
process_and_save_rotated_bounding_boxes(input_folder, output_folder, angle=30)
