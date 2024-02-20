import cv2
from ultralytics import YOLO
import os

# Load YOLO model
model_path = os.path.join('C:/Users/dezmu/PycharmProjects/Web Scraping Images/runs/detect/train39', 'weights',
                          'best.pt')
model = YOLO(model_path)  # load a custom model

# Path to the folder containing images
images_folder = 'C:/Users/dezmu/OneDrive/YOLO v8 Material Detection Project/labels/0demo/rand_test_images/'

# Output folder for saving images with bounding boxes
output_folder = 'C:/Users/dezmu/OneDrive/YOLO v8 Material Detection Project/output/'

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Get a list of image file paths in the folder
image_files = [os.path.join(images_folder, file) for file in os.listdir(images_folder) if
               file.lower().endswith(('png', 'jpg', 'jpeg'))]

# Process each image
for image_path in image_files:
    # Run inference on the current image
    results = model([image_path])

    # Get the first result from the list (assuming only one image is processed in this example)
    result = results[0]

    # Check if there are any detected objects
    if result.boxes is not None and result.probs is not None:
        # Read the image using OpenCV
        image = cv2.imread(image_path)

        # Loop through the bounding boxes and draw rectangles on the image
        for box, prob in zip(result.boxes, result.probs):
            box = [round(coord, 2) for coord in box]  # Round coordinates to two decimal places
            start_point = (int(box[0]), int(box[1]))
            end_point = (int(box[2]), int(box[3]))
            color = (0, 0, 255)  # BGR color for red
            thickness = 1
            image = cv2.rectangle(image, start_point, end_point, color, thickness)
            label = f'Class: {model.names[int(prob.argmax())]}, Prob: {round(prob.max(), 2)}'
            image = cv2.putText(image, label, (int(box[0]), int(box[1]) - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color,
                                thickness, cv2.LINE_AA)

        # Save the image with bounding boxes
        output_path = os.path.join(output_folder, os.path.basename(image_path))
        cv2.imwrite(output_path, image)

        # Display the image with bounding boxes using OpenCV
        cv2.imshow('Image with Bounding Boxes', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # Print a statement to indicate that the image has been saved
        print(f"Image saved to {output_path}")
    else:
        print(f"No objects detected in {image_path}")

    # Print some information for debugging
    print("Result Boxes:", result.boxes)
    print("Result Probs:", result.probs)
    print("Model Names:", model.names)
