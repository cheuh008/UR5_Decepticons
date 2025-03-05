import cv2, warnings, time, threading, os
import numpy as np
import pandas as pd

current_dir = os.path.dirname(os.path.abspath(__file__))

def capture_image():
    save_path = os.path.join(current_dir, 'test_picture_store')
    os.makedirs(save_path, exist_ok=True)
    
    try:
        # Determine the next available file name
        existing_files = [f for f in os.listdir(save_path) if f.startswith("captured_image_") and f.endswith(".jpg")]
        next_number = max([int(f.split("_")[-1].split(".")[0]) for f in existing_files], default=-1) + 1
        img_name = os.path.join(save_path, f"captured_image_{next_number}.jpg")
        
        cam = cv2.VideoCapture(0)
        if not cam.isOpened():
            print("Error: Could not open camera.")
            return None, None
        
        ret, frame = cam.read()
        cam.release()
        cv2.destroyAllWindows()
        
        if not ret or frame is None:
            print("Error: Failed to capture image.")
            return None, None
        
        # Get image dimensions
        h, w, _ = frame.shape
        
        # Define crop area for upper center slightly to the right
        crop_width, crop_height = w // 4, h // 4  # Adjust for finer cropping
        start_x = (w // 2) + (w // 8) - (crop_width // 2)  # Upper center, slightly right
        start_y = h // 8  # Upper section
        
        cropped_frame = frame[start_y:start_y + crop_height, start_x:start_x + crop_width]
        
        if cropped_frame is None or cropped_frame.size == 0:
            print("Error: Cropping failed, resulting in an empty image.")
            return None, None
        
        cv2.imwrite(img_name, cropped_frame)
        print(f"Cropped image saved at {img_name}")
        
        return img_name, cropped_frame
    except Exception as e:
        print(f"Unexpected error in capture_image(): {e}")
        return None, None

def extract_rgb(image_path, image):
    if image is None:
        print("Error: No image to extract RGB from.")
        return
    
    try:
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        avg_color = np.mean(image_rgb, axis=(0, 1))  # Compute mean RGB
        r, g, b = int(avg_color[0]), int(avg_color[1]), int(avg_color[2])
        sample_id = os.path.basename(image_path).split("_")[-1].split(".")[0]
        
        csv_path = os.path.join(current_dir, 'RGB_values_test.csv')
        df = pd.DataFrame([[sample_id, r, g, b]], columns=["Sample_ID", "Red", "Green", "Blue"])
        df.to_csv(csv_path, mode='a', header=not os.path.exists(csv_path), index=False)
        
        print(f"Saved RGB values to {csv_path}")
    except Exception as e:
        print(f"Error processing RGB values: {e}")

def process_image():
    image_data = capture_image()
    if image_data and image_data[0] is not None and image_data[1] is not None:
        extract_rgb(image_data[0], image_data[1])
    else:
        print("Skipping RGB extraction due to image capture failure.")

        
# Run the Colour Change Detector
if __name__ == "__main__":
    pass