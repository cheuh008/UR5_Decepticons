import cv2
import os
import numpy as np
import time
import csv

def process_image(i):
    """Track the average color (in BGR) of the ROI. Since methylene blue is typically blue, checks for a significant drop in the Blue channel 
    (or for near-equal B, G, R values, signaling a fade to grey/white). When we detect that it's close to colorless 
    (e.g., all channels above a certain threshold and similar to each other), we stop capturing."""
    
    i += 1
    cap = cv2.VideoCapture(0)  # 0 is the default camera
    x, y, w, h = 311, 108, 36, 46 # Example: a 50x50 square at (100, 100)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    
    file_name = "RGB_values.csv"
    file_path = os.path.join(data_dir, file_name)

    try:

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            roi = frame[y:y+h, x:x+w]
            average_color = np.mean(roi, axis=(0, 1)).astype(int)
            b, g, r = average_color
            
            # Get the current timestamp
            time.sleep(0.2)
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"Sample_ID: {i}, Timestamp: {timestamp}, ROI Color (BGR): {average_color}")
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)  # Draw rectangle around ROI
            cv2.imshow('Camera Stream', frame)

            with open(file_path, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([i, timestamp, average_color])

            #Auto-stops condition when colour is "faded"
            if abs(r - g) < 20 or abs(g - b) < 20 or abs(r - b) < 20:
                break

    finally:
        # Release the camera and close all OpenCV windows
        cap.release()
        cv2.destroyAllWindows()
        print("Colour Change Detected")
        return True


if __name__ == "__main__":
    process_image(0)
