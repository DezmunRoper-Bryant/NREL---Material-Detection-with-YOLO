import os
import cv2
import numpy as np
import shutil


def apply_random_tint_or_gamma_correction(image, label, output_folder, output_label_folder):
    # Decide randomly whether to apply gamma correction or tint
    if np.random.choice([True, False]):
        # Apply random gamma correction
        random_gamma = np.random.choice([0.4, 3])
        corrected_image = np.power(image / 255.0, random_gamma) * 255.0
        operation_type = "gamma"
    else:
        # Apply random tint
        random_tint_color = np.random.randint(0, 256, size=(3,))
        random_tint_color = random_tint_color / 255.0
        tinted_image = np.ones_like(image) * random_tint_color * 255
        corrected_image = cv2.add(image.astype(np.float32) * 0.5, tinted_image.astype(np.float32) * 0.)
        corrected_image = np.uint8(corrected_image)
        operation_type = "tint"

    # Save the corrected image
    base_filename = os.path.splitext(os.path.basename(label))[0]
    save_path = os.path.join(output_folder, f"{operation_type}_altered_{base_filename}.png")
    cv2.imwrite(save_path, corrected_image)

    # Copy the corresponding label file to the output label folder
    output_label_path = os.path.join(output_label_folder, f"{operation_type}_altered_{base_filename}.txt")
    shutil.copy2(label, output_label_path)


# Specify your paths
input_folder = r"C:\Users\dezmu\OneDrive\YOLO v8 Material Detection Project\Dataset\Original Images"
output_folder = r"C:\Users\dezmu\OneDrive\YOLO v8 Material Detection Project\Dataset\Colored Images"
output_label_folder = r"C:\Users\dezmu\OneDrive\YOLO v8 Material Detection Project\Dataset\Colored Labels"
# Create output label folder if it doesn't exist
os.makedirs(output_label_folder, exist_ok=True)

# Process each image in the input folder
for image_file in os.listdir(input_folder):
    if image_file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
        image_path = os.path.join(input_folder, image_file)
        label_path = os.path.join(r"C:\Users\dezmu\OneDrive\YOLO v8 Material Detection Project\Dataset\Original Labels",
                                  f"{os.path.splitext(image_file)[0]}.txt")

        # Apply random tint or gamma correction
        apply_random_tint_or_gamma_correction(cv2.imread(image_path), label_path, output_folder, output_label_folder)
