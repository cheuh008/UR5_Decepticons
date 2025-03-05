import cv2
import numpy as np
import pandas as pd
import warnings
import time
import threading
import os

warnings.filterwarnings("ignore")

# Colour Ranges (Adjust as needed)
lower_yellow = np.array([20, 100, 100])
upper_yellow = np.array([30, 255, 255])
lower_blue = np.array([100, 100, 50])
upper_blue = np.array([130, 255, 255])

""" Counts Pixels """
def colour_pixels(mask):
    return np.sum(mask > 0)

""" Crop Only the Vial Area """
def crop_vial(image):
    height, width, _ = image.shape
    return image[int(height * 0.3):int(height * 0.8), int(width * 0.4):int(width * 0.6)]

""" Open Camera in a Separate Thread """
def open_camera():
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
