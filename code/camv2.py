import cv2
import numpy as np
import time
import csv

<<<<<<< HEAD
cap = cv2.VideoCapture(0)  # 0 is the default camera
x, y, w, h = 267, 102, 72, 78

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        roi = frame[y:y+h, x:x+w]
        average_color = np.mean(roi, axis=(0, 1)).astype(int)
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"Timestamp: {timestamp}, ROI Color (BGR): {average_color}")
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)  # Draw rectangle around ROI
        cv2.imshow('Camera Stream', frame)

=======
def process_image(i):
    i += 1
    # Initialize the camera
    cap = cv2.VideoCapture(0)  # 0 is the default camera

    # Define the region of interest (ROI) coordinates
    x, y, w, h = 100, 100, 50, 50  # Example: a 50x50 square at (100, 100)

    # Create a CSV
    csv_filename = f"RGB_values_Timedstamp.csv"

    # Open a new CSV file to write the data
    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.writer(file)

        # Write headers
        writer.writerow(['Sample ID', 'Timestamp', 'ROI Colour (BGR)'])
        print(f"Created new CSV file: {csv_filename}")

    try:
        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()
            if not ret:
                break

            # Extract the ROI
            roi = frame[y:y+h, x:x+w]

            # Calculate the average color of the ROI
            average_color = np.mean(roi, axis=(0, 1)).astype(int)

            # Get the current timestamp
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
>>>>>>> b97d209ec636c3d63f0d0332fa06ecaea5f45b54

            # Print the color data to the console
            print(f"Sample_ID: {i}, Timestamp: {timestamp}, ROI Color (BGR): {average_color}")

            # Display the frame with the ROI highlighted
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)  # Draw rectangle around ROI
            cv2.imshow('Camera Stream', frame)

            # Save the data to the new CSV
            with open(csv_filename, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([i, timestamp, average_color])

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        # Release the camera and close all OpenCV windows
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    process_image(0)