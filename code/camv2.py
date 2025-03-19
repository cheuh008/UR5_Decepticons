import cv2
import numpy as np
import time
import csv

def process_image(i):
    i += 1
    cap = cv2.VideoCapture(0)  # 0 is the default camera
    x, y, w, h = 100, 100, 50, 50  # Example: a 50x50 square at (100, 100)
    csv_filename = f"RGB_values_Timedstamp.csv"
    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Sample ID', 'Timestamp', 'ROI Colour (BGR)'])
        print(f"Created new CSV file: {csv_filename}")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            roi = frame[y:y+h, x:x+w]
            average_color = np.mean(roi, axis=(0, 1)).astype(int)
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"Sample_ID: {i}, Timestamp: {timestamp}, ROI Color (BGR): {average_color}")
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)  # Draw rectangle around ROI
            cv2.imshow('Camera Stream', frame)

            with open(csv_filename, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([i, timestamp, average_color])


    finally:
        # Release the camera and close all OpenCV windows
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    process_image(0)