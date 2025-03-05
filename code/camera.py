import cv2, warnings, time, threading, os
import numpy as np
import pandas as pd


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

        
warnings.filterwarnings("ignore")
current_dir = os.path.dirname(os.path.abspath(__file__))

# Colour Ranges (Adjust as needed)
lower_yellow = np.array([20, 100, 100])
upper_yellow = np.array([30, 255, 255])
lower_blue = np.array([100, 100, 50])
upper_blue = np.array([130, 255, 255])

def colour_pixels(mask):
    """ Counts Pixels """
    return np.sum(mask > 0)

def crop_vial(image):
    """ Crop Only the Vial Area """
    height, width, _ = image.shape
    return image[int(height * 0.3):int(height * 0.8), int(width * 0.4):int(width * 0.6)]


def capture_image():
    save_path = os.path.join(current_dir, 'test_picture_store')
    os.makedirs(save_path, exist_ok=True)
    
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("Error: Could not open camera.")
        return
    
    ret, frame = cam.read()
    if ret:
        img_name = os.path.join(save_path, "captured_image.jpg")
        cv2.imwrite(img_name, frame)
        print(f"Image saved at {img_name}")
    else:
        print("Failed to capture image.")
    
    cam.release()
    cv2.destroyAllWindows()

def open_camera():
    """ Open Camera in a Separate Thread """
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("Camera Feed")
    img_counter = 0

    while True:
        ret, frame = cam.read()
        if not ret:
            print("Failed to grab frame")
            break
        cv2.imshow("Camera Feed", frame)

        k = cv2.waitKey(1)
        if k % 256 == 27:  # ESC key to exit
            print("Escape hit, closing...")
            break
        elif k % 256 == 32:  # SPACE key to capture image
            img_name = f"opencv_frame_{img_counter}.png"
            cv2.imwrite(img_name, frame)
            print(f"{img_name} written!")
            img_counter += 1

    cam.release()
    cv2.destroyAllWindows()

# Start camera thread
camera_thread = threading.Thread(target=open_camera, daemon=True)
camera_thread.start()

""" Colour Change Detector Function """
def colour_change_detector():
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    try:
        camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
        camera.set(cv2.CAP_PROP_FPS, 30)

        print("[INFO] Taking Before Image ...")
        ret, before = camera.read()
        if not ret:
            raise RuntimeError("Camera Error: Before Image Not Captured")

        before = crop_vial(before)
        cv2.imwrite("before.jpg", before)

        print("[INFO] Waiting for Hotplate to Stir the Solution ...")
        time.sleep(30)  # Adjust waiting time if needed

        print("[INFO] Taking After Image ...")
        ret, after = camera.read()
        if not ret:
            raise RuntimeError("Camera Error: After Image Not Captured")

        after = crop_vial(after)
        cv2.imwrite("after.jpg", after)

        # Convert to HSV for Colour Detection
        before_hsv = cv2.cvtColor(before, cv2.COLOR_BGR2HSV)
        after_hsv = cv2.cvtColor(after, cv2.COLOR_BGR2HSV)

        # Blue Colour Detection
        before_blue_mask = cv2.inRange(before_hsv, lower_blue, upper_blue)
        after_blue_mask = cv2.inRange(after_hsv, lower_blue, upper_blue)

        # Count Blue Pixels
        before_pixels = colour_pixels(before_blue_mask)
        after_pixels = colour_pixels(after_blue_mask)

        # Colour Change Percentage Calculation
        change_percentage = 100 if before_pixels == 0 else ((after_pixels - before_pixels) / before_pixels) * 100

        print(f"Colour Change Percentage: {round(change_percentage, 2)}%")

        # Determine if color change occurred
        result = "YES" if after_pixels > before_pixels else "NO"
        print("Colour Change Detected" if result == "YES" else "No Colour Change")

        # Save Results to CSV
        data = {
            "Before Pixels": [before_pixels],
            "After Pixels": [after_pixels],
            "Colour Change %": [round(change_percentage, 2)],
            "Result": [result],
        }

        df = pd.DataFrame(data)

        # Check if file exists before writing
        file_exists = os.path.exists("results.csv")
        df.to_csv("results.csv", index=False, mode="a", header=not file_exists)

        print("[INFO] Data Saved to results.csv")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        camera.release()
        cv2.destroyAllWindows()

# Run the Colour Change Detector
if __name__ == "__main__":
    colour_change_detector()
