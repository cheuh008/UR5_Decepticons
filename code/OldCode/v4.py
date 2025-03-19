import cv2
import numpy as np
import time

def process_image(sample_id):
    cap = cv2.VideoCapture(0)  # 0 is the default camera
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    x, y, w, h = 100, 100, 50, 50  # Example: a 50x50 square at (100, 100)

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Failed to capture frame.")
                break

            # Extract ROI and calculate average color
            roi = frame[y:y+h, x:x+w]
            average_color = np.mean(roi, axis=(0, 1)).astype(int)
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"Sample_ID: {sample_id}, Timestamp: {timestamp}, ROI Color (BGR): {average_color}")

            # Draw rectangle around ROI
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.imshow('Camera Stream', frame)

            # Exit on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        # Release the camera and close all OpenCV windows
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    process_image(0)